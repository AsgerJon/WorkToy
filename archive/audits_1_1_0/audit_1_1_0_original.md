# worktoy 1.1 work list: full read audit (2026-09-25)

## How this was produced

One Claude session read every file in `src/worktoy` (157 files, ~18.7k
lines) and `tests` (251 files, ~26.1k lines) in the layer order from
`src/worktoy/__init__.py`. Every item marked **verified** below was
reproduced with a throwaway script, run as:

```
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. ~/miniforge3/envs/worktoy_env/bin/python probe.py
```

Baseline at the time: Python 3.14.5, `pytest tests` gives 1286 passed,
100% line and branch coverage. None of the bugs below are caught by the
suite.

The repro snippets are meant to become regression tests. Items marked
**DECISION** are behaviour the author may want to keep; mark them KEEP or
CHANGE before a session starts on them.

## Suggested session split

Each group touches a separate slice of the code, so one session per group
can read only the work list, the package `__init__` docstrings, the files
listed, and the tests for that area.

| Group | Items | Files |
|---|---|---|
| A. Dispatch cache and ordering | 1, 2, 7, 13, L3 | `dispatch/_dispatcher.py`, `mcls/_base_space.py`, `dispatch/_type_sig.py`, `core/sentinels/_args.py` |
| B. EZHook capturing too much | 4, 8, 9 | `ezdata/_ez_hook.py`, `ezdata/_ez_space.py`, `mcls/space_hooks/_reserved_names.py` |
| C. KeeBox resolution | 3, 6 | `keenum/_kee_box.py` |
| D. KeeMeta | 10, 11 | `keenum/_kee_meta.py`, `keenum/_kee_meta_meta.py` |
| E. flexCall | 5 | `dispatch/_flex_call.py`, `mcls/space_hooks/_flex_call_hook.py` |
| F. Test support | 12, T1 to T5 | `work_test/samplers/_lorem_sampler.py`, `work_test/_base_test.py`, tests |
| G. Small fixes and docs | L1, L2, L4, D1 to D5 | various |

## Progress

The current work list is `audit_1_1_0_after_a.md`, which carries every
open item over and adds items 14, L5 and L6. This file stays as the
record of the original audit.

### Group A: DONE (2026-09-25)

Items 1, 2, 7, 13 and L3 are fixed. Suite: 1330 passed, 100% line and
branch coverage. A mutation check of 28 deliberate breaks across the
changed files was caught in full.

- **Cache (items 1, 2):** `Dispatcher.__get__` builds a fresh
  `MethodType` on every access and stores nothing on the instance.
  `_getCachedKey` is gone, and `test_peek` lost its cache assertion.
- **Precedence (items 7, 13):** `BaseSpace` records only the class
  body's own registrations, in lists rather than dicts keyed by
  signature, and no longer copies inherited ones in `__init__`. On
  compilation, `collectOverloads`, `collectVariadics`,
  `collectFallback` and `collectFinalizer` walk the method resolution
  order: own registrations first, the nearest class wins an equal
  signature, and the walk stops at the first plain definition. A
  `Dispatcher` written in a class body, or held by a class not built by
  `BaseSpace`, counts as a plain definition (`_definesPlainly`).
- **Cast order (DECIDED: inherited first):** each registration reaches
  the `Dispatcher` with its distance from the class (0 for its own).
  FASTEST and FAST try the nearest first; the SLOW passes try the
  farthest first (`_getCastOrder`), so a signature a subclass adds never
  takes a call its parent handled through a cast. This is what keeps
  `Complex(69, 420)` in `test_dispatcher.py` at `69+420j`.
- **ARGS (L3 and the equality complication):** `ARGS` instances compare
  and hash by inner type and render as `ARGS[int]`; `TypeSig` compares
  an `ARGS` entry structurally and renders it the same way.
- **New tests:** `test_super_overload.py`, `test_overload_binding.py`,
  `test_overload_footprint.py`, `test_override_precedence.py`,
  `test_base_precedence.py`, `test_fallback_precedence.py` (all in
  `tests/test_overload/`), `tests/test_dispatch/test_variadic_type_sig.py`,
  `tests/test_core/test_args_sentinel.py`,
  `tests/test_mcls/test_space/test_lookup_order.py`, plus added cases in
  `test_variadic_prefix_overlap.py`, `test_load_args.py` and
  `test_shadow_reads.py`.

---

## High severity

### 1. `super()` inside an overriding overload recurses forever (verified)

- **Where:** `src/worktoy/dispatch/_dispatcher.py:172` (`_getCachedKey`),
  `:477` (`__get__`)
- **Cause:** the bound dispatch function is cached on the instance under
  `'__bound_dispatch_%s__' % fieldName`. The key has no owner component,
  so the parent's `Dispatcher.__get__` (reached through `super()`) finds
  the child's cached bound method and calls the child again.
- **Repro:**
  ```python
  class Parent(BaseObject):
    @overload(int)
    def foo(self, x): return 'parent'

  class Child(Parent):
    @overload(int)
    def foo(self, x): return 'child+' + super().foo(x)

  Child().foo(1)  # RecursionError
  ```
- **Variants (verified, added in the group A session):**
  - `super().__init__(...)` inside an overloaded `__init__` recurses the
    same way. Python reads `__init__` through the instance during
    construction, so the subclass's bound method is always cached first.
    This is the most common way to hit the bug.
  - A chain of three overriding overloads recurses too.
  - Reaching the parent first (`super(Child, c).foo(1)` from outside)
    caches the parent's bound method, after which `c.foo(1)` silently
    runs the parent version instead of the override.
- **Fix direction:** see item 2; both come from the same cache.
- **Tests:** `tests/test_overload/test_super_overload.py`.

### 2. `copy.copy` of a BaseObject shares its overloaded methods with the original (verified)

- **Where:** same cache as item 1.
- **Cause:** the cached `MethodType` lives in the instance `__dict__`, so
  `copy.copy` copies a bound method whose `__self__` is the original.
  Overloaded calls on the copy then run against the original.
- **Repro:**
  ```python
  class Counter(BaseObject):
    def __init__(self, *args): self.n = 0
    @overload(int)
    def bump(self, k):
      self.n += k
      return self.n

  a = Counter(); a.bump(1)
  b = copy.copy(a); b.bump(10)
  (a.n, b.n)  # (11, 1): the copy's call mutated the original
  ```
- **Variants (verified, added in the group A session):**
  - After `obj.__class__ = Other`, overloaded calls keep running the old
    class's version.
  - The cached bound method makes the instance refer to itself, so an
    instance that has made an overloaded call is only freed by the
    garbage collector, never by reference counting.
  - Every called instance gains a `__bound_dispatch_*__` entry in its
    `__dict__`.
  - `copy.deepcopy` is not affected: it rebinds the copied method to the
    copy.
- **Fix direction (DECIDED: drop the cache):** build the `MethodType` on
  every access, as Python does for plain methods. The rejected option was
  keying the cache by dispatcher identity, which would have left the
  reference cycle and the `__dict__` entries in place. `test_peek` in
  `tests/test_dispatch/test_dispatcher.py` tests the cache's recursion
  guard in `__get__` and goes away with the cache.
- **Tests:** `tests/test_overload/test_overload_binding.py`,
  `tests/test_overload/test_overload_footprint.py`.

### 3. `KeeBox[E](E.MEMBER)` as a default can resolve to a different member (verified)

- **Where:** `src/worktoy/keenum/_kee_box.py:114` (`_resolveNum`)
- **Cause:** there is no identity check. A member argument falls through
  to `valueType(*args)`; for an `int` value type that calls
  `int(member)`, which is the member's index, and then matches by value.
  For other value types it usually raises `KeeBoxValueError` instead. The
  setter path is fine because `__instance_set__` checks
  `isinstance(value, self.fieldType)` first; the default (get) path does
  not.
- **Repro:**
  ```python
  class Slot(KeeNum):
    LEFT = Kee[int](2)
    CENTER = Kee[int](0)
    RIGHT = Kee[int](1)

  class Widget:
    align = KeeBox[Slot](Slot.LEFT)

  Widget().align  # Slot.CENTER
  ```
- **Fix direction:** in `_resolveNum` (and per argument in
  `_resolveFlags`), return the argument directly when it is already a
  member of the field enumeration.

### 4. EZHook turns interpreter-set names into fields (verified)

- **Where:** `src/worktoy/ezdata/_ez_hook.py:142` (`setItemPhase`), with
  the pass-through list in `src/worktoy/mcls/space_hooks/_reserved_names.py:32`
- **Cause:** every class-body value that is not a function and has no
  descriptor methods becomes an `EZField`. That includes names the
  interpreter writes into the namespace:
  - `__classcell__` (any method using `super()` or `__class__`): the
    cell never reaches `type.__new__`, so class creation fails.
  - `__orig_bases__` (from `Generic[T]` bases): becomes a slot and
    breaks `Generic.__init_subclass__`.
  - also worth checking on 3.13+ / 3.14: `__classdictcell__`,
    `__conditional_annotations__`, `__type_params__`.
- **Repro:**
  ```python
  class Base(EZData):
    x = EZField[int](0)
    def __post_init__(self): pass

  class Sub(Base):
    def __post_init__(self): super().__post_init__()
  # RuntimeError: __class__ not set defining 'Sub' ... __classcell__

  class Box(EZData, Generic[T]):
    x = EZField[int](0)
  # TypeError: argument of type 'member_descriptor' is not a container

  class Holder(EZData):
    x = EZField[int](0)
    class Inner: pass
  tuple(Holder.__ez_fields__), Holder().Inner  # (('x', 'Inner'), <class 'type'>)
  ```
- **Fix direction:** pass through the interpreter-set dunders above.
  **DECISION:** should classes (and other bare class constants) in an
  EZData body become fields at all? A nested class currently becomes a
  field whose default is `type(Inner)(Inner)`, which is `type`.

---

## Medium severity

### 5. flexCall rejects keyword arguments for positional parameters (verified, DECISION)

- **Where:** `src/worktoy/dispatch/_flex_call.py:105` (the wrapper),
  applied to every plain method by
  `src/worktoy/mcls/space_hooks/_flex_call_hook.py:40`, which is on
  `AbstractNamespace`, so it affects BaseObject, KeeNum, EZData and
  everything built on them.
- **Cause:** `minPos` is checked against `len(args)` only; parameters
  supplied by keyword are not counted.
- **Repro:**
  ```python
  class Plain(BaseObject):
    def bar(self, x): return x

  Plain().bar(x=1)     # TypeError: requires at least '2' positional ...
  Plain().bar(1, 2, 3) # returns 1, extras silently dropped
  ```
- **Fix direction:** subtract names present in `kwargs` from the missing
  list before raising. **DECISION:** whether silent truncation of extra
  positionals on ordinary methods should stay, given the fail-fast
  philosophy in `waitaminute`.

### 6. `KeeBox` over `KeeFlags` fails for combined members (verified)

- **Where:** `src/worktoy/keenum/_kee_box.py:161`
- **Cause:** the lookup key is `frozenset(h.name for h in highs)`, so a
  combined member contributes `'READ_WRITE'` instead of
  `{'READ', 'WRITE'}`.
- **Repro:**
  ```python
  class Perm(KeeFlags):
    READ = KeeFlag(); WRITE = KeeFlag()

  class File:
    mode = KeeBox[Perm]('READ')

  f = File(); f.mode = 'READ_WRITE'  # KeyError: frozenset({'READ_WRITE'})
  class File2:
    mode = KeeBox[Perm](3)
  File2().mode                       # same KeyError
  ```
- **Fix direction:** build the key from the union of `h.names`.

### 7. Inherited overloads beat subclass overrides (verified)

- **Where:** `src/worktoy/mcls/_base_space.py:76` (inherited variadics
  appended first, never deduplicated),
  `src/worktoy/dispatch/_dispatcher.py:189` and `:199` (FAST passes are
  first-registered-wins)
- **Cases:**
  - A subclass that re-declares a variadic overload gets its own version
    for short calls (the concrete expansions are replaced) but the
    parent's for calls longer than `__variadic_fastpath_limit__`.
  - A subclass that re-declares `@overload(THIS)`: an argument that is an
    instance of a further subclass matches the parent's `(Parent,)`
    signature first, so the parent's version runs.
- **Repro:**
  ```python
  class VParent(BaseObject):
    @overload(int, ARGS[int])
    def f(self, *a): return 'parent'
  class VChild(VParent):
    @overload(int, ARGS[int])
    def f(self, *a): return 'child'
  VChild().f(1, 2)           # 'child'
  VChild().f(*range(10))     # 'parent'

  class TParent(BaseObject):
    @overload(THIS)
    def g(self, o): return 'parent'
  class TChild(TParent):
    @overload(THIS)
    def g(self, o): return 'child'
  class TGrand(TChild): pass
  TChild().g(TGrand())       # 'parent'
  ```
- **Also affected (verified, added in the group A session):** a class
  inheriting both registrations without declaring anything (a
  grandchild) gets the parent version too, in both cases.
- **Complication:** `ARGS[int] is not ARGS[int]`, and `TypeSig` compares
  its entries by identity, so two variadic signatures written the same
  way never compare equal. An override can only replace an equal
  inherited variadic once `ARGS` instances compare and hash by their
  inner type.
- **Fix direction:** let own variadics replace inherited ones with an
  equal signature, and order own registrations ahead of inherited ones
  in the FAST passes (or rank inherited last).
- **Tests:** `tests/test_overload/test_override_precedence.py`.

### 8. Non-frozen EZData accepts wrongly typed assignment (verified, DECISION)

- **Where:** `src/worktoy/ezdata/_ez_hook.py:312` (only frozen classes
  get a generated `__setattr__`)
- **Repro:** `class Pt(EZData): x = EZField[float](0.0)`, then
  `p = Pt(1); p.x = 'not a float'` succeeds.
- **Note:** `badDelAttrFactory` refuses deletion to protect "every field
  always holds a value of the declared type", which assignment currently
  breaks. **DECISION:** add a casting `__setattr__` for non-frozen
  classes, or narrow the documented guarantee.

### 9. Two EZData bases with fields cannot be combined (verified, DECISION)

- **Where:** `src/worktoy/ezdata/_ez_hook.py:332` (`slotsFactory` puts
  every inherited field into `__slots__` again)
- **Repro:** `class C(A, B)` where both `A` and `B` are EZData classes
  with fields raises `TypeError: multiple bases have instance lay-out
  conflict`.
- **Note:** `EZSpace.__init__` and `initFactory` document merging fields
  from several bases. **DECISION:** support it (would need a different
  storage layout) or reject it early with a clear worktoy exception and
  fix the docstrings.

### 10. `__class_init__` on a KeeNum is silently ignored (verified)

- **Where:** `src/worktoy/keenum/_kee_meta.py:429`
- **Cause:** `KeeMeta.__init__` never calls `AbstractMetaclass.__init__`,
  which is what routes `__class_init__` (and `_notifySubclassHook`).
- **Repro:** a KeeNum subclass with an `@classmethod __class_init__`
  that appends to a list; the list stays empty.

### 11. Custom `KeeMeta` subclasses break `mroNum` and `base` (verified)

- **Where:** `src/worktoy/keenum/_kee_meta.py:136` and `:155`
- **Cause:** `_createBase` special-cases the literal class name
  `'KeeNum'`. The root built for `FontMeta.keeNum` is named
  `'FontMetaNum'`, so it is treated as an ordinary enumeration.
- **Repro:**
  ```python
  class FontMeta(KeeMeta): pass
  class FontNum(FontMeta.keeNum):
    ARIAL = Kee[int](1)
  FontNum.base    # the root 'FontMetaNum', where KeeNum children get themselves
  FontNum.mroNum  # ValueError: ... must have exactly one base, but received none!
  ```
- **Fix direction:** `_getKeeNum` already sets `__root_class__ = True` in
  the root namespace; test for that marker instead of the name.

### 12. Shared sampler state (verified)

- **Where:** `src/worktoy/work_test/samplers/_lorem_sampler.py:33`
  (`sentence = Sentence()` at class level), and the class-level samplers
  on `BaseTest` (`src/worktoy/work_test/_base_test.py:76`)
- **Repro:** two `LoremSampler()` instances; setting `charCount` on one
  gives `(100, 100, True)` for both counts and `a.sentence is b.sentence`.
- **Knock-on:** tests change the shared `BaseTest` samplers (for example
  `test_symbolic_name.py:124`, `test_alias.py:21`, `test_sentence.py:29`,
  `test_point_2d.py:69`), and `tearDownClass` only unloads the test
  module, so those settings leak into later test classes.
- **Fix direction:** per-instance `Sentence` in `LoremSampler`
  (`AttriBox[Sentence]()`); per-test sampler instances or a reset in
  `BaseTest.setUp`.

### 13. Overloads from several bases ignore the method resolution order (verified, added in the group A session)

- **Where:** `src/worktoy/mcls/_base_space.py:62` (`BaseSpace.__init__`
  merges the direct bases left to right, and a later base overwrites an
  equal signature), `src/worktoy/mcls/space_hooks/_load_space_hook.py:74`
  (`postCompilePhase` only checks the class's own body for a plain
  definition)
- **Cases:**
  - `class Both(Left, Right)` with an equal overload in each base runs
    `Right`'s version, where Python's order says `Left`.
  - With an equal variadic overload in each base, short calls run
    `Right`'s version and calls longer than
    `__variadic_fastpath_limit__` run `Left`'s, so the winner changes
    with the length of the call.
  - A plain method in an earlier base (`class C(PlainMixin, Right)`) is
    shadowed by a dispatcher built from `Right`'s overloads. The diamond
    `class LoudRight(Loud, Right)`, where `Loud(Right)` overrides with a
    plain method, runs `Right`'s overload instead of `Loud`'s override.
- **Decision:** signatures from all bases keep merging into one
  dispatcher. On an equal signature the class first in the method
  resolution order wins in every pass. A plain method earlier in that
  order shadows overloads contributed only by later classes.
- **Tests:** `tests/test_overload/test_base_precedence.py`.

---

## Low severity

- **L1. AttriBox storage name collisions (verified).**
  `src/worktoy/core/_object.py:384`, `src/worktoy/desc/_attri_box.py:389`.
  The storage name comes from the field name alone:
  - `fooBar` and `foo_bar` both map to `__foo_bar__`; an `AttriBox[int]`
    returned the `str` stored by the other field.
  - A class attribute `__value__` hides the default of an AttriBox named
    `value` (the read returns `None`), which collides with the codebase's
    own `__x__` plus `Field` convention.
- **L2. worktoy exceptions cannot be unpickled (verified).** They call the
  base `__init__` with no arguments, so `args == ()` and unpickling calls
  the constructor with nothing
  (`pickle.loads(pickle.dumps(TypeException('x', 1, str)))` raises).
  Matters for multiprocessing and xdist. `KeeResolveError` and
  `KeeWriteOnceError` are the exceptions that happen to work, since they
  skip the base `__init__`.
- **L3. `str()` of a variadic `TypeSig` raises (verified).**
  `src/worktoy/dispatch/_type_sig.py:213` uses `t.__name__`; an
  `ARGS[int]` instance has none. The tests in
  `tests/test_dispatch/test_variadic_type_sig.py` pin the rendering
  `TypeSig(int, ARGS[int])`, mirroring how the signature is written.
- **L4. Class-level `MissingVariable` names the metaclass (verified).**
  `src/worktoy/mcls/_abstract_metaclass.py:309` passes `cls` as the
  instance and `MissingVariable.__str__`
  (`src/worktoy/waitaminute/_missing_variable.py:69`) prints
  `type(instance).__name__`, giving `Missing 'BaseMeta.nope'!`.

---

## Tests

- **T1. Fixture bug.** `tests/test_keenum/examples/_prime_valued.py:37`
  loops `while cls.isPrime(p)`, so `indexPrime(0..4)` gives
  `[2, 9, 15, 21, 25]`. `testPrimeValued` only checks divisibility, so it
  passes anyway.
- **T2. Misspelled keyword hides behind a repr check.**
  `tests/test_ezdata/test_ez_field.py:198` and `:208` pass `givenName=` to
  a `FullName` whose field is `givenNames`; EZData drops unknown keywords
  silently and the test only inspects the repr.
- **T3. Tests that check nothing:**
  - no body: `tests/test_mcls/test_hooks/test_duplicate_hook.py`,
    `tests/test_mcls/test_space/test_more_space.py` (`test_str_repr`)
  - no test cases: `tests/test_desc/test_notification.py`
  - no assertions: `tests/test_dispatch/test_dispatcher.py`
    (`test_str_repr`), `tests/test_dispatch/test_space_point.py`
    (`test_dispatcher`)
  - `tests/test_mcls/test_meta/test_class_hash.py` never calls
    `hash(cls)`, only `__class_hash__()` directly.
- **T4. FullName fixture mismatch.** `tests/test_ezdata/examples/_full_name.py`
  says family name first, the fields are `givenNames, familyName`, and
  `test_full_name.py` passes family names first.
- **T5. Weak or no-op lines.** `tests/test_desc/test_field.py:204` and
  `:216` set `__deleter_keys__` / `__delete_keys__` on the instance, which
  has no effect; `tests/test_work_test/test_word_sampler.py:25` iterates
  the characters of one word and checks each is a `str`.

## Out-of-date docstrings

- **D1.** `src/worktoy/waitaminute/desc/_descriptor_exception.py`: lists
  three subclasses; `PhantomBoxError` is a fourth.
- **D2.** `src/worktoy/waitaminute/meta/_illegal_instantiation.py`: says
  `ValidSlice` raises it; `ValidSlice` raises plain `TypeError`.
- **D3.** `src/worktoy/mcls/_abstract_metaclass.py` (`__class_hash__`
  note): says the overload protocol expects the default hash; the
  `TypeSig` docstring says nothing depends on it.
- **D4.** `tests/test_keenum/examples/_prime_num.py` and
  `tests/test_keenum/test_http_status.py`: say `cls(2)` resolves by index;
  only `cls[2]` does.
- **D5.** Test docstrings naming things that no longer exist:
  `worktoy.markwork` (`test_base_sampler.py`), `worktoy.work_test.mixins`
  (`test_complex_mixin.py`), `Ugedag` (`test_kee.py`), `WORKTOY_DATA_DIR`
  (`test_stochastic_word.py`), `strict=True` (`test_int_sampler.py`), RGB
  as an "EZData class" (`examples/_rgb.py`, `_rgb_num.py`), and the
  "Falsy because of name" comments in `examples/_compass.py`.

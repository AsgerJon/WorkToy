# worktoy 1.1 work list: after group A (2026-09-25)

## About this file

This file is the current work list for the 1.1 update. It replaces
`audit_1_1_0.md` for that purpose, which stays as the record of the
original full-read audit. The file has one section per group: first the
groups that are done (A to D), each summarizing what changed, then the
open groups (E to G), each holding its items. Every open item keeps its
original number, so references between the two files stay valid, and
its heading or subheading states its severity; no high-severity item
remains open. Item 15 sits in a last section of its own, since it is out
of scope. Items 13, 14, 15, L5, L6, L7 and L8 are new since the original
audit.

State after group D:

```
PYTHONDONTWRITEBYTECODE=1 ~/miniforge3/envs/worktoy_env/bin/python -m pytest -p no:cacheprovider tests
```

gives 1387 passed on Python 3.14, with 100% line and branch coverage
over both `src/worktoy` and `tests`. The `base_3_7` to `base_3_13`
environments in `~/miniforge3/envs` cover the older versions. Only
`base_3_7` has pytest; the others run the suite as:

```
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. ~/miniforge3/envs/base_3_11/bin/python -m unittest discover -s tests -t . -q
```

Probes are run as:

```
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. ~/miniforge3/envs/worktoy_env/bin/python probe.py
```

Items marked **DECISION** need the author's KEEP or CHANGE before a
session starts on them.

## Status

| Group | Items | Status | Files |
|---|---|---|---|
| A. Dispatch cache and ordering | 1, 2, 7, 13, L3 | **DONE** | `dispatch/_dispatcher.py`, `dispatch/_type_sig.py`, `mcls/_base_space.py`, `mcls/space_hooks/_load_space_hook.py`, `core/sentinels/_args.py` |
| B. EZHook capturing too much | 4, 8, 9 | **DONE** | `ezdata/_ez_hook.py`, `ezdata/_ez_space.py`, `ezdata/_ez_store.py`, `mcls/space_hooks/_reserved_names.py`, `waitaminute/ezdata/_class_field_error.py`, `waitaminute/ezdata/_reserved_method_error.py` |
| C. KeeBox and KeeFlags resolution | 3, 6, 14 | **DONE** | `keenum/_kee_box.py`, `keenum/_kee_flags_meta.py`, `keenum/_kee_flags_space.py`, `waitaminute/keenum/_kee_flag_name_error.py` |
| D. KeeMeta | 10, 11 | **DONE** | `keenum/_kee_meta.py`, `keenum/_kee_meta_meta.py` |
| E. flexCall | 5 | open | `dispatch/_flex_call.py`, `mcls/space_hooks/_flex_call_hook.py` |
| F. Test support | 12, L5, T1 to T5 | open | `work_test/samplers/_lorem_sampler.py`, `work_test/_base_test.py`, `work_test/_sub_test.py`, tests |
| G. Small fixes and docs | L1, L2, L4, L6, L7, L8, D1 to D5 | open | various |

---

## Group A: done

### What was wrong

- **1.** `super()` inside an overloaded override recursed forever,
  including `super().__init__(...)` in an overloaded `__init__`.
  Reaching the parent first through `super()` silently replaced the
  override on that instance.
- **2.** A shallow copy ran its overloaded calls against the original,
  and an instance given a new `__class__` kept running the old class's
  versions. Both came from the bound method cached on the instance, which
  also kept every called instance alive through a reference cycle.
- **7.** A subclass override lost to the parent it overrides for long
  variadic calls, and for `THIS` arguments that are further subclasses.
- **13.** Overloads from several bases ignored the method resolution
  order: the last base won collisions, the winner changed with the length
  of a variadic call, and plain methods in earlier bases were shadowed.
- **L3.** `str()` and `repr()` of a variadic `TypeSig` raised.

### What changed

- **Bound methods (items 1, 2):** `Dispatcher.__get__` builds a fresh
  `MethodType` on every access and stores nothing on the instance, just
  as Python does for plain methods. The cost is about 0.25 microseconds
  per call. `_getCachedKey` is gone.
- **Own and inherited registrations (items 7, 13):** `BaseSpace` records
  only the registrations its own class body makes, in lists of
  `(TypeSig, function)` pairs rather than dicts keyed by signature (a
  signature holding `THIS` hashes differently before and after its class
  exists). When the class compiles, `collectOverloads`,
  `collectVariadics`, `collectFallback` and `collectFinalizer` walk the
  method resolution order:
  - the class body's own registrations come first;
  - each class in the order then contributes its own, and a signature
    equal to one already collected is skipped, so the nearest class wins;
  - the walk stops at the first plain definition of the name
    (`_definesPlainly`). A `Dispatcher` written in a class body, or held
    by a class not built by `BaseSpace`, counts as a plain definition;
    only a `Dispatcher` that `BaseSpace` built from registrations lets the
    walk continue.
- **Cast order (DECIDED: inherited first):** every registration reaches
  the `Dispatcher` with its distance from the class, 0 for its own. The
  exact-type and `isinstance` passes try the nearest first, so an
  override wins wherever it matches. The cast passes try the farthest
  first (`Dispatcher._getCastOrder`), so a signature a subclass adds
  never takes a call its parent already handled through a cast. This is
  what keeps `Complex(69, 420)` in `tests/test_dispatch/test_dispatcher.py`
  at `69+420j`.
- **ARGS (L3, and needed for item 7):** `ARGS` instances compare and hash
  by their inner type and render as `ARGS[int]`. `TypeSig` compares an
  `ARGS` entry structurally and renders it the same way.

### Tests added

- `tests/test_overload/`: `test_super_overload.py`,
  `test_overload_binding.py`, `test_overload_footprint.py`,
  `test_override_precedence.py`, `test_base_precedence.py`,
  `test_fallback_precedence.py`
- `tests/test_dispatch/test_variadic_type_sig.py`
- `tests/test_core/test_args_sentinel.py`
- `tests/test_mcls/test_space/test_lookup_order.py`
- new cases in `test_variadic_prefix_overlap.py`, `test_load_args.py`
  and `tests/test_mcls/test_space/test_shadow_reads.py`

The one existing assertion removed is the cache check in `test_peek`
(`tests/test_dispatch/test_dispatcher.py`), which tested the cache that
was dropped.

### Verification

Besides the suite and coverage, a mutation check applied 28 deliberate
breaks to the changed code, one at a time on a scratch copy of `src`,
and the suite caught every one. The first round let 6 through, each
closed with a new test. To run the suite against a copy of `src`, pass
`-o pythonpath=<copy>` to pytest: `pyproject.toml` sets
`pythonpath = ["src"]`, which otherwise puts the real `src` ahead of
`PYTHONPATH` and makes every mutation look like it survived.

### Notes for later groups

- `BaseSpace.getOverloads()` and `getVariadics()` now return the class
  body's own registrations only, as `dict[str, list[tuple[TypeSig,
  function]]]`. Inherited registrations come from the `collect*` methods,
  which return `(sig, function, distance)` entries.
- `BaseSpace` no longer defines `__init__`, so the calls to
  `BaseSpace.__init__` in `KeeFlagsSpace` and `EZSpace` (and `super()`
  in `KeeSpace`) reach `AbstractNamespace.__init__`.
- `Dispatcher.addSigFunc` and `addVariadicSigFunc` take an optional
  `distance`. A hand-built `Dispatcher` leaves it at 0, which keeps
  registration order in every pass.

---

## Group B: done

### What was wrong

- **4.** `EZHook` turned every plain class-body value into a field,
  including the names the interpreter writes into a class body itself:
  - `__classcell__` (any method using `super()` or `__class__`): class
    creation failed, with `RuntimeError` on 3.8 and later and
    `cannot create 'cell' instances` on 3.7.
  - `__orig_bases__` and `__type_params__`: `Generic[T]` bases and the
    3.12 `class Box[S](EZData)` syntax failed.
  - `__classdictcell__`: on 3.14 an annotated body compiled without the
    future import gained a field of that name.

  A class object (a nested class, or `kind = int`) became a field whose
  default was `type`.
- **8.** Assigning to a field of a non-frozen instance stored any value
  unchecked.
- **9.** Two EZData bases with fields raised `multiple bases have
  instance lay-out conflict`, because every class declared all its
  fields, inherited ones included, as `__slots__`.

### What changed

- **Interpreter names (item 4):** `ReservedNames` lists
  `__classcell__`, `__classdictcell__`, `__orig_bases__` and
  `__type_params__`, which `EZHook.setItemPhase` passes through.
  `__annotate_func__` (3.14) is left out on purpose: it holds a
  function, and functions already pass through.
- **Class objects (item 4, DECIDED: reject):** `setItemPhase` raises the
  new `ClassFieldError` (a `TypeError`, with `clsName`, `fieldName` and
  `classObject`).
- **Assignment (item 8, DECIDED: cast like `__init__`):** the new
  `EZHook.castField` is the one cast that the generated `__init__` and
  the new `setAttrFactory` share, so assignment accepts and refuses
  exactly what construction does. Non-frozen classes get the casting
  `__setattr__`; a name that is not a field is stored as given.
- **Class-body `__setattr__` (DECIDED: forbidden):** binding
  `__setattr__` in an EZData body raises the new `ReservedMethodError`
  (an `AttributeError`, like `ReservedFieldError`), whatever the value.
  The list is `EZSpace.__reserved_ez_methods__`.
- **Storage (item 9, DECIDED: support several bases):** EZData classes
  declare no `__slots__`. Field values live in the instance `__dict__`,
  which every EZData instance had already, since `Object` declares no
  slots. On 3.14 a read measured 14.5 ns against 13.7 ns for a slot. The
  old layout also carried a second slot for every inherited field
  (`Sub(1)` took 32 bytes where `Base(1)` took 24).
  - A data descriptor anywhere in the method resolution order beats the
    instance `__dict__`, so a field sharing its name with one gets an
    `EZStore` (new, `ezdata/_ez_store.py`) through
    `EZHook.storeFactory`. Cases in the library: `Object.directory`, and
    `REAL`/`IMAG` of `ComplexMixin` under `EZComplex`.
  - `_applyDefaults` checks the instance `__dict__` rather than
    `getattr`, so a mixin attribute of the same name no longer
    suppresses the default.
- **Field order (DECIDED: the `dataclasses` order):** `EZSpace.__init__`
  walks the reversed method resolution order and registers each EZData
  class's own fields. The farthest class decides a field's position, the
  nearest class decides the field itself, as with attribute lookup and
  the group A overload merge. The old merge (bases right to left, each
  base's merged fields) disagreed with this in 185 of 2110 small
  hierarchies: `class E(D, A)` reordered the fields `E` inherits from
  `class D(A, B)`. It differs from `dataclasses` in one case: in a
  diamond whose right-hand side redeclares a shared field,
  `dataclasses` keeps the shared base's version, since it also copies
  the fields the left-hand side inherited.

### Tests added

- `tests/test_ezdata/`: `test_interpreter_names.py`,
  `test_class_object_rejected.py`, `test_field_assignment.py`,
  `test_multiple_bases.py`, `test_reserved_method.py`,
  `test_field_storage.py`

The one existing assertion changed is in `test_field_owner_name`
(`tests/test_ezdata/test_ez_data.py`), which checked field names against
`__slots__` and now checks them against `__ez_fields__`.

### Verification

The suite passes on every version from 3.7 to 3.14; the skips are the
tests gated on 3.12 and 3.14. A mutation check applied 22 deliberate
breaks, each on its own copy of `src`, and the suite caught every one;
an unmodified copy passed as a control. Two tests (the diamond
redeclaration and the descriptor defining only `__delete__`) were
written specifically to catch breaks that would otherwise have passed.

### Notes for later groups

- `vars(instance)` now shows the fields. Reading a field without a
  store through the class (`Point2D.x`) raises `MissingVariable` through
  `AbstractMetaclass.__getattr__`, whose message names the metaclass
  (L4), where it used to return the slot descriptor.
- `EZHook.postCompilePhase` uses `BaseSpace._getLookupOrder` through
  `self.space`.
- The names added to `ReservedNames` also reach `ReservedNamespaceHook`
  in every namespace, which raises only when such a name is assigned a
  second time.
- Cost: assigning to a field of a non-frozen instance takes about
  305 ns against 14 ns for a plain attribute on 3.14, almost all of it
  the Python-level `__setattr__`. Checking `isinstance(value,
  fieldType)` before calling `castField` measured 291 ns down to 205 ns;
  it matches `typeCast` except for `slice` fields, which `typeCast`
  always revalidates. Not applied.
- `ClassFieldError` and `ReservedMethodError` call the base `__init__`
  with no arguments like the other exceptions, so L2 applies to them.

---

## Group C: done

### What was wrong

- **3.** A member given as a `KeeBox` default never came back as itself.
  An `int` enumeration read the member as its index and matched that
  against the values, landing on another member (`Slot.LEFT` gave
  `Slot.CENTER`). A `str` enumeration raised `KeeBoxValueError`, and a
  box over `KeeFlags` raised `KeeBoxTypeError` for every member, `NULL`
  included, and for members mixed with names.
- **6.** A box over `KeeFlags` built its lookup key from the plain names
  of the resolved members, so a combined member contributed
  `'READ_WRITE'` and nothing matched: `'READ_WRITE'`, `3` and a combined
  member plus a further flag all raised `KeyError`, by default and by
  assignment.
- **14.** A flag name containing `'_'` could not be told apart from a
  combination: the flags `READ`, `ONLY` and `READ_ONLY` gave two members
  named `READ_ONLY`, with `Clash.READ_ONLY` and `Clash['READ_ONLY']`
  returning different ones. Also `Perm['null']` raised where
  `Perm['NULL']` worked.
- **Found on the way.** Assigning a value that is not a member, such as an
  `RGB` to a `KeeBox[ColorNum]`, raised `AttributeError`.
  `KeeMeta.__instancecheck__` compares the value with every member
  through `==`, which hands the decision to the value's own `__eq__`, and
  `RGB.__eq__` reads `other.r` from a member.

### What changed

- **Member recognition (item 3 and the `RGB` case):** the new
  `KeeBox._isMember` refuses any value whose type is not built by
  `KeeMeta` or `KeeFlagsMeta` before running `isinstance`, so a value's
  own `__eq__` is never asked about a member. Members of subclass
  enumerations are still accepted, as before. Both `_resolveNum` and
  `__instance_set__` use it; `_resolveNum` returns a member as it is.
- **Flags (items 3 and 6):** `_resolveFlags` resolves each argument by
  subscripting the flags class, so the box accepts per argument exactly
  what the class does: members, names in any case and order, indices.
  The result is built from the union of the members' `names`.
- **Flag names (item 14, DECIDED: refuse `'_'`):**
  `KeeFlagsSpace.addKeeFlag` raises the new `KeeFlagNameError` (a
  `ValueError` with `clsName` and `name`, like `KeeCaseException`) in the
  class body. `KeeFlagsMeta._resolveName` compares canonical names
  ignoring case before splitting, which fixes `'null'`.

### Tests added

- `tests/test_keenum/`: `test_kee_box_member_default.py`,
  `test_kee_box_combined_flags.py`, `test_kee_flag_names.py`

No existing assertion changed.

### Verification

The suite passes on every version from 3.7 to 3.14. A mutation check
applied 11 deliberate breaks, each on its own copy of `src`, and the
suite caught 10; an unmodified copy passed as a control. The survivor
drops the upper-casing of the member name in `_resolveName`, which only
matters for lower-case flag names; see L7.

### Notes for later groups

- `cls['READ_WRITE', 'EXECUTE']` on a flags class still raises
  `KeyError`: several names at once must each be a single flag name.
  `KeeBox` resolves each argument separately, so it accepts that
  combination. Nothing documents the subscript form, so it is left as is.
- The `RGB` fixture (`tests/test_keenum/examples/_rgb.py`) raises from
  `__eq__` on a foreign type instead of returning `NotImplemented`. It is
  left as it is, since it is exactly what exposed the `KeeBox` issue.
- `KeeFlagNameError` calls the base `__init__` with no arguments, so L2
  applies to it.

---

## Group D: done

### What was wrong

- **10.** `KeeMeta.__init__` never called the inherited `__init__`, so a
  `KeeNum` class's `__class_init__` never ran, and its bases never
  heard of it through `__subclasshook__`, both of which
  `AbstractMetaclass.__init__` provides for every other worktoy class.
- **11.** `_createBase` recognised the root by the name `'KeeNum'`. Each
  subclass of `KeeMeta` builds a root of its own through `keeNum`, named
  after the metaclass (`FontMetaNum` for `FontMeta`), which is the class
  enumerations under that metaclass derive from. That root failed the
  name check: `FontMeta.keeNum.base` and every `mroNum` below it raised
  `ValueError`, and `FontNum.base` was the root instead of `FontNum`.
- **Found on the way (same cause).** An ordinary enumeration that
  happens to be named `KeeNum` passed the name check: a subclass of it
  took itself as its base, with an empty `mroNum`.

### What changed

- **`__class_init__` (item 10):** `KeeMeta.__init__` takes the bases,
  namespace and keyword arguments instead of discarding them, builds the
  members, and ends by calling the inherited `__init__`. Coming last, a
  `__class_init__` hook sees the finished members.
- **Root (item 11, DECIDED: identity with `keeNum`):** `_createBase`
  compares with `type(cls).keeNum`, the root the class's own metaclass
  builds and caches, instead of comparing names. The root is its own
  base, and so is every enumeration derived directly from it. The
  `__root_class__` marker that `_getKeeNum` wrote into the root
  namespace was never read, so it is gone. The comparison must not run
  while a root is still being built, or `keeNum` would build a second
  one; it cannot today, since `_getKeeNum` builds the root with
  `__new__` alone and `base` is computed on first read.

### Tests added

- `tests/test_keenum/`: `test_kee_num_class_init.py`,
  `test_custom_kee_meta_base.py`

No existing assertion changed.

### Verification

The suite passes on every version from 3.7 to 3.14. A mutation check
applied 6 deliberate breaks, each on its own copy of `src`, and the suite
caught every one; an unmodified copy passed as a control.

### Notes for later groups

- Deriving an enumeration under a custom metaclass from the wrong root,
  as in `class Bad(KeeNum, metaclass=FontMeta)`, is refused at class
  creation, but the message ("must have exactly one base, but received
  none!") does not name the root to derive from; see L8.

---

## Group E: flexCall (open)

Files: `dispatch/_flex_call.py`, `mcls/space_hooks/_flex_call_hook.py`

### 5. flexCall rejects keyword arguments for positional parameters (medium, verified, DECISION)

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

---

## Group F: Test support (open)

Files: `work_test/samplers/_lorem_sampler.py`, `work_test/_base_test.py`, `work_test/_sub_test.py`, tests

### 12. Shared sampler state (medium, verified)

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

### Low severity

- **L5. `SubTest` used without calling it raises an empty
  `RuntimeError` (verified, new).** `with self.subTest:` never pushes a
  label, and `__exit__` pops one in its `finally`
  (`src/worktoy/work_test/_sub_test.py:208`), so `_popCurrent` raises a
  bare `RuntimeError` (`:122`). Raised from `finally`, it also replaces
  whatever the block itself raised. Only `with self.subTest(...):` works.
  Fix direction: push the fallback label in `__enter__` when nothing was
  pushed, or raise a typed exception naming the required call.

### Test issues

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

---

## Group G: Small fixes and docs (open)

Files: various

### Low severity

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
- **L4. Class-level `MissingVariable` names the metaclass (verified).**
  `src/worktoy/mcls/_abstract_metaclass.py:309` passes `cls` as the
  instance and `MissingVariable.__str__`
  (`src/worktoy/waitaminute/_missing_variable.py:69`) prints
  `type(instance).__name__`, giving `Missing 'BaseMeta.nope'!`.
- **L6. `Field(other)` drops the `setName` hooks (verified, new).** The
  copy constructor (`src/worktoy/desc/_field.py:224`) copies every hook
  group except `__set_name_keys__`, so a callback registered with
  `@field.setName` on the prototype never fires on the copy. Every other
  group is copied, so this looks like an oversight rather than a choice.
- **L7. Lower-case `KeeFlag` names are only partly found (verified, new,
  DECISION).** `KeeNum` refuses member names that are not upper case
  (`KeeCaseException`), but `KeeFlags` accepts any flag name. The
  canonical name of such a flag is found in any case since group C
  (`Low['READ']` and `Low['READ_WRITE']` find `Low.read` and
  `Low.read_write`), but the flag names in another order
  (`Low['write_read']`) and several names at once (`Low['read',
  'write']`) raise `KeyError`: `_resolveName` and `_resolveNames` upper-case
  the query and compare it with the flag names as declared. **DECISION:**
  refuse flag names that are not upper case in the class body, as
  `KeeNum` does, or compare flag names ignoring case on both sides.
- **L8. Deriving from the wrong root gives an unhelpful message (verified,
  new).** An enumeration under a custom metaclass that derives from
  another metaclass's root, as in `class Bad(KeeNum,
  metaclass=FontMeta)`, is refused at class creation by
  `KeeMeta._createBase` with "Enumerating classes derived from
  'FontMeta', must have exactly one base, but received none!". The
  message should say that the base must be `FontMeta.keeNum` or an
  enumeration derived from it.

### Out-of-date docstrings

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

---

## Out of scope

### 15. On 3.14, classes built by some metaclasses report the wrong `__annotations__` (medium, verified, new, OUT OF SCOPE)

- **Where:** every worktoy metaclass whose own class body holds
  annotations: `EZMeta` (`ezdata/_ez_meta.py`), `KeeMeta`
  (`keenum/_kee_meta.py`), `KeeFlagsMeta` (`keenum/_kee_flags_meta.py`),
  `KeeMetaMeta` (`keenum/_kee_meta_meta.py`), `MetaFlow`
  (`waitaminute/control_flow/_meta_flow.py`) and `_MetaARGS`
  (`core/sentinels/_args.py`).
- **Cause:** each of these metaclasses has an `__annotations__` dict of
  its own. From 3.14, a class body compiled without `from __future__
  import annotations` keeps its annotations lazily instead of as an
  `__annotations__` dict. Looking up `cls.__annotations__` then finds
  the metaclass's plain dict before the getter on `type`, which is not a
  data descriptor there, so the lookup falls through to the first class
  in the method resolution order holding such a dict: `Object` for
  EZData classes, `KeeBase` for KeeNum classes.
  `annotationlib.get_annotations(cls)` still answers correctly, 3.13 and
  earlier are unaffected, and so is `BaseMeta`, which has no annotations.
- **Repro:**
  ```python
  # A file without 'from __future__ import annotations', on 3.14
  class Pt(EZData):
    x: float = EZField[float](0.0)

  Pt.__annotations__  # the annotations of 'Object', not {'x': float}
  ```
- **DECIDED: out of scope for 1.1.** A proper fix needs a change to the
  language itself, through a new PEP, so the item belongs to no group.
  Code that needs the annotations of such a class should use
  `annotationlib.get_annotations(cls)`, which answers correctly.

# Code review: core, dispatch, desc and mcls

Scope: the four non-leaf packages of `worktoy`, reviewed from the
entries in `research_notes.md` (one entry per item, written during a
line-by-line read of every module). Each line of reasoning below starts
from something an entry records or implies, states the check that was
run against the checkout, and records the outcome. No source or test
file was modified; every check ran as a throwaway script with
`PYTHONPATH=src` in the `worktoy314` (Python 3.14.8) environment, and
where version behaviour matters also in `worktoy37` (Python 3.7.12).

Outcome vocabulary:

- **Confirmed**: the suspected problem reproduces.
- **Refuted**: the suspicion was wrong; the code behaves well.
- **By design**: the behaviour is real but documented or deliberate.
- **Observation**: a fact worth knowing with no defect behind it.

Severity of recommendations: **medium** (a behavioural defect a user
can hit through the public API), **low** (an inconsistency, a misleading
message, a docstring or annotation that misstates the code, or a cost
on a hot path), **note** (an observation with no action required).

---

## Baseline

The full test suite passes on both interpreters:

| Interpreter | Result |
|---|---|
| Python 3.14.8 | 2238 passed, 50 skipped, 10 subtests passed |
| Python 3.7.12 | 2221 passed, 67 skipped |

Reported coverage is 99% on both. The findings below are therefore
about behaviour the tests do not pin down, not about regressions.

---

## core

### C1. The class keeps the namespace that built it

- Reasoning: `MetaType.__new__` inserts `space['__namespace__'] =
  space` before `type.__new__` and deletes it afterwards. Since
  `type.__new__` copies the namespace, the key should survive on the
  class even though it is gone from the dict.
- Check: `'__namespace__' in Object.__dict__` and whether the dict it
  points to still holds the key.
- Outcome: **Confirmed, by design.** The class holds it (`True`), the
  namespace no longer does (`False`). `AbstractNamespace.getMROSpace`,
  `BaseSpace._getInheritedSpaces` and `AbstractMetaclass.getNamespace`
  all depend on this.
- Recommendation [low, docstring]: say in the `MetaType` docstring that
  every class built by a worktoy metaclass keeps the namespace that
  built it under `__namespace__`. Today only a comment in `__new__`
  and the `AbstractNamespace` docstring mention it, while two packages
  rely on it.

### C2. `_Chill` appended twice when a plain mixin is listed last

- Reasoning: `MetaType.__new__` appends `_Chill` whenever the *last*
  base is not a `MetaType` instance. `class X(BaseObject, Mixin)` has a
  plain last base, yet `_Chill` is already in the MRO through
  `BaseObject`. Appending it again could raise a duplicate-base or MRO
  error.
- Check: build exactly that class and read its MRO.
- Outcome: **Refuted.** The MRO is `X, BaseObject, Object, Mixin,
  _Chill, object`. C3 linearisation accepts the repeated `_Chill`
  because it is last everywhere. Class keywords still reach
  `_Chill.__init_subclass__` (`class Y(Mixin, BaseObject,
  trustMeBro=True)` builds, and `__keyword_arguments__` records the
  keyword).
- Recommendation: none.

### C3. `_AnnotationsDescriptor` effect by interpreter

- Reasoning: the descriptor is installed only when `type` carries its
  own `__annotations__` descriptor (3.10 and up). On 3.7 every class
  should fall through to a base's annotations, as the comment says.
- Check: `type(AbstractMetaclass.__dict__['__annotations__'])` and
  `BaseObject.__annotations__` on both interpreters.
- Outcome: **Confirmed, by design.** On 3.14 the descriptor is
  installed and `BaseObject.__annotations__` is `{}`. On 3.7 the
  metaclass holds a plain dict and `BaseObject.__annotations__` answers
  with the six annotations of `Object`, exactly as documented.
- Recommendation [low, docstring]: the three method docstrings of
  `_AnnotationsDescriptor` restate the method names, and the one on
  `__get__` says the owner's annotations are returned for class and
  instance access alike, while a read on the metaclass itself returns
  the metaclass's own dict. The class docstring already states the
  two-way rule; drop or correct the method docstrings.

### C4. Duplicate sentinel refusal

- Reasoning: a second class statement at a registered name must raise
  `DuplicateSentinel` naming the module of the refused statement.
- Check: declare `class THIS(Sentinel)` in a script.
- Outcome: **Confirmed, by design.** The message names
  `worktoy.core.sentinels._this` as the existing declaration and
  `__main__` as the refused one.
- Recommendation: none.

### C5. Unreachable branches in the context getters

- Reasoning: `Object.getContextInstance` and `getContextOwner` test
  `hasContext()` and then, inside that branch, raise `MissingVariable`
  if `__call_chain__ is None`. `hasContext` is `bool(__call_chain__)`,
  so a `None` chain can never enter the branch.
- Check: read the source; `hasContext` has no other path.
- Outcome: **Confirmed.** Two dead branches, harmless.
- Recommendation [low]: remove the two `is None` checks, or move them
  above the `hasContext` test if the intent was to distinguish an
  uninitialised descriptor (one built without `Object.__init__`) from
  an empty stack.

### C6. Private name derivation collapses distinct names

- Reasoning: `getPrivateName` lower-cases and inserts underscores
  before capitals, so `fooBar` and `foo_bar`, and `X` and `x`, derive
  one private name; acronyms get one underscore per letter.
- Check: derive names for `fooBar`, `foo_bar`, `HTTPServer`, `X`, `x`,
  `a1B`.
- Outcome: **Confirmed, by design** for the documented cases:
  `__foo_bar__` twice, `__h_t_t_p_server__`, `__x__` twice, `__a1_b__`.
  Within one class body `AttriBox._refuseStorageCollision` refuses the
  second spelling. Across classes it does not; see E3.
- Recommendation: see E3. The acronym rendering is only cosmetic.

### C7. A signal body with an annotation

- Reasoning: `ControlSpace.__setitem__` admits a whitelist plus
  non-callable attributes of `Exception`. An annotated line in a signal
  body writes `__annotations__` (eager, with the future import) or, on
  3.14 without it, `__annotate_func__`, neither of which is admitted.
- Check: declare `class Sig(ControlFlow): x: int = 1` and `x: int`
  alone, with and without the future import, on 3.14 and 3.7.
- Outcome: **Confirmed.** Every variant raises `ControlClassError`,
  which is the intended refusal, but the message names the
  interpreter's bookkeeping key rather than the user's line: "tried
  implementing attribute `__annotations__`" with the future import, and
  "tried implementing attribute `__annotate_func__`" for an
  annotation-only line on 3.14 without it. The one with a value is
  reported as `x` only on 3.14 without the future import, where the
  value is bound before the annotation machinery runs.
- Recommendation [low, message]: in `ControlSpace.__setitem__`, map
  `__annotations__`, `__annotate__` and `__annotate_func__` to a message
  saying that a signal body may not carry annotations, and name the
  annotated attribute where the dict allows it.

### C8. Rootness recorded twice in `ControlSpace` and `MetaFlow`

- Reasoning: `ControlSpace.__init__` keeps `__is_root__` as an attribute
  of the namespace, and `MetaFlow.__prepare__` also writes an
  `__is_root__` key into the same namespace. One of the two could be
  redundant.
- Check: read `ControlFlow.__dict__['__is_root__']`,
  `SkipSet.__dict__.get('__is_root__')` and `SkipSet.__is_root__`.
- Outcome: **Refuted.** The key becomes the class attribute
  (`True` on the root, `False` on `SkipSet`) that `MetaFlow.__new__`
  reads as `cls.__is_root__`, while the namespace attribute is what
  `__setitem__` reads while the body executes. The two records have
  different consumers.
- Recommendation: none.

### C9. `ARGS.__iter__` has no user

- Reasoning: `TypeSig` iterates its raw types and reads
  `__inner_type__` directly, so yielding the instance from `__iter__`
  looked purposeless from the non-leaf read alone.
- Check: grep `src` and `tests` for iteration over an `ARGS` instance.
- Outcome: **Refuted.** `tests/test_mcls/test_space/test_shadow_reads.py`
  writes `@overload(str, *ARGS[int])`. Star-unpacking is the use:
  `__iter__` yielding the instance lets a subscript be written with or
  without the star.
- Recommendation [low, docstring]: say so in the `__iter__` docstring,
  which currently only says "ARGS is iterable and yields itself".

### C10. `_MetaARGS.__call__` return annotation

- Reasoning: the method is annotated `-> _MetaARGS` but returns an
  instance of the class called, an `ARGS`.
- Check: `type(ARGS[int])` is `ARGS`.
- Outcome: **Confirmed.** Annotation only.
- Recommendation [low, typing]: annotate as `ARGS` (under
  `TYPE_CHECKING`) or `Any`.

### C11. `parseKwargs` contract

- Reasoning: a `bool` should pass as an `int`, and a missing key should
  return the keywords untouched.
- Check: `Object.parseKwargs('a', int, a=True, b=2)` and
  `Object.parseKwargs('a', 'b', b=3)`.
- Outcome: **Confirmed, by design.** `(True, {'b': 2})` and
  `(3, {})`. The method returns a fresh dict each time, so the caller's
  mapping is not mutated.
- Recommendation: none.

### C12. `Object.__init__` accepts any arguments

- Reasoning: the constructor captures `*args, **kwargs` for the boxes,
  so every `Object` subclass without its own `__init__` accepts any
  call silently.
- Check: `Object(1, 2, x=3).getPosArgs()` returns `(1, 2)`.
- Outcome: **Observation.** This is the capture mechanism the boxes
  need, but it has a consequence recorded under E12.
- Recommendation: none here.

### C13. Owner frame on write and delete

- Reasoning: `__get__` pushes the `owner` Python passes (the class the
  attribute was read through), while `__set__` and `__delete__` push
  `type(instance)`. A hook could see different owners for one
  attribute.
- Check: a spy descriptor placed on `A`, accessed through a `B(A)`
  instance, records `self.owner` on get and set.
- Outcome: **Refuted in practice.** Both record `B`: for instance
  access Python passes `type(instance)` as the owner anyway. The two
  only differ when `__get__` is called by hand with another owner.
- Recommendation: none.

### C14. Message subject in `_deletedGuard`

- Reasoning: when the descriptor has no field name, `_deletedGuard`
  raises `MissingVariable(instance, '__field_name__', str)`, naming the
  accessed instance as the object missing the variable, while the
  variable is the descriptor's own.
- Check: read the source; `getPrivateName` passes `self` for the same
  condition.
- Outcome: **Confirmed.** Message only, and only reachable through a
  descriptor read by hand before placement.
- Recommendation [low, message]: pass `self`.

---

## dispatch

### D1. `flexCall` lists `self` among missing arguments

- Reasoning: `requiredNames = co_varnames[:minPos]` includes the first
  parameter of a method, so a call with too few positionals on a
  wrapped method names `self` as missing.
- Check: wrap `def m(self, a, b=1)` and call it with no arguments.
- Outcome: **Confirmed.** The message reads "requires at least '2'
  positional arguments but received only '0', missing arguments:
  (self and a)". For the two users of `flexCall` (`BaseDescriptor`
  callbacks and `FlexCallHook`) the instance is always supplied, so the
  message only appears when `a` is genuinely missing, and then `self`
  is noise.
- Recommendation [low, message]: when the first parameter name is
  `self` or `cls` and it was supplied, leave it out of the list; or
  report only the names after the ones received, which the helper
  already does when the instance is passed.

### D2. `Dispatcher.overload` accepts unknown keywords

- Reasoning: `overload.__new__` refuses any keyword but `strict`
  through `_refuseKeywords`; `Dispatcher.overload` reads
  `kwargs.get('strict')` and ignores the rest.
- Check: `@d.overload(int, stric=True)` on a bare `Dispatcher`, and the
  same typo through `overload` in a class body.
- Outcome: **Confirmed.** The dispatcher accepts the typo silently and
  leaves the signature open to casts; `overload` raises
  `TypeError: overload() got an unexpected keyword argument 'stric'`.
- Recommendation [low]: call the same refusal from
  `Dispatcher.overload`, or move `_refuseKeywords` to `TypeSig` so both
  entry points share it.

### D3. `flex` admits callables that `Permuter` then refuses

- Reasoning: `overload._refuseMethodKinds` admits any callable that is
  not a staticmethod or classmethod, but `Permuter.__init__` accepts the
  function only as a `types.FunctionType`.
- Check: apply `overload.flex(int, str)` to a `functools.partial`.
- Outcome: **Confirmed.** `TypeException` from `Permuter`, worded as
  "Expected object at name 'arg' to be an instance of 'Arrangement' or
  'function'", which says nothing about `flex`. `CallMeMaybe.__init__`
  would have accepted the partial.
- Recommendation [low]: either accept any callable in `Permuter` (the
  arrangement logic does not need a code object) or refuse non-function
  callables in `flex` with a message naming the decorator.

### D4. Keyword duplicating a positional

- Reasoning: `bindKeywords` returns `None` when a keyword names a
  parameter already filled by position, so the call falls to the
  fallback or `DispatchException`, where Python would raise
  `TypeError: got multiple values`.
- Check: `P(1, x=2)` against `@overload(int, int) def __init__(self,
  x, y)`.
- Outcome: **By design.** `DispatchException`, which is a `TypeError`
  subclass, and its message lists the keywords received.
- Recommendation: none.

### D5. A nearer variadic takes a parent's explicit signature

- Reasoning: `_getExactFuncMap` replaces the function of a concrete
  signature by that of a nearer variadic signature covering it exactly,
  and the FAST pass iterates the same map.
- Check: parent `@overload(int, int)`, child `@overload(ARGS[int])`,
  called with ints, with an `int` subclass and with bools.
- Outcome: **By design.** All three calls reach the child's variadic,
  as the `Dispatcher` docstring promises ("a variadic override in a
  subclass takes every call it accepts").
- Recommendation: none.

### D6. Finalizer exception chaining

- Reasoning: a finalizer raising while the body raised should chain
  from the body's exception.
- Check: body raises `ValueError`, finalizer raises `KeyError`.
- Outcome: **Confirmed, by design.** `KeyError` propagates with
  `__cause__` the `ValueError`.
- Recommendation: none.

### D7. `super()` through a dispatcher

- Reasoning: `__get__` returns a fresh `MethodType` on instance access
  and stores nothing on the instance, so `super().f(...)` from a
  subclass dispatcher must bind the parent's compiled function.
- Check: `T(S)` where both overload `f`, `T.f` calling `super().f(1)`.
- Outcome: **Confirmed, by design.** Returns `'TS'`.
- Recommendation: none.

### D8. `validateTypes` and `typing.Any`

- Reasoning: on 3.11 and up `type(Any)` is a metaclass, so the class
  test passes; the `isinstance` probe must catch it.
- Check: `TypeSig.validateTypes(typing.Any)` and `type(None)`.
- Outcome: **Confirmed, by design.** `Any` is refused at declaration
  with a message naming the position; `type(None)` is accepted.
- Recommendation: none.

### D9. Unhashable argument classes

- Reasoning: `TypeSig.fromArgs` builds a tuple of classes; a class whose
  metaclass sets `__hash__ = None` makes the exact-map read raise
  `TypeError`, which the closure catches.
- Check: dispatch an instance of such a class against `@overload(object)`.
- Outcome: **Confirmed, by design.** The call reaches the `isinstance`
  pass and returns.
- Recommendation: none.

### D10. `addVariadicSigFunc` registers a signature without `ARGS`

- Reasoning: the method says the trailing `ARGS` is not validated. A
  signature without one still reaches `_getExactVariadics` and the
  variadic passes, which read `raw[-1].__inner_type__`.
- Check: `d.addVariadicSigFunc(TypeSig(int, str), func)`, place the
  dispatcher with `setattr`, call once.
- Outcome: **Confirmed.** `AttributeError: type object 'str' has no
  attribute '__inner_type__'` at the first call, from inside the
  compile step, with no hint that registration was wrong.
- Recommendation [medium]: refuse at registration, as `addSigFunc`
  refuses a duplicate: require `types and isinstance(types[-1], ARGS)`
  and raise `TypeException` naming the signature otherwise. The
  decorator paths (`overload`, `Dispatcher.overload`) never produce
  such a signature, so only hand-wired dispatchers are affected.

### D11. `TypeSig.__call__` docstring names the wrong caller

- Reasoning: the docstring says `Dispatcher._copySig` relies on the
  no-argument copy. `_copySig` builds `type(sig)(*sig.getDeclaredTypes())`
  and never calls the signature. The caller that does rely on it is
  `LoadSpaceHook.setItemPhase`, which registers `sig()` so the
  `overload` object keeps `THIS`.
- Check: read both call sites.
- Outcome: **Confirmed.** Docstring only. (The `TypeSig` entry in
  `research_notes.md` repeats the docstring's claim and inherits the
  error.)
- Recommendation [low, docstring]: name `LoadSpaceHook`.

### D12. The `HASHABLE` alias

- Reasoning: `HASHABLE = Union[type, int]`, but nothing puts an `int`
  into a signature; the non-class entries are `ARGS` instances.
- Outcome: **Confirmed.** Typing only.
- Recommendation [low, typing]: `Union[type, ARGS]`.

### D13. Keyword calls cannot reach registrations without a code object

- Reasoning: `_getKeywordBindings` skips a registration whose target has
  no `__code__` (a builtin, a callable object). Such registrations are
  reachable by position only.
- Outcome: **Observation.** Consistent with D3: the decorator paths
  only ever register plain functions, so this affects hand-wired
  dispatchers alone.
- Recommendation [note]: state it in the `Dispatcher` docstring under
  "Keyword arguments".

### D14. `THIS` resolution when one `overload` is bound in two classes

- Reasoning: `LoadSpaceHook` registers copies of the signatures so the
  `overload` object keeps `THIS`; placing a second class must resolve
  `THIS` to that class, not the first.
- Check: one `overload(THIS)` object bound as `f` in `A1` and `A2`.
- Outcome: **Confirmed, by design.** `A1.f` dispatches on `A1`, `A2.f`
  on `A2`; the declared signatures read `TypeSig(A1)` and
  `TypeSig(A2)`.
- Recommendation: none.

---

## desc

### E1. `FastBox` on an owner without an instance dict

- Reasoning: `FastBox.__get__`, `__set__` and `__delete__` read
  `instance.__dict__` directly, so a `__slots__`-only owner fails with
  the interpreter's bare `AttributeError`, where `AttriBox._store`
  raises `MissingInstanceDict` naming the field.
- Check: `class SlotFast: __slots__ = (); x = FastBox[int](1)`, read
  `x`.
- Outcome: **Confirmed.** `AttributeError: 'SlotFast' object has no
  attribute '__dict__'`, which the attribute protocol reads as the
  attribute being absent (`hasattr` answers `False`).
- Recommendation [low]: catch the `AttributeError` of the dict read and
  raise `MissingInstanceDict(instance, self.__field_name__)` from it,
  as `AttriBox` does. The `FastBox` docstring already names the
  requirement; the exception should too.

### E2. `AttriBox` tags collide with `Object`'s placement record

- Reasoning: `_applyTags` writes `__field_name__`, `__field_owner__` and
  `__field_box__` onto every object the box builds. The first two are
  the names `Object` uses to record where a descriptor was placed. A
  default built from an `Object` subclass is therefore marked as placed.
- Check: `Outer.inner = AttriBox[Inner]()` with `Inner(BaseObject)`;
  read `o.inner`, then `hasattr(o.inner, 'instance')`, and the same on
  a plain `Inner()`.
- Outcome: **Confirmed.** The built `Inner` carries
  `__field_name__ == 'inner'`, and `hasattr(inner, 'instance')` raises
  `WithoutException` (a `RuntimeError`) instead of returning `False`,
  while the untagged `Inner()` answers `False`. This breaks the promise
  in the `Object` docstring that `hasattr` and `inspect.getmembers`
  answer on a value no class holds. `getPrivateName` on the tagged
  value also answers `__inner__`.
- Recommendation [medium]: give the tags names of their own (for
  example `__box_field_name__`, `__box_field_owner__`, keeping
  `__field_box__`), and update the readers in the leaf packages. If the
  overlap is intended so a built value "knows its field", document it
  on `Object` and make `getContextInstance` tolerate a tagged value.

### E3. Storage collision across a class hierarchy

- Reasoning: `_refuseStorageCollision` inspects `owner.__dict__` only,
  so a subclass box whose name derives the same storage name as a
  parent's box is not refused, and the two share one slot.
- Check: `Par.fooBar = AttriBox[int](1)`, `Chi(Par).foo_bar =
  AttriBox[str]('a')`; set `c.fooBar = 7` and read both.
- Outcome: **Confirmed.** Both read `7`: the `str` field of the child
  returns an `int` written through the parent's field, with no error.
  Within one body the same pair is refused with `StorageCollision`.
- Recommendation [medium]: walk `owner.__mro__` in
  `_refuseStorageCollision` (skipping the owner's own entry for `self`),
  or derive the storage name from the field name verbatim with a
  separator the private-name rule cannot produce, so distinct spellings
  never collide. The second removes the whole class of collisions and
  the need for the check.

### E4. Text and number field types use different rules

- Reasoning: `_isNumberField` consults `castRule`, trusting a number
  subclass with a constructor of its own, while `_isTextField` uses
  `issubclass`, sending every `str` subclass through `resolveText`.
- Check: `Name(str)` with its own `__new__` and `Level(int)` with its
  own `__new__`, as field types with a lone default and on assignment.
- Outcome: **Refuted in behaviour.** `resolveText` defers to
  `typeCast`, and `typeCast` itself consults `castRule`: for `Name` the
  rule is `None`, so the cast falls back to `Name('x')` and the field
  holds `'name:x'`; assignment gives `'name:y'`; `Level('2')` builds
  `20`. The two predicates differ in code but reach the same answer
  because `typeCast` makes the decision underneath.
- Recommendation [note]: use `castRule` in `_isTextField` too, for one
  rule in one place; no behaviour changes.

### E5. Refusal message from `_callFieldType`

- Reasoning: the method raises `TypeException('value', badValue, ...)`
  with the literal name `value` and, when the field type was called
  with no arguments, `None` as the bad value, while `resolveText`,
  `resolveNumber` and `_resolve` name the field.
- Check: `AttriBox[Pt]()` where `Pt.__init__` requires an argument.
- Outcome: **Confirmed.** "Expected object at name 'value' to be an
  instance of 'Pt', but received object: 'None' of type 'NoneType'!",
  which suggests `None` was passed when nothing was.
- Recommendation [low, message]: name the field, and for an empty
  argument list say that the field type refused a call with no
  arguments (the chained `TypeError` already says why).

### E6. A new `flexCall` wrapper on every access for undecorated overrides

- Reasoning: `BaseDescriptor._getCallback` wraps the resolved callback
  with `flexCall` on every hook call. For a decorated callback the
  marker makes that a no-op, but an override that was never decorated
  gets a fresh wrapper (closure, metadata copy, `__dict__` update) on
  every attribute access.
- Check: compare the identity of two consecutive `_getCallback` results
  for a decorated callback and for an undecorated override.
- Outcome: **Confirmed.** Decorated: same object twice. Override: a new
  object each time. The class docstring says the override "is wrapped
  as it is called", so the behaviour is intended, but the cost sits on
  the hot path of every get, set and delete of such a descriptor.
- Recommendation [low, performance]: cache the wrapped callback per
  `(owner, key)` on the descriptor, or wrap undecorated overrides once
  at `__set_name__`/`__init_subclass__` time.

### E7. `hookSetName` skips the flex treatment

- Reasoning: the six access hooks resolve through `_getCallback`, which
  applies `flexCall`; `hookSetName` unwraps `__func__` by hand and
  calls the callback as it is. An override of a set-name callback that
  declares fewer parameters would fail where an access-hook override
  succeeds.
- Check: `Par.f = Field()` with a decorated `_onName(cls, desc)`;
  `Chi(Par).g = Field(Par.f)` (which copies the set-name keys) with an
  override `_onName(cls)`. Separately, an `onGet` override with fewer
  parameters.
- Outcome: **Confirmed.** The set-name override raises `TypeError:
  _onName() takes 1 positional argument but 2 were given` as the class
  is created, while the `onGet` override with fewer parameters runs.
- Recommendation [low]: route `hookSetName` through `_getCallback` so
  all seven hooks follow the rule the class docstring states.

### E8. `FixBox` default consumes the single write

- Reasoning: a read before the first assignment builds and stores the
  default, so a later assignment must raise `WriteOnceError`.
- Check: read then write.
- Outcome: **Confirmed, by design**, and documented in the `FixBox`
  docstring.
- Recommendation: none.

### E9. `Alias` removes itself at class creation

- Reasoning: when the target resolves during `__set_name__`, the alias
  writes the real object into the owner under its own name. Both names
  should then hold one object, and writes through the alias should land
  in the real field.
- Check: `Ch(Pa).v = Alias('value')`; set `c.v = 5`; compare
  `Ch.__dict__['v']` with `Pa.__dict__['value']`.
- Outcome: **Confirmed, by design.** `c.value == 5` and the two dict
  entries are the same object. Modifying the class dict from inside
  `__set_name__` is safe because `type.__new__` iterates a copy of the
  dict when calling `__set_name__`.
- Recommendation: none.

### E10. Per-instance copies of a lone default

- Check: `AttriBox[list]([1, 2])` on two instances, append to one.
- Outcome: **Confirmed, by design.** `[1, 2, 3]` and `[1, 2]`.
- Recommendation: none.

### E11. Pickling and deep-copying an owner with a tagged field

- Reasoning: `__reduce__` pickles a placed box by `(owner, name)` and
  `__deepcopy__` returns the box, so after a round trip the field value
  must still name the box declared on the class.
- Check: pickle and deep-copy an `Outer` whose `inner` was built.
- Outcome: **Confirmed, by design.** Both copies' `__field_box__` is
  `Outer.__dict__['inner']`.
- Recommendation: none.

### E12. `THIS` with a field type that is a base of the owner

- Reasoning: the `AttriBox` docstring says `Kid.mom = AttriBox[Base]
  (THIS)` builds `Base(kid)` and that "a `Parent` with no constructor
  taking an argument raises `TypeException`". For a `BaseObject`-based
  `Base`, `Object.__init__` accepts any argument (C12), so the build
  succeeds silently.
- Check: `Base(BaseObject)` with no `__init__`, `Kid(Base)` with
  `mom = AttriBox[Base](THIS)`, read `Kid().mom`.
- Outcome: **Confirmed.** A fresh `Base` is built and returned; no
  error. The docstring's promise holds for plain classes only.
- Recommendation [low, docstring]: say that the refusal applies to a
  field type whose constructor refuses the argument, and that a
  `BaseObject` subclass without its own `__init__` accepts anything and
  builds silently.

### E13. `onSet` receives the stored value

- Check: `AttriBox[float]` assigned `1`; the `onSet` callback records
  the type of the value it receives.
- Outcome: **Confirmed, by design.** `('float', 1.0)`.
- Recommendation: none.

### E14. `bool` into an `int` field

- Check: assign `True` to `AttriBox[int]` and `FastBox[int]`.
- Outcome: **By design.** Both store the `bool` unchanged, as the
  `AttriBox` docstring states ("a `bool` assigned to an `AttriBox[int]`
  stays a `bool`").
- Recommendation: none.

### E15. `FastBox[int]` without the trailing call

- Check: `x = FastBox[int]` in a class body, read it.
- Outcome: **By design.** Reads `0`; the empty argument list builds
  `int()`. Consistent with `AttriBox.__set_name__`, which normalises
  the same spelling.
- Recommendation: none.

### E16. `_RootAlias` relies on `typing` internals

- Reasoning: `typing._GenericAlias`, `_name`, `_inst` and `copy_with`
  are private and have shifted between 3.7 and 3.14.
- Check: the test suite on both interpreters (baseline).
- Outcome: **Observation.** Green on 3.7.12 and 3.14.8. Nothing to fix;
  the two interpreter runs are what guards it.
- Recommendation [note]: keep both environments in the release checks
  whenever this file changes.

---

## mcls

### M1. Same-named classes hash alike

- Reasoning: the default `__hash__` of `AbstractMetaclass` hashes
  `(name, base names, metaclass name)` and `__eq__` is identity, so two
  classes with the same name and bases (a class built in a loop or a
  factory, or in two modules) collide in every dict and set.
- Check: build `A(BaseObject)` twice in a factory; compare hashes,
  equality and set size.
- Outcome: **Confirmed, by design.** Hashes equal, classes unequal, set
  of size 2. Correct, with degraded hashing for factories that make
  many same-named classes.
- Recommendation [note]: include `__module__` and `__qualname__` in the
  tuple if such factories appear; otherwise leave as is.

### M2. `METACALL` seeding is done once at the root

- Check: count `__dict__` values that are `METACALL` on `BaseObject`,
  a subclass and a sub-subclass.
- Outcome: **Confirmed, by design.** 17 on `BaseObject`, 0 on its
  subclasses, which inherit them; `NamespaceHook.preCompilePhase` stops
  at the first class along the lookup order that supplies the name.
- Recommendation: none.

### M3. The metaclass called with a plain dict

- Check: `BaseMeta('X', (BaseObject,), {'f': overload(int)(...)})`.
- Outcome: **Confirmed, by design.** The dict is copied into a
  `BaseSpace`, the hooks run, and `X.__dict__['f']` is a `Dispatcher`.
- Recommendation: none.

### M4. Deleting a claimed name

- Check: `del f` after `@overload(int) def f`.
- Outcome: **Confirmed, by design.** `ClaimedName` at class creation,
  with a message explaining why the deletion cannot take effect.
- Recommendation: none.

### M5. Aliasing an overload in the same body

- Check: `g = f` after an overloaded `f`.
- Outcome: **Confirmed, by design.** `g` becomes its own `Dispatcher`
  with the registrations of `f`.
- Recommendation: none.

### M6. `hasattr` on a class with no `__class_getattr__`

- Outcome: **Confirmed, by design.** `__getattr__` raises
  `MissingVariable`, an `AttributeError`, so `hasattr(BaseObject,
  'nope')` is `False`.
- Recommendation: none.

### M7. A base refusing subclasses through `__subclasshook__`

- Check: a base whose `__subclasshook__` raises; declare a subclass.
- Outcome: **Confirmed, by design.** The `TypeError` propagates from
  the class statement.
- Recommendation: none.

### M8. A plain override stops the collection of inherited overloads

- Reasoning: `BaseSpace._getInheritedSpaces` stops at the first class
  that defines the name plainly, so a further subclass that overloads
  the name again sees only its own registrations.
- Check: `Par` overloads `f(int)`, `Mid` defines `f` plainly, `Leaf`
  overloads `f(str)`; call `Leaf().f('a')` and `Leaf().f(1)`.
- Outcome: **By design.** `'str'` and `DispatchException` for the
  `int` call: the plain `Mid.f` is shadowed by `Leaf`'s dispatcher, and
  `Par`'s `int` signature is not collected. This matches the
  `BaseSpace` docstring, but it is the one place where overloading in a
  subclass removes behaviour a parent provided.
- Recommendation [note]: mention in the `overload` docstring that
  overloading a name a plain method in between defines discards both
  the plain method and the overloads beyond it; a user wanting the
  plain behaviour kept registers it as the fallback.

### M9. Routed hook bound without `@classmethod`

- Check: `def __class_len__(cls)` in a body.
- Outcome: **Confirmed, by design.** `UnboundClassHook` at the line.
- Recommendation: none.

### M10. Every subclass gets its own `Dispatcher` for inherited names

- Check: `Q(P)` with no body of its own, where `P` overloads `f`.
- Outcome: **Confirmed, by design.** `'f' in Q.__dict__` and the object
  differs from `P.__dict__['f']`. Each subclass compiles its own
  dispatch closure on first call, so a deep hierarchy with many
  overloaded names pays one compile per name per class.
- Recommendation [note]: acceptable; worth a line in the `BaseSpace`
  docstring, which only says "one is built for every inherited name".

### M11. Hook order on `BaseSpace`

- Outcome: **Confirmed, by design.** `ReservedNamespaceHook`,
  `NamespaceHook`, `LoadSpaceHook`.
- Recommendation: none.

### M12. Keys `compile` adds to every class

- Check: a class declared with `trustMeBro=False`.
- Outcome: **Observation.** `__metaclass__`, `__namespace__` and
  `__keyword_arguments__` are class attributes of every class built by
  these metaclasses; `__keyword_arguments__` records the keywords
  verbatim, including `_strictMRO` when given.
- Recommendation: none.

### M13. Overload and plain definition in one body, duplicate signatures

- Check: overload then plain `f`; `@overload(int)` twice on `f`
  with a different body.
- Outcome: **Confirmed, by design.** `OverloadConflict` and
  `DuplicateSignature`, each at class creation with a clear message.
- Recommendation: none.

### M14. `getNamespaceClass` runs the prepare phase

- Check: `BaseMeta.getNamespaceClass()`.
- Outcome: **Observation.** It builds a throwaway `BaseSpace('_', ())`,
  so every hook's `preparePhase` runs for a class that never exists.
  Harmless today, since no hook's `preparePhase` has side effects.
- Recommendation [note]: a hook with a side-effecting `preparePhase`
  would need this to be rewritten to inspect the return annotation or
  a class attribute instead.

### M15. Class-level hooks: iteration fallbacks

- Check: a class with `__class_iter__` only; `list`, `len`, `bool`,
  `in`.
- Outcome: **Confirmed, by design.** `[1, 2, 3]`, `3`, `True`, `True`.
- Recommendation: none.

### M16. Two hand-maintained lists of routed hooks

- Reasoning: `NamespaceHook._getClassDunders` lists the seventeen routed
  names and `AbstractMetaclass` implements the same seventeen; nothing
  ties the lists together.
- Check: compared the two lists by reading; they match today.
- Outcome: **Observation.**
- Recommendation [low, test]: a test asserting that every name in
  `_getClassDunders` has its operation implemented on
  `AbstractMetaclass` and the reverse, so a hook added on one side only
  fails in CI.

### M17. `AbstractMetaclass` docstring misstates the default hash

- Reasoning: the docstring shows `__class_hash__` hashing
  `clsName.__bases__` directly; the implementation drops `object` and
  every base flagged `__skip_hash__`.
- Check: `hash(A) == hash(('A', 'BaseObject', 'BaseMeta'))` for
  `A(BaseObject)`, whose bases include `_Chill` through `Object`.
- Outcome: **Confirmed.** Docstring only.
- Recommendation [low, docstring]: show the rule as implemented.

### M18. One hook object serves every namespace of its class

- Reasoning: `AbstractSpaceHook.__get__` rebinds `__space_object__` on
  each access, and `AbstractNamespace` rebinds before every phase call.
  A hook method that itself executes a class statement using the same
  namespace class would return to a hook bound to the inner namespace.
- Check: by reading; nothing in the library runs a class statement
  from inside a phase.
- Outcome: **Observation.** Safe for the library's own hooks.
- Recommendation [note]: a sentence in the `AbstractSpaceHook`
  docstring, or binding the namespace as an argument of each phase
  instead of as state on the hook, if third-party hooks are expected.

### M19. Thread safety

- Reasoning: the `Object` context stack lives on the descriptor and the
  hook binding lives on the hook, both shared process-wide.
- Outcome: **Observation.** `Object` documents the limitation; the hook
  binding is only exercised during class statements, which hold the
  import lock in practice.
- Recommendation: none beyond the existing docstring.

---

## Summary of recommendations

| # | Severity | Item | Recommendation |
|---|---|---|---|
| D10 | medium | `Dispatcher.addVariadicSigFunc` | Refuse a signature without a trailing `ARGS` at registration instead of failing with `AttributeError` at the first call. |
| E2 | medium | `AttriBox._applyTags` | Rename the tags so a built `Object` value is not marked as placed; `hasattr(value, 'instance')` currently raises `WithoutException`. |
| E3 | medium | `AttriBox._refuseStorageCollision` | Check the owner's MRO, or derive collision-free storage names; a parent `fooBar` and a child `foo_bar` share one slot silently. |
| C1 | low | `MetaType` | Document that every class keeps its namespace under `__namespace__`. |
| C3 | low | `_AnnotationsDescriptor` | Correct or drop the method docstrings. |
| C5 | low | `Object.getContextInstance` / `getContextOwner` | Remove the unreachable `is None` branches. |
| C7 | low | `ControlSpace.__setitem__` | Report an annotation in a signal body as such, not as `__annotations__` or `__annotate_func__`. |
| C9 | low | `ARGS.__iter__` | Say that it exists for `@overload(str, *ARGS[int])`. |
| C10 | low | `_MetaARGS.__call__` | Fix the return annotation. |
| C14 | low | `Object._deletedGuard` | Pass `self`, not the instance, as the subject of the missing field name. |
| D1 | low | `flexCall` | Leave `self` out of the missing-arguments list. |
| D2 | low | `Dispatcher.overload` | Refuse unknown keywords as `overload` does. |
| D3 | low | `overload.flex` / `Permuter` | Accept any callable, or refuse non-functions in `flex` with a message naming the decorator. |
| D11 | low | `TypeSig.__call__` | Name `LoadSpaceHook`, not `Dispatcher._copySig`, as the caller. |
| D12 | low | `TypeSig` | `HASHABLE` should be `Union[type, ARGS]`. |
| E1 | low | `FastBox` | Raise `MissingInstanceDict` for a `__slots__`-only owner. |
| E5 | low | `AttriBox._callFieldType` | Name the field and describe an empty argument list honestly. |
| E6 | low | `BaseDescriptor._getCallback` | Cache the flex wrapper of an undecorated override. |
| E7 | low | `BaseDescriptor.hookSetName` | Route through `_getCallback` for the flex treatment. |
| E12 | low | `AttriBox` docstring | The `THIS`-with-base-type refusal does not apply to `BaseObject` field types. |
| M16 | low | tests | Tie `NamespaceHook._getClassDunders` to the operations `AbstractMetaclass` implements. |
| M17 | low | `AbstractMetaclass` docstring | Show the hash rule as implemented. |
| C8, D13, E4, E16, M1, M8, M10, M14, M18 | note | various | Observations recorded above; no action required. |

Refuted suspicions, for the record: C2 (duplicate `_Chill`), C8
(double root record), C9 (unused `ARGS.__iter__`), C13 (owner frames)
and E4 (text/number asymmetry). All five were worth checking and none
is a defect.

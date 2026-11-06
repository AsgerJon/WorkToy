# Research notes: the non-leaf packages of worktoy

Read order: `core` (MetaType, sentinels, control_flow, ContextInstance,
ContextOwner, Object), then `dispatch`, `desc` and `mcls`, following the
import order of each `__init__.py`. Support packages (`utilities`,
`waitaminute`) are inspected ad hoc and are recorded only inside the
entry of the non-leaf item that relies on them. They never get their own
entry.

Every entry has the same shape so that `structure_map.html` can be built
from this file alone:

```
### <Item>
- package: <core | dispatch | desc | mcls>
- module: <module path relative to src/worktoy>
- kind: <class | metaclass | sentinel | signal | function | descriptor | namespace | hook>
- bases: <comma separated items this class is based on (non-leaf only), or none>
- metaclass: <non-leaf metaclass the class is derived from, or none>
- uses:
  - <Target> | <short verb phrase> | <one or two sentences on what the use is for>
- support: <utilities / waitaminute items relied upon, with what for>
- description: <prose>
- interactions: <prose on how it fits with the rest of the non-leaf packages>
```

`bases` lines become "based on" edges, `metaclass` lines become
"metaclass" edges and `uses` lines become "other use" edges. A target
named in `uses` that is not an item of the four packages is not an edge.

---

### _AnnotationsDescriptor
- package: core
- module: core/_annotations_descriptor.py
- kind: descriptor
- bases: none
- metaclass: none
- uses: none
- support: `utilities.maybe` picks `owner` over `type(cls)` in `__get__`.
- description: Private data descriptor that `MetaType.__new__` installs
  at `__annotations__` on any metaclass whose own body carries
  annotations (only when `HAS_TYPE_ANNOTATIONS`, i.e. Python 3.10+ where
  `type.__dict__['__annotations__']` exists). Without it, the eager dict
  left behind by `from __future__ import annotations` on the metaclass
  would shadow `type`'s descriptor, so a class annotating nothing would
  answer with the annotations of a base. `__get__` with `cls is None`
  returns the metaclass's own stored dict; otherwise it defers to the
  getset descriptor of `type` so the class answers for itself. `__set__`
  and `__delete__` forward to the same getset descriptor. `__objclass__`
  is set to `type` so it looks like a native slot. The module also
  exports `HAS_TYPE_ANNOTATIONS` and `typeAnnDesc`.
- interactions: Used only by `MetaType.__new__`. Every metaclass in the
  library (`SentinelMeta`, `_MetaARGS`, `MetaFlow`, `AbstractMetaclass`,
  `BaseMeta`) is built by `MetaType`, so any of them with annotated class
  variables (for example `MetaFlow.__is_root__: bool`) gets this
  descriptor transparently.

### _Chill
- package: core
- module: core/_meta_type.py
- kind: class
- bases: none
- metaclass: none
- uses: none
- support: none
- description: Private terminal base that `MetaType.__new__` appends to
  the bases of every class whose last base is not already a `MetaType`
  instance. It declares `__skip_hash__ = True` as a class attribute and a
  classmethod `__init_subclass__(**kwargs)` that accepts and swallows
  arbitrary class keywords, then sets `__skip_hash__ = False` on the new
  subclass via `type.__setattr__`. Because it is always last in the MRO
  before `object`, the `__init_subclass__` chain ends here, so a class
  statement with custom keywords (such as `_root=True` on `ControlFlow`)
  never reaches `object.__init_subclass__` which would refuse them.
- interactions: Implicit base of every class built by `MetaType` or any
  metaclass derived from it: every `Sentinel`, every `ControlFlow`
  signal, every `AbstractMetaclass`/`BaseMeta` class and `BaseObject`
  itself. The `__skip_hash__` flag it toggles is read by
  `AbstractMetaclass` (see that entry) to decide whether a class is
  eligible for metaclass-level hashing.

### MetaType
- package: core
- module: core/_meta_type.py
- kind: metaclass
- bases: none
- metaclass: none
- uses:
  - _AnnotationsDescriptor | installs | `__new__` wraps a metaclass body's `__annotations__` dict in this descriptor so classes of the metaclass answer for their own annotations.
  - _Chill | appends as base | `__new__` adds `_Chill` as the last base when the last base is not itself a `MetaType`, so class keywords are absorbed by `_Chill.__init_subclass__`.
- support: none
- description: The meta-metaclass of the whole library; subclasses
  `type` directly. `__str__`/`__repr__` render as `Name[metaclass=Meta]`.
  `__new__(mmcls, name, bases, space, **kw)`: (1) appends `_Chill` when
  the last base is not a `MetaType` instance, (2) strips `object` from
  the bases, (3) if `HAS_TYPE_ANNOTATIONS` and the body has
  `__annotations__` and any base is a subclass of `type` (i.e. the class
  being created is itself a metaclass), replaces that dict with
  `_AnnotationsDescriptor`, (4) temporarily inserts
  `space['__namespace__'] = space` before calling `type.__new__` and
  removes it afterwards unless the namespace already carried one. Thus
  during class creation the namespace object is reachable from the class
  body as `__namespace__`. `__init__` sets `__skip_hash__ = False` on
  the created class.
- interactions: `SentinelMeta`, `_MetaARGS` (via `SentinelMeta`),
  `MetaFlow`, `AbstractMetaclass` and `BaseMeta` all subclass `MetaType`
  *and* declare `metaclass=MetaType`, so all worktoy metaclasses share a
  common meta-metaclass and never raise a metaclass conflict when
  combined. `MetaType` is also what makes the `__namespace__` key
  available to `AbstractNamespace`/`BaseSpace` consumers. Only
  `_MetaSlice` in `utilities` subclasses `type` directly instead.

### SentinelMeta
- package: core
- module: core/sentinels/_sentinel.py
- kind: metaclass
- bases: MetaType
- metaclass: MetaType
- uses: none
- support: `utilities.maybe` defaults the registry to `[]`;
  `waitaminute.meta.IllegalInstantiation` (a `TypeError`) is raised from
  `__call__`; `waitaminute.meta.DuplicateSentinel` (a `TypeError`) is
  raised from `__new__` for a second class statement at a registered
  name.
- description: Metaclass for sentinel classes. Keeps one process-wide
  registry `SentinelMeta.__registered_sentinels__` (shared by all
  subclasses of `SentinelMeta`, accessed via `_getRegisteredSentinels`,
  `_getNamedSentinel`, `_registerSentinel`). `__prepare__` returns a
  plain dict. `__new__` refuses a name already registered with
  `DuplicateSentinel(name, existing, module)`, otherwise builds and
  registers the class. `__call__` always raises `IllegalInstantiation`,
  so sentinels are never instantiated. `__hash__` hashes the tuple of
  metaclass module/name and class module/name. `__str__`/`__repr__`
  render `<Sentinel: 'NAME'>`.
- interactions: Built by `MetaType`, so a sentinel declared with a class
  keyword has it absorbed by `_Chill`. `Sentinel` and every concrete
  sentinel (`DELETED`, `OWNER`, `THIS`, `DESC`, `METACALL`) is an
  instance of it; `_MetaARGS` subclasses it to make `ARGS` instantiable.
  The identity-only nature of sentinels is what `Object`, `AttriBox` and
  `TypeSig`/`Dispatcher` rely on when they compare with `is`.

### Sentinel
- package: core
- module: core/sentinels/_sentinel.py
- kind: sentinel
- bases: none
- metaclass: SentinelMeta
- uses: none
- support: none
- description: The root sentinel class (`class Sentinel(metaclass=
  SentinelMeta)`), with no body beyond its docstring. It exists so that
  concrete sentinels can subclass it and so `isinstance(x, Sentinel)` /
  `issubclass` style checks can identify sentinel classes.
- interactions: Base of `DELETED`, `OWNER`, `THIS`, `DESC`, `METACALL`.
  `ARGS` is not based on it; it only shares the metaclass family.

### DELETED
- package: core
- module: core/sentinels/_deleted.py
- kind: sentinel
- bases: Sentinel
- metaclass: SentinelMeta
- uses: none
- support: none
- description: Marks a descriptor slot as deleted. Instead of threading
  deletion through the three lookups a descriptor performs (instance
  value, descriptor default, descriptor-class fallback), the descriptor
  stores `DELETED` in the instance slot and the next read raises
  `MissingVariable`.
- interactions: Written by `Object.__delete__` /
  `__instance_delete__` family and read back by `Object.__get__` and the
  `desc` boxes (`AttriBox`, `FastBox`, `Field`) which check for it before
  returning a value.

### OWNER
- package: core
- module: core/sentinels/_owner.py
- kind: sentinel
- bases: Sentinel
- metaclass: SentinelMeta
- uses: none
- support: none
- description: Placeholder for the `owner` class passed to `__get__`.
  Used in deferred `AttriBox` constructor arguments, where it is
  replaced at access time by the owning class. Plays no role in overload
  signatures.
- interactions: Substituted by `AttriBox` when it builds the field value
  for an instance.

### THIS
- package: core
- module: core/sentinels/_this.py
- kind: sentinel
- bases: Sentinel
- metaclass: SentinelMeta
- uses: none
- support: none
- description: Placeholder for the enclosing class used inside a class
  body before that class exists. In deferred `AttriBox` arguments it is
  replaced by the accessing instance; in an `@overload` signature it
  stands for the class being defined (like `typing.Self`).
- interactions: Substituted by `AttriBox` at access time, and resolved by
  `TypeSig`/`Dispatcher`/`overload` in `dispatch` and by `BaseMeta` in
  `mcls`, which replace it with the class once that class exists.

### DESC
- package: core
- module: core/sentinels/_desc.py
- kind: sentinel
- bases: Sentinel
- metaclass: SentinelMeta
- uses: none
- support: none
- description: Placeholder for the descriptor object itself in deferred
  `AttriBox` constructor arguments; replaced at access time by the
  descriptor mediating the access.
- interactions: Substituted by `AttriBox` alongside `THIS` and `OWNER`.

### METACALL
- package: core
- module: core/sentinels/_meta_call.py
- kind: sentinel
- bases: Sentinel
- metaclass: SentinelMeta
- uses: none
- support: none
- description: Marks a class-level dunder hook (such as `__class_str__`
  or `__class_iter__`) as deferred to the metaclass implementation.
- interactions: `AbstractMetaclass` checks whether a hook value `is
  METACALL` and then falls back to its own implementation instead of
  calling the hook on the class.

### _MetaARGS
- package: core
- module: core/sentinels/_args.py
- kind: metaclass
- bases: SentinelMeta
- metaclass: MetaType
- uses: none
- support: none
- description: Metaclass of `ARGS`. Inherits registration and duplicate
  refusal from `SentinelMeta` but overrides `__call__(cls, type_)` to
  create an instance via `type.__call__` and store `type_` on it as
  `__inner_type__`, so `ARGS`, unlike the other sentinels, can be
  instantiated.
- interactions: Only used to build `ARGS`.

### ARGS
- package: core
- module: core/sentinels/_args.py
- kind: sentinel
- bases: none
- metaclass: _MetaARGS
- uses: none
- support: none
- description: Placeholder for a starred (variadic) argument in an
  overload signature. `ARGS[int]` (via `__class_getitem__`) calls the
  metaclass and returns a new instance holding `int` as
  `__inner_type__`. Instances are iterable (yield themselves), compare
  equal when their inner types are identical, hash on
  `(type name, inner type)`, and render as `ARGS[int]`.
- interactions: Consumed by `TypeSig` in `dispatch` to mark the variadic
  tail of a signature, and by `Dispatcher`/`overload` when matching call
  arguments against signatures. Equality by inner type lets a subclass
  variadic signature be recognised as equal to the one it overrides.

### ControlSpace
- package: core
- module: core/control_flow/_control_space.py
- kind: namespace
- bases: none
- metaclass: none
- uses: none
- support: `utilities.maybe` defaults the white list and the root flag;
  `waitaminute.meta.ControlClassError` (a `TypeError`) is raised from
  `__setitem__` for a disallowed attribute, and reads
  `space.__metaclass__` and `space.__class_name__` to render its message.
- description: A `dict` subclass used as the class-body namespace of
  control-flow signals. Stores the metaclass, bases, class name and an
  `__is_root__` flag (from the `_root` class keyword) and puts itself at
  `self['__namespace__']`. `__setitem__` allows white-listed keys
  (`__firstlineno__`, `__str__`, `__repr__`, `__namespace__`,
  `__static_attributes__`, `__classcell__`, `__classdictcell__`); for a
  non-root class every other key must be a non-callable attribute that
  `Exception` already holds (e.g. `__doc__`, `__module__`), otherwise
  `ControlClassError` is raised. The root class is exempt.
- interactions: Created and returned by `MetaFlow.__prepare__`. It is a
  sibling of `AbstractNamespace`/`BaseSpace` in `mcls` in role (a
  namespace object with a metaclass back-reference) but shares no code.

### MetaFlow
- package: core
- module: core/control_flow/_meta_flow.py
- kind: metaclass
- bases: MetaType
- metaclass: MetaType
- uses:
  - ControlSpace | prepares as namespace | `__prepare__` builds a `ControlSpace` for every signal so the class body is validated as it executes.
- support: `waitaminute.VariableNotNone` is raised by `_registerRoot` if
  a second root is registered.
- description: Metaclass of the control-flow signals. Keeps one root
  class in `MetaFlow.__root_cls__` (`getRootClass`, `_registerRoot`).
  `__prepare__` creates a `ControlSpace`, pre-installs `__str__` and
  `__repr__` from `_strFactory()` (an instance `__str__` that returns
  `str(type(self))`) and stores the `_root` keyword as `__is_root__`.
  `__new__` builds the class through `MetaType.__new__` and registers it
  as root if `__is_root__`. `__str__` renders `<Root: [Root]>` or
  `<Root: Name>`.
- interactions: Built by `MetaType` so the `_root=True` keyword used by
  `ControlFlow` is absorbed by `_Chill`. `ControlFlow` and `SkipSet` are
  its instances.

### ControlFlow
- package: core
- module: core/control_flow/_control_flow.py
- kind: signal
- bases: none
- metaclass: MetaFlow
- uses: none
- support: none
- description: `class ControlFlow(Exception, metaclass=MetaFlow,
  _root=True)`. The root signal: an exception raised to steer a protocol
  rather than to report a failure. Registered as the root with
  `MetaFlow._registerRoot`.
- interactions: Base of `SkipSet`. `Object.__set__` catches subclasses of
  this family; `mcls`/`desc` hook code may raise them.

### SkipSet
- package: core
- module: core/control_flow/_skip_set.py
- kind: signal
- bases: ControlFlow
- metaclass: MetaFlow
- uses: none
- support: none
- description: The one signal the library raises itself. Raised from a
  descriptor's `hookPreSet` to tell `Object.__set__` to skip
  `__instance_set__` and `hookOnSet` entirely; the caller sees no
  exception. Recommended only for redundant-set elision.
- interactions: Caught by `Object.__set__` in `core`; raised by
  descriptor subclasses in `desc` (and user code) from their
  `hookPreSet`.

### ContextInstance
- package: core
- module: core/_instance_owner.py
- kind: descriptor
- bases: none
- metaclass: none
- uses:
  - Object | reads context of | `__get__` on an `Object` instance returns `instance.getContextInstance()`, the top-of-stack instance of that descriptor's context.
- support: none
- description: Tiny non-data descriptor. Accessed on the class it returns
  itself; accessed on an `Object` instance it returns the currently
  active contextual instance by calling `getContextInstance()`, which
  raises `WithoutException` when no context frame is active.
- interactions: Placed as `Object.instance`, so every descriptor in
  `desc`, `dispatch` and `mcls` that subclasses `Object` can write
  `self.instance` inside its hooks.

### ContextOwner
- package: core
- module: core/_instance_owner.py
- kind: descriptor
- bases: none
- metaclass: none
- uses:
  - Object | reads context of | `__get__` on an `Object` instance returns `instance.getContextOwner()`, the top-of-stack owner class.
- support: none
- description: Twin of `ContextInstance` for the owner class: returns
  itself on class access and `instance.getContextOwner()` on instance
  access.
- interactions: Placed as `Object.owner`; read as `self.owner` from
  descriptor hooks throughout `desc` and `mcls`.

### Object
- package: core
- module: core/_object.py
- kind: class
- bases: none
- metaclass: MetaType
- uses:
  - ContextInstance | exposes as `instance` | The class attribute `instance = ContextInstance()` lets hooks read the active instance as `self.instance`.
  - ContextOwner | exposes as `owner` | The class attribute `owner = ContextOwner()` lets hooks read the active owner as `self.owner`.
  - SkipSet | catches | `__set__` catches `SkipSet` raised by `hookPreSet` and then skips `__instance_set__` and `hookOnSet`, so the write is silently elided.
  - DELETED | translates | `_deletedGuard` turns a `DELETED` value returned by `__instance_get__` into `MissingVariable`, so a deleted attribute reads as absent.
  - THIS | substitutes | `getContextualSentinels`/`filterSentinels` replace `THIS` in captured constructor args with the contextual instance.
  - OWNER | substitutes | `getContextualSentinels`/`filterSentinels` replace `OWNER` in captured constructor args with the contextual owner class.
  - DESC | substitutes | `getContextualSentinels`/`filterSentinels` replace `DESC` in captured constructor args with the descriptor itself.
  - Sentinel | types the mapping | `getContextualSentinels` is annotated as returning `dict[Type[Sentinel], Any]`; the sentinel identity semantics are what make the `is` comparisons in `hasSentinelArgs` sound.
- support: `utilities.Directory` is placed as the class attribute
  `directory` (read-only descriptor giving the owner module's source
  directory); `utilities.maybe` is used for defaults throughout;
  `waitaminute.MissingVariable` (an `AttributeError`) is raised for
  deleted values and missing field names; `waitaminute.TypeException`
  is raised by `getPrivateName` and `parseKwargs`;
  `waitaminute.desc.WithoutException` (a `RuntimeError`) is raised when
  context is read outside a frame or `exitContext` is unpaired;
  `waitaminute.desc.ReadOnlyError` is the default `__instance_set__`
  refusal and `waitaminute.desc.ProtectedError` the default
  `__instance_delete__` refusal (both `AttributeError`s).
- description: The most primitive base class of the library and a full
  data descriptor. State: `__field_owner__`, `__field_name__`,
  `__private_name__` (cache), `__pos_args__`, `__key_args__` (the
  constructor arguments captured by `__init__`, used later by the boxes)
  and `__call_chain__` (the per-descriptor stack of `(instance, owner)`
  frames). `__init__` stores args/kwargs and an empty chain through
  `object.__setattr__` so a subclass `__setattr__` is bypassed.
  `__set_name__` records owner and name and calls `hookSetName`.
  `__get__` returns self on class access; otherwise pushes a frame,
  runs `hookPreGet`, `__instance_get__`, `_deletedGuard`, `hookOnGet`
  and pops in `finally`. `__set__` pushes a frame, runs `hookPreSet`
  (catching `SkipSet`), `__instance_set__` and `hookOnSet` with the
  stored value (or the assigned one if `None` was returned).
  `__delete__` reads the old value with `_deleting=True`, then
  `hookPreDelete`, `__instance_delete__(instance, old)`, `hookOnDelete`.
  The defaults are: get returns self, set raises `ReadOnlyError`, delete
  raises `ProtectedError`, so a plain worktoy value in a class body is a
  shared read-only class attribute. `createContext`/`exitContext`/
  `hasContext`/`getContextInstance`/`getContextOwner` are the public
  context API. `getPrivateName` converts `fooBar` to `__foo_bar__` with a
  precompiled regex and caches it. `getPosArgs`/`getKeyArgs` return the
  captured constructor arguments with sentinels substituted;
  `hasSentinelArgs` says whether any captured arg is `THIS`/`OWNER`/
  `DESC`. The classmethod `parseKwargs(*args, **kwargs)` pulls the
  first present key among the given string keys whose value matches any
  given type (number types widened: complex admits float and int, float
  admits int) and returns `(value, remaining kwargs)`, raising
  `TypeException` on a mismatch. Not thread-safe by design.
- interactions: The root of nearly everything: `BaseDescriptor`,
  `FastBox`, `_RootAlias`, `Alias`, `Field`, `AttriBox`, `SymbolicName`
  in `desc`; `Dispatcher`, `overload` and `CallMeMaybe` in `dispatch`;
  `AbstractSpaceHook` in `mcls.space_hooks`; and `BaseObject` in `mcls`
  all derive from it (some override `__get__`/`__set__` wholesale and
  use only the `__set_name__` bookkeeping). The boxes in `desc` build on
  the captured args and sentinel substitution; `Dispatcher` relies on
  the field name/owner. Being a `MetaType` class, it also has `_Chill`
  appended and `__skip_hash__` set.

### flexCall
- package: dispatch
- module: dispatch/_flex_call.py
- kind: function
- bases: none
- metaclass: none
- uses:
  - isFlex | shares marker with | Both read the `__flex_wrapped__` attribute; `flexCall` sets it on the wrapper and returns an already-marked function unchanged.
- support: `utilities.joinWords` and `utilities.textFmt` format the
  missing-arguments message; `waitaminute.TypeException` is raised when
  `func` is not a `types.FunctionType`.
- description: Wraps a plain function with truncating positional-argument
  dispatch. Returns `func` unchanged when it is already flex-wrapped,
  when it takes `*args` (`co_flags & 0x04`), or when it is a dunder.
  Otherwise caches `maxPos = co_argcount`, `minPos = co_argcount -
  len(defaults)` and the required names in closure cells, and returns a
  `wrapper(*args, **kwargs)` that: raises a plain `TypeError` when a
  required positional parameter receives no value by position or
  keyword (`_missingNames` helper), truncates positional args beyond
  `maxPos`, and passes keywords through. The wrapper copies `__dict__`,
  `__name__`, `__qualname__`, `__module__`, `__doc__`,
  `__annotations__`, sets `__wrapped__` and the `__flex_wrapped__`
  marker.
- interactions: `BaseDescriptor` in `desc` wraps its notification
  callbacks with `flexCall` so a callback may declare fewer parameters
  than the descriptor passes. `FlexCallHook` in `mcls.space_hooks`
  applies it to every plain function in a class body whose namespace
  declares the hook.

### isFlex
- package: dispatch
- module: dispatch/_flex_call.py
- kind: function
- bases: none
- metaclass: none
- uses: none
- support: none
- description: Returns True when `func` carries the `__flex_wrapped__`
  marker set by `flexCall`, i.e. it has already been wrapped.
- interactions: Companion predicate for `flexCall`; used by code that
  must not double wrap (`FlexCallHook`, `BaseDescriptor`).

### _Wrapped
- package: dispatch
- module: dispatch/_call_me_maybe.py
- kind: descriptor
- bases: none
- metaclass: none
- uses: none
- support: Subclasses `utilities.QuickDesc` (a minimal descriptor that
  reads a private attribute named at construction); raises
  `waitaminute.MissingVariable` and `waitaminute.TypeException` on a
  missing or wrongly typed private key or stored tuple.
- description: Private generic descriptor (`QuickDesc, Generic[T]`)
  placed as `CallMeMaybe.__wrapped__`. On class access returns itself;
  on instance access reads the one-tuple stored at the private key
  (`__function_case__`) and returns its first element, the wrapped
  function.
- interactions: Only used inside `CallMeMaybe`, and transitively by
  `Permuter`, `PermuterMethod` and the `overload` machinery via
  `CallMeMaybe.__wrapped__`.

### CallMeMaybe
- package: dispatch
- module: dispatch/_call_me_maybe.py
- kind: class
- bases: none
- metaclass: none
- uses:
  - _Wrapped | exposes function through | The class attribute `__wrapped__ = _Wrapped('__function_case__')` reads the stored function out of its one-tuple without method binding.
- support: `utilities.textFmt` formats the `__set_name__` refusal;
  `utilities.QuickDesc` is the base of `_Wrapped`;
  `waitaminute.MissingVariable` is raised when no function is stored;
  `waitaminute.TypeException` when the constructor argument is not
  callable.
- description: Minimal callable indirection: holds one function in
  `__function_case__ = (func,)` (a one-tuple so `FunctionType.__get__`
  never binds it) and forwards `__call__(*args, **kwargs)` to
  `invoke(func, *args, **kwargs)`, which subclasses override to
  transform the call. `setFunction` stores the tuple;
  `_getWrappedFunction` unwraps it. It deliberately has no `__get__`;
  `__set_name__` always raises `TypeError` so it cannot be used as a
  class attribute. `__getattr__` forwards unknown attributes to the
  wrapped function.
- interactions: Base of `Permuter` (and so `PermuterMethod`). Used by
  the `overload.flex` machinery in `dispatch` as a non-descriptor
  callable so descriptor binding does not interfere with dispatch.

### Permuter
- package: dispatch
- module: dispatch/_permuter.py
- kind: class
- bases: CallMeMaybe
- metaclass: none
- uses:
  - CallMeMaybe | overrides invoke of | `invoke` restores the received positional args to canonical order through the `Arrangement` before calling the wrapped function; `super().__init__(func)` stores the function.
- support: `utilities.combinatorics.Arrangement` describes the
  permutation and performs `restoreFrom(*args)`; `utilities.QuickDesc`
  exposes `arrangement`; `utilities.textFmt` formats constructor
  errors; `waitaminute.TypeException` for wrong argument types,
  `waitaminute.MissingVariable` when no arrangement is set,
  `waitaminute.desc.WriteOnceError` when an arrangement is set twice.
- description: A `CallMeMaybe` holding an `Arrangement`
  (`__arg_arrangement__`, write-once through `setArrangement`). The
  constructor accepts at most two positional args, a function and/or an
  `Arrangement`, in any order, raising `ValueError` for duplicates and
  `TypeException` otherwise. `newArrangement(original, arrangement)`
  builds a new `Permuter` over the same function. Operators: `p <<
  arrangement` returns a new permuter, `p <<= arrangement` sets it in
  place, `arrangement >> p` mirrors `<<`. `invoke` calls
  `func(*arrangement.restoreFrom(*args), **kwargs)`.
- interactions: Base of `PermuterMethod`. The `Dispatcher` and
  `overload` machinery use permuters to accept arguments in any of the
  permuted orders of a signature (`overload.flex` style) and reorder
  them to the canonical order of the implementation.

### PermuterMethod
- package: dispatch
- module: dispatch/_permuter_method.py
- kind: class
- bases: Permuter
- metaclass: none
- uses:
  - Permuter | overrides invoke of | `invoke(func, instance, *args)` forwards the bound instance first and then the arguments restored by the arrangement, so a method can be wrapped.
- support: none beyond what `Permuter` uses.
- description: A `Permuter` whose `invoke` takes the calling instance
  as the first positional argument, forwards it untouched, and permutes
  only the remaining positional arguments.
- interactions: Used by `Dispatcher`/`overload` when the overloaded
  callable is a method and the instance must stay in front of the
  reordered arguments.

### TypeSig
- package: dispatch
- module: dispatch/_type_sig.py
- kind: class
- bases: none
- metaclass: none
- uses:
  - THIS | substitutes and detects | `namesTHIS` reports a `THIS` entry, `swapTHIS` replaces it in place with the finished class, `restoreTHIS` puts it back, and `__call__(this=...)` returns a substituted copy.
  - OWNER | refuses and substitutes | `validateTypes` raises `TypeError` for an `OWNER` entry since it has no meaning in a signature, while `__call__(owner=...)` can still substitute it in a copy.
  - ARGS | marks variadic tail | A trailing `ARGS[T]` entry is accepted by `validateTypes` (unless `variadic=False`), compared by inner type in `__eq__`, rendered by `_getTypeName`, and rebuilt as `ARGS[cls]` by `swapTHIS`.
- support: `utilities.textFmt` formats messages;
  `waitaminute.TypeException` is raised by `validateTypes` for a
  non-class entry.
- description: Hashable, ordered tuple of types used as the dispatch
  key of a single overload. Keeps `__raw_types__` (what it dispatches
  on) beside `__declared_types__` (what it was declared with) and a
  class-level `__allow_flex__` flag (default True) that tells the
  dispatcher's slow path whether `typeCast` conversions may be tried;
  `overload.flex`/`Dispatcher.flex` set it False on generated
  signatures, and so do `overload`/`Dispatcher.overload` on any
  signature naming `THIS` unless `strict=False`. `fromArgs(*args)`
  builds the key of an incoming call from the argument types.
  `validateTypes(*types, variadic=True)` refuses entries whose type is
  not a metaclass, `OWNER`, and entries `isinstance` cannot use.
  Iterable, `len`, `in` (identity), `__hash__` on the raw tuple,
  `__eq__` by identity per entry with trailing `ARGS` compared by inner
  type. `__str__` renders `<TypeSig: [int, ARGS[str]]>`, `__repr__`
  `TypeSig(int, str)`. `__call__(this, owner)` returns a substituted
  copy preserving `__allow_flex__`; `Dispatcher._copySig` relies on a
  bare call copying.
- interactions: Created by `overload` as decorators run inside a class
  body (hashing through the `THIS` sentinel until the class exists);
  `Dispatcher` compiles lookup tables keyed by swapped signatures,
  calls `fromArgs` on each call, and uses `swapTHIS`/`restoreTHIS` so a
  clone of a placed dispatcher can resolve `THIS` to its own owner.
  `BaseMeta` in `mcls` triggers the swap once the class is built.

### Dispatcher
- package: dispatch
- module: dispatch/_dispatcher.py
- kind: descriptor
- bases: Object
- metaclass: MetaType
- uses:
  - Object | overrides protocol of | Subclasses `Object` but replaces `__get__`, `__set__`, `__delete__` and `__set_name__` wholesale, keeping only the `__field_name__`/`__field_owner__` bookkeeping and `getFieldOwner`/`getFieldName`; the context stack and notification hooks are out of play.
  - TypeSig | keys registrations by | Every registration is a `(TypeSig, func)` pair; `TypeSig.fromArgs` builds the lookup key per call, `validateTypes` guards `overload`/`flex`, `swapTHIS`/`restoreTHIS` are driven by `swapAllTHIS`/`restoreTHIS`, and `_copySig` duplicates signatures for `clone`.
  - PermuterMethod | wraps flex functions in | `flex(*types)` registers one `PermuterMethod(func, arrangement)` per unique arrangement so a call in any order is restored to canonical order; `_getKeywordBindings` unwraps it to read the canonical parameter names.
  - ARGS | detects variadic signatures by | `overload` routes a signature whose last entry is an `ARGS` instance to `addVariadicSigFunc`; the dispatch tables read `ARGS.__inner_type__` for the tail type.
  - THIS | resolves | `_resolveTHIS` swaps `THIS` for the owner when a signature is registered after placement; `_getKeywordBindings` maps `THIS` in a flex arrangement to the owner; `overload` defaults `strict` to `namesTHIS`.
- support: `utilities.maybe` for defaults; `utilities.typeCast` performs
  the SLOW pass conversions (with `allowInstantiation=False` when a
  constructor would re-dispatch its own sole argument);
  `utilities.textFmt` formats `__str__`;
  `utilities.combinatorics.Arrangements` enumerates the unique
  permutations for `flex`; `waitaminute.TypeException` for a non-callable
  fallback/finalizer; `waitaminute.MissingVariable` for an unplaced
  dispatcher or an empty decorator stack; `waitaminute.desc.ReadOnlyError`
  and `ProtectedError` from `__set__`/`__delete__`;
  `waitaminute.dispatch.DispatchException` when no overload matches and
  `waitaminute.dispatch.DuplicateSignature` for a repeated concrete
  signature, fallback or finalizer.
- description: The runtime overload engine. State: `__sig_funcs__`
  (concrete `(sig, func)` list) with `__sig_distances__`,
  `__variadic_funcs__` with `__variadic_distances__`,
  `__fallback_func__`, `__finalizer_func__`, `__compiled_func__` (the
  lazily built dispatch closure) and `__latest_func__` (for decorator
  stacking). Registration: `addSigFunc(sig, func, distance)` (refuses
  equal signatures), `addVariadicSigFunc` (appends; the most recent of
  the nearest class wins), `setFallbackFunction`, `setFinalizerFunction`;
  each invalidates the cache. Decorator API mirroring `overload`:
  `overload(*types, strict=...)`, `flex(*types)`, `fallback(func)`,
  `finalize(func)`; each returns the dispatcher so decorators stack, with
  `_stackedFunction` resolving the one function of a stack.
  `_createCachedFunction` precomputes the exact-type map
  (`_getExactFuncMap`, where a nearer variadic signature can take a
  parent's explicit call), the variadic exact tables keyed by prefix
  length/prefix/inner type (`_getExactVariadics`), the isinstance order
  (nearest first), the cast order (farthest first, `_getCastOrder`,
  `_getVariadicOrder`) and the keyword bindings, then builds
  `dispatch(instance, *args, **kwargs)`: keyword calls go through
  `keywordDispatch` (bind by name, then exact/isinstance/cast tiers);
  positional calls go FASTEST (dict lookup by `TypeSig.fromArgs`, then
  the variadic tables), FAST concrete, FAST variadic, SLOW concrete,
  SLOW variadic, fallback, else `DispatchException`; the finalizer runs
  in `finally` and its exception chains from the in-flight one. The
  closure gets `__name__`, `__qualname__`, `__module__` and the doc of
  the first registration. `__get__` adopts an owner if installed by
  `setattr` (`_adoptOwner`), returns the compiled function on class
  access and a fresh `MethodType` on instance access. `__set_name__`
  records name/owner and `swapAllTHIS(owner)`. `clone()` copies
  registrations with copied signatures, so a clone placed on a subclass
  resolves `THIS` independently (after `restoreTHIS`).
- interactions: `BaseSpace` in `mcls` compiles the `overload` objects
  found in a class body into a `Dispatcher`, registering the body's own
  signatures first and inherited ones with their MRO distance, and
  `BaseMeta` places it on the class so `__set_name__` swaps `THIS`.
  `DispatchException.__str__` reads back `_getDeclaredSigs` and the
  field name/owner. Users of non-`BaseMeta` classes wire a `Dispatcher`
  by hand.

### overload
- package: dispatch
- module: dispatch/_overload.py
- kind: class
- bases: none
- metaclass: none
- uses:
  - TypeSig | records signatures as | `__new__` validates the types and stores a `TypeSig` per decorator with `__allow_flex__` set from `strict` (default `namesTHIS`); `__iter__` yields the `(TypeSig, func)` pairs.
  - ARGS | separates variadic declarations by | `_addSigFunc` puts a signature whose last raw type is an `ARGS` instance into the variadic list instead of the concrete dict.
  - PermuterMethod | wraps flex functions in | `flex(*types)` stores a `PermuterMethod(function, arrangement)` under the signature of each unique arrangement.
- support: `utilities.maybe` for defaults; `utilities.textFmt` for
  `__str__`; `utilities.combinatorics.Arrangements` enumerates the
  permutations for `flex`; `waitaminute.TypeException` refuses a
  staticmethod, classmethod or non-callable; `waitaminute.MissingVariable`
  from `__getattr__` when nothing is registered.
- description: The user-facing decorator, a class with a lowercase name
  whose `__new__` returns a decorator rather than an instance (unless
  `_root=True`). The decorator builds a `TypeSig`, and either extends an
  existing `overload` from the decorator below in the stack
  (`_extendLatest`) or creates a new `overload` holding
  `__sig_func_dict__` (concrete), `__variadic_sig_func_list__`,
  `__latest_func__`, `__fallback_func__` and `__finalizer_func__`.
  Classmethods `flex`, `fallback` and `finalize` add roles to the stack
  via `_stackOn`. `_refuseKeywords` allows only `strict`;
  `_refuseMethodKinds` rejects staticmethod/classmethod/non-callables.
  `__getattr__` forwards to the latest function (or the fallback).
  `__str__` lists every role. It records only; it performs no dispatch.
- interactions: An `overload` instance is what sits in the class
  namespace while the body runs. `BaseSpace` in `mcls` detects these
  values and compiles them into a `Dispatcher` (reading `__iter__`,
  `getVariadics`, `getFallback`, `getFinalizer`), and `BaseMeta` places
  the dispatcher on the class. `AttriBox`/`BaseObject` users write
  `@overload(...)` on `__init__` and friends.

### _RootAlias
- package: desc
- module: desc/_root_alias.py
- kind: class
- bases: none
- metaclass: none
- uses: none
- support: `waitaminute.desc.PhantomBoxError` (a `DescriptorException`)
  is raised from both `__set_name__` and `__get__`.
- description: Private subclass of `typing._GenericAlias` (declared with
  `_root=True`). When a box is subscripted with anything but a plain
  class (a `TypeVar`, or `list[int]`), the generic machinery returns a
  plain alias that a class body would silently store; `fromAlias`
  re-clothes that alias in this class (copying origin, args, `_name`,
  `_inst`) so the stored object's type has a `__get__`. `copy_with` is
  overridden so internal copies (e.g. `TypeVar` substitution) keep the
  class. `__set_name__` raises `PhantomBoxError(self, owner, name)` at
  class creation; `__get__` raises `PhantomBoxError(self, owner)` for an
  alias installed via `setattr` later.
- interactions: Imported first in `desc/__init__.py` because both
  `FastBox.__class_getitem__` and `AttriBox.__class_getitem__` return
  `_RootAlias.fromAlias(...)` for a non-class subscript. A legitimate use
  such as `class Sub(AttriBox[T])` never reaches `__set_name__` since a
  base-class entry is not a namespace value.

### FastBox
- package: desc
- module: desc/_fast_box.py
- kind: descriptor
- bases: none
- metaclass: none
- uses:
  - _RootAlias | returns for generic subscripts | `__class_getitem__` hands a `TypeVar` or parametrized generic to `Generic.__class_getitem__` and re-clothes the result with `_RootAlias.fromAlias` so binding it in a class body is refused.
- support: `utilities.typeCast` casts a lone default of a number field
  type; `utilities.castRule` decides whether the field type follows a
  builtin number rule; `waitaminute.TypeException` for type-refused
  writes/defaults; `waitaminute.MissingVariable` for a box without a
  field type or deletion of an absent value;
  `waitaminute.dispatch.TypeCastException` is caught from `typeCast` and
  re-raised as `TypeException`.
- description: A lean `Generic[T]` descriptor that is *not* an `Object`
  subclass: no context stack, no hooks, no sentinel resolution.
  `FastBox[int]` (`__class_getitem__`, plain class only) creates a fresh
  box with `__field_type__`; the trailing call `FastBox[int](42)`
  captures `__default_args__`/`__default_kwargs__` and returns self.
  `__set_name__` refuses a box with no field type and stores
  `__private_name__ = '__fast_<name>__'`. `__get__` reads
  `instance.__dict__[private]` and on `KeyError` builds and stores the
  default via `_build`. `__set__` accepts only an instance of the field
  type (no coercion) and stores it. `__delete__` removes the key or
  raises `MissingVariable`; the next read rebuilds a fresh default.
  `_build` follows AttriBox's rules: a container field type refuses a
  lone text argument; a number field type casts a lone value through
  `typeCast` (`_castNumber`); `_callFieldType` tries `fieldType(*args,
  **kwargs)` and, for builtin containers only, retries with
  `fieldType(args)`; the result must be an instance of the field type.
  Owners must have a `__dict__`.
- interactions: The speed-oriented sibling of `AttriBox`; shares the
  `_RootAlias` phantom mechanism and the default-building rules but not
  the `Object` machinery. `desc/__init__` notes it creates no pickling
  tags and follows the default protocol.

### BaseDescriptor
- package: desc
- module: desc/_base_descriptor.py
- kind: descriptor
- bases: Object
- metaclass: MetaType
- uses:
  - Object | implements hooks of | Overrides `hookPreGet`, `hookOnGet`, `hookPreSet`, `hookOnSet`, `hookPreDelete`, `hookOnDelete` and `hookSetName` to look up the registered callback names on `type(instance)` (or the owner) and call them in registration order.
  - flexCall | wraps callbacks with | Each decorator (`preGet`, `onGet`, ...) returns `flexCall(callback)` and `_getCallback` wraps the looked-up function again, so a callback may declare fewer positional parameters than the hook passes.
- support: `utilities.maybe` defaults the key tuples;
  `waitaminute.desc.NamelessCallback` is raised by `_getCallbackName`
  for a lambda or a callable without `__name__`.
- description: `Object` plus seven decorator methods that record callback
  *names* in tuples (`__pre_get_keys__`, `__on_get_keys__`,
  `__pre_set_keys__`, `__on_set_keys__`, `__pre_delete_keys__`,
  `__on_delete_keys__`, `__set_name_keys__`). The hooks resolve those
  names on the class of the accessing instance at call time, so a
  subclass override is used, and a classmethod is unwrapped via
  `__func__`. `hookSetName` calls each setName callback as
  `callback(owner, self)`. Inherits the `Object` defaults (get returns
  self, set raises `ReadOnlyError`, delete raises `ProtectedError`); it
  adds no accessor behaviour of its own and is meant to be subclassed by
  descriptors that implement `__instance_get__`/`__instance_set__`/
  `__instance_delete__`. Under `TYPE_CHECKING` it declares typed
  `__get__`/`__set__` overloads only.
- interactions: Base of `Field` and `AttriBox` (and through it `FixBox`)
  in `desc`. Its reliance on `flexCall` is the one place `desc` depends
  on `dispatch`. `BaseObject` subclasses in `mcls` are the typical owners
  whose methods are decorated with `@box.preGet` etc.

### Alias
- package: desc
- module: desc/_alias.py
- kind: descriptor
- bases: Object
- metaclass: MetaType
- uses:
  - Object | overrides protocol of | Subclasses `Object` but replaces `__get__`, `__set__` and `__delete__` so the context stack and hooks are not used; `__set_name__` calls `Object.__set_name__` for the field bookkeeping and `__init__` passes the real name to `Object.__init__`.
- support: `waitaminute.desc.ReadOnlyError` when the target has no
  `__set__`; `waitaminute.desc.ProtectedError` when it has no
  `__delete__`.
- description: Re-exposes another attribute under a second name.
  Stores `__real_name__`. `_getRealObject(owner)` finds the first entry
  under the real name in the `__dict__` of a class along the MRO (so a
  staticmethod/classmethod is seen raw, as `inspect.getattr_static`
  would), else `getattr(owner, name)`. `__set_name__` tries to resolve
  the target immediately and, if found, writes the real object into
  the owner under the alias name (`setattr`), removing itself; if the
  target is not visible yet it stays and forwards. `__get__`/`__set__`/
  `__delete__` look up the protocol method on `type(realObject)` and
  forward, returning a plain non-descriptor value as is on read and
  refusing writes/deletes to it.
- interactions: Typically used on `BaseObject` subclasses in `mcls` to
  alias an `AttriBox`/`Field` inherited from a parent. One of the three
  `Object` subclasses the `Object` docstring names as overriding the
  entry points wholesale (with `Dispatcher` and `AbstractSpaceHook`).

### Field
- package: desc
- module: desc/_field.py
- kind: descriptor
- bases: BaseDescriptor
- metaclass: MetaType
- uses:
  - BaseDescriptor | extends decorators of | Reuses `_getCallbackName` for `GET`/`SET`/`DELETE`, inherits the notification hooks, and the copy constructor copies the seven callback key tuples of `BaseDescriptor` alongside its own.
  - Object | implements accessors of | Overrides `__instance_get__`, `__instance_set__` and `__instance_delete__`, which `Object.__get__`/`__set__`/`__delete__` call inside the context frame; honours the `_deleting=True` read via `_peekValue`.
  - DELETED | documents deletion through | A deleter may store `DELETED`; the getter then answers it and `Object._deletedGuard` raises `MissingVariable` on a second `del` or a read.
- support: `utilities.maybe` defaults the key tuples;
  `waitaminute.TypeException` for a wrong `other` in the constructor or
  a non-str getter key; `waitaminute.desc.AccessError` when no getter is
  registered; `waitaminute.desc.ReadOnlyError` when no setter;
  `waitaminute.desc.ProtectedError` when no deleter.
- description: Property-like descriptor whose accessors are methods
  decorated below it in the class body: `@field.GET` (one getter, last
  wins), `@field.SET` (any number, run in order), `@field.DELETE` (any
  number). Only the *names* are recorded (`__get_key__`,
  `__set_keys__`, `__delete_keys__`) and resolved with `getattr(owner,
  key)` on the type of the accessing instance, so a subclass overrides
  an accessor simply by redefining the method name. `__instance_get__`
  calls the getter; with `_deleting=True` it uses `_peekValue`, which
  swallows getter exceptions so deleters still run. `__init__(other)`
  copies the key groups from another `Field`.
- interactions: Built on `BaseDescriptor` and the `Object` context
  protocol; `SymbolicName` (later in `desc`) and user classes based on
  `BaseObject` use it. The `work_test` samplers rely on the by-name
  override behaviour.

### AttriBox
- package: desc
- module: desc/_attri_box.py
- kind: descriptor
- bases: BaseDescriptor
- metaclass: MetaType
- uses:
  - BaseDescriptor | inherits hooks from | Gets the notification decorators and hook dispatch; `__set_name__` calls `BaseDescriptor.__init__` to capture an empty argument list when the trailing call was omitted.
  - Object | implements accessors of | Overrides `__instance_get__`, `__instance_set__`, `__instance_delete__`; `__call__` routes the deferred default through `Object.__init__` so `getPosArgs`/`getKeyArgs`/`hasSentinelArgs`/`filterSentinels` and `getPrivateName` can be used; `__get__` checks the field type then defers to `Object.__get__`.
  - Field | exposes field type through | The class attribute `fieldType = Field()` with `@fieldType.GET getFieldType` makes the captured field type readable as a descriptor.
  - _RootAlias | returns for generic subscripts | `__class_getitem__` re-clothes a non-class subscript (TypeVar, `list[int]`) with `_RootAlias.fromAlias` so a class body binding it raises `PhantomBoxError`.
  - DELETED | stores on delete | `__instance_delete__` stores `DELETED` under the storage name; the next read is turned into `MissingVariable` by `Object._deletedGuard`.
  - THIS | substitutes in defaults | Captured `THIS` is replaced by the accessing instance via `getPosArgs`/`getKeyArgs`/`_assignedArgs`; `hasSentinelArgs` suppresses the deep-copy shortcut when it is present.
  - OWNER | substitutes in defaults | Captured `OWNER` is replaced by the owner class at build time.
  - DESC | substitutes in defaults | Captured `DESC` is replaced by the box itself at build time.
- support: `utilities.typeCast` performs lossless conversions
  (`resolveNumber`, `resolveText`, and the no-instantiation cast in
  `__instance_set__`); `utilities.castRule` decides whether a field type
  follows a builtin number rule; `utilities.textFmt` formats the refusal
  of a second `__call__`; `waitaminute.TypeException` for refused
  values/arguments; `waitaminute.MissingVariable` for a missing field
  type; `waitaminute.desc.MissingInstanceDict` when the instance has no
  `__dict__`; `waitaminute.desc.StorageCollision` when two boxes derive
  the same storage name; `waitaminute.dispatch.TypeCastException` is
  caught from `typeCast` (an `OverflowError` cause is re-raised as is).
- description: The main lazily built, strongly typed attribute
  descriptor, declared `x = AttriBox[T](*args, **kw)`.
  `__class_getitem__` (plain class only) creates a fresh instance of the
  box class with `__field_type__`; `__call__` captures the deferred
  default through `Object.__init__` and refuses a second call on a
  placed box. `__set_name__` refuses a box without field type, fills an
  empty argument list if the call was omitted, delegates to
  `BaseDescriptor.__set_name__`, then `_refuseStorageCollision`.
  Storage: each instance holds the value under
  `_getStorageName()` = `getPrivateName() + boxclassname +
  '_field_object__'` (e.g. `__foo_bar__attribox_field_object__`), written
  with `object.__setattr__` by `_store`. `__instance_get__` reads it with
  `object.__getattribute__`; on miss (not when `_deleting`) it builds via
  `_resolve(*getPosArgs(), **getKeyArgs())`, stores and re-reads.
  `_resolve`: a lone argument already of the field type (and no
  sentinel args, no kwargs) is deep-copied; otherwise a text field goes
  to `resolveText`, a lone number value to `resolveNumber`, else
  `_callFieldType` (containers take one iterable, refuse lone text,
  several args become elements); the result must be an instance of the
  field type and is tagged by `_applyTags` with `__field_name__`,
  `__field_owner__`, `__field_box__` (skipping args, classes,
  `__no_box_tag__` classes, `Enum` members, objects without `__dict__`).
  `__instance_set__`: a value of the field type is stored; text fields
  go through `_resolve`; otherwise `typeCast(..., allowInstantiation=
  False)` then fallback to `_resolve(*_assignedArgs(value))` where an
  assigned tuple splats except for builtin containers; returns the
  stored value for `onSet`. `__copy__`/`__deepcopy__` return the box
  itself; `__reduce__` pickles a placed box by reference to
  `(owner, name)`.
- interactions: The workhorse descriptor for `BaseObject` classes in
  `mcls`. `FixBox` subclasses it; `Kee`/`KeeBox` in the leaf `keenum`
  package also do. The `_RootAlias` mechanism is shared with `FastBox`.
  The `castRule`/`typeCast` rules are the same the `Dispatcher` uses in
  its SLOW pass, so boxes and overloads coerce alike.

### FixBox
- package: desc
- module: desc/_fix_box.py
- kind: descriptor
- bases: AttriBox
- metaclass: MetaType
- uses:
  - AttriBox | restricts writes of | `__instance_set__` checks the storage name with `object.__getattribute__` and raises `WriteOnceError` if a value is already there, otherwise delegates to `AttriBox.__instance_set__`.
  - Object | restores default deletion of | `__instance_delete__` calls `Object.__instance_delete__`, which raises `ProtectedError`, so deletion is disabled.
- support: `waitaminute.desc.WriteOnceError` (a `TypeError`) is raised
  on a second write.
- description: A write-once `AttriBox`. The single write is whatever
  stores the value first, including the lazily built default on the
  first read, so a runtime value must be assigned before the first read.
  Deletion always raises `ProtectedError`.
- interactions: Inherits the storage name scheme (stores at
  `__foo_bar__fixbox_field_object__`), tagging, pickling and copying of
  `AttriBox`.

### SymbolicName
- package: desc
- module: desc/_symbolic_name.py
- kind: class
- bases: Object
- metaclass: MetaType
- uses:
  - Field | exposes renderings through | Seven `Field()` class attributes (`words`, `snake`, `pascal`, `camel`, `kebab`, `screamingSnake`, `screamingKebab`) each with a `@field.GET` getter compute the renderings on read.
  - Object | is a value based on | Being an `Object`, a `SymbolicName` placed in a class body is a shared read-only class attribute (the `Object` defaults apply); the constructor does not call `Object.__init__`.
- support: `utilities.textFmt` formats `__str__`/`__repr__`;
  `waitaminute.MissingVariable` when no words were given;
  `waitaminute.TypeException` for a non-str word or a bad subscript.
- description: Holds a tuple of words (`__part_words__`) and renders
  them as snake_case, SCREAMING_SNAKE_CASE, kebab-case,
  SCREAMING-KEBAB-CASE, PascalCase and camelCase. Supports `bool`,
  `len`, iteration, `in`, int and slice indexing. Equality and hashing
  use the lower-cased words, so names differing only in case are one
  key; comparison with anything else returns `NotImplemented`.
- interactions: A small consumer of `Field` and `Object`; used elsewhere
  in the library (e.g. `keenum`) for naming, and demonstrates the
  `Field` pattern with private `__x__` state and GET-only accessors.

### SpaceDesc
- package: mcls
- module: mcls/space_hooks/_space_desc.py
- kind: descriptor
- bases: none
- metaclass: none
- uses:
  - AbstractSpaceHook | exposes namespace of | Placed as `AbstractSpaceHook.space`; on a hook instance it returns `instance.__space_object__`, the namespace the hook is currently bound to.
- support: none
- description: Minimal `Generic[NamespaceT]` non-data descriptor:
  returns itself on class access, otherwise `getattr(instance,
  '__space_object__')`.
- interactions: Only consumed by `AbstractSpaceHook` and its subclasses,
  which read `self.space` to reach the `AbstractNamespace`/`BaseSpace`
  during a phase.

### ReservedNames
- package: mcls
- module: mcls/space_hooks/_reserved_names.py
- kind: descriptor
- bases: none
- metaclass: none
- uses: none
- support: none
- description: Descriptor that returns itself on class access and, on
  instance access, the tuple of names the interpreter sets
  automatically: `__dict__`, `__weakref__`, `__module__`,
  `__annotations__`, `__match_args__`, `__doc__`, `__name__`,
  `__qualname__`, `__firstlineno__`, `__static_attributes__`,
  `__classcell__`, `__classdictcell__`, `__orig_bases__`,
  `__type_params__`.
- interactions: Placed as `ReservedNamespaceHook.reservedNames`.

### AbstractSpaceHook
- package: mcls
- module: mcls/space_hooks/_abstract_space_hook.py
- kind: hook
- bases: Object
- metaclass: MetaType
- uses:
  - Object | overrides protocol of | Subclasses `Object` for the `__set_name__` bookkeeping only; `__get__` is replaced to bind `__space_object__` to the accessing namespace and return the hook, so the context stack and hooks are not used.
  - SpaceDesc | exposes namespace through | The class attribute `space = SpaceDesc()` gives phase methods access to the bound namespace as `self.space`.
  - AbstractNamespace | registers with | `__set_name__` calls `owner.addHook(self)`, so declaring a hook in a namespace class body registers it; phases receive and return the namespace's compiled dict.
- support: none
- description: Base class of the namespace hooks. Defines the phase
  protocol with no-op defaults: `preparePhase(space)` (during namespace
  `__init__`, no changes allowed), `setItemPhase(key, val, old) ->
  bool` (True blocks the default store), `getItemPhase(key, value)`,
  `preCompilePhase(dict) -> dict`, `postCompilePhase(dict) -> dict`, and
  `newClassPhase(cls) -> cls`. `__get__` on a namespace instance sets
  `__space_object__` and returns the hook.
- interactions: Base of `FlexCallHook`, `ReservedNamespaceHook`,
  `NamespaceHook` and `LoadSpaceHook`. `AbstractNamespace` calls the
  phases in order; `AbstractMetaclass` calls `newClassPhase`. One of the
  three `Object` subclasses named in the `Object` docstring as
  overriding the entry points.

### FlexCallHook
- package: mcls
- module: mcls/space_hooks/_flex_call_hook.py
- kind: hook
- bases: AbstractSpaceHook
- metaclass: MetaType
- uses:
  - AbstractSpaceHook | implements phase of | Overrides `postCompilePhase` only.
  - flexCall | wraps functions with | In `postCompilePhase` every `FunctionType` value of the compiled dict is replaced by `flexCall(val)`, so the class's methods drop surplus positional arguments.
- support: none
- description: Opt-in hook; no namespace in worktoy declares it. A
  namespace that wants its classes' methods to truncate extra positional
  arguments declares `flexCallHook = FlexCallHook()`.
- interactions: Provides the only `mcls` entry point to `flexCall`
  besides `BaseDescriptor`.

### ReservedNamespaceHook
- package: mcls
- module: mcls/space_hooks/_reserved_namespace_hook.py
- kind: hook
- bases: AbstractSpaceHook
- metaclass: MetaType
- uses:
  - AbstractSpaceHook | implements phase of | Overrides `setItemPhase` to raise `ReservedName` when a reserved key is bound while already present in `self.space`.
  - ReservedNames | reads list from | The class attribute `reservedNames = ReservedNames()` supplies the protected names.
- support: `waitaminute.meta.ReservedName` is raised for a protected
  name already present in the namespace.
- description: Protects interpreter-set names (`__dict__`, `__module__`,
  `__qualname__`, ...) from being reassigned in a class body, but only
  if the name already exists in the namespace, so deferred
  initialisation by the interpreter still works. Returns False so the
  assignment proceeds otherwise.
- interactions: Declared on `AbstractNamespace` (see that entry).

### NamespaceHook
- package: mcls
- module: mcls/space_hooks/_name_hook.py
- kind: hook
- bases: AbstractSpaceHook
- metaclass: MetaType
- uses:
  - AbstractSpaceHook | implements phases of | Overrides `setItemPhase` (name screening) and `preCompilePhase` (seeding class hooks).
  - METACALL | seeds hooks with | `preCompilePhase` writes `METACALL` into the compiled dict for every routed `__class_*__` hook name that neither the body nor a class along the lookup order supplies, so `AbstractMetaclass` falls back to its own implementation.
  - AbstractMetaclass | checks shadowing against | `_getShadowingMetaclass` imports `AbstractMetaclass` locally and walks `space.getMetaclass().__mro__` up to it to find a metaclass that implements the operation itself (e.g. `__len__`), in which case the hook is refused.
  - AbstractNamespace | reads state of | Uses `self.space.getKwargs()`, `getMetaclass()`, `getClassName()`, `getBases()` and `_getLookupOrder()`.
- support: `waitaminute.meta.QuestionableSyntax` for a near-miss dunder
  (`__setname__`, `__get_item__`, `__set_item__`, `__del_item__`);
  `waitaminute.meta.DelException` for `__del__` without
  `trustMeBro=True`; `waitaminute.meta.UnboundClassHook` for a routed
  hook bound to a plain function or staticmethod (in the body or in a
  plain base); `waitaminute.meta.ShadowedClassHook` for a routed hook
  whose operation a metaclass before `AbstractMetaclass` in the MRO
  takes over.
- description: Screens names as they are bound. `_getClassDunders` lists
  the routed hooks: `__class_call__`, `__class_init__`,
  `__class_instancecheck__`, `__class_subclasscheck__`, `__class_str__`,
  `__class_repr__`, `__class_iter__`, `__class_next__`,
  `__class_bool__`, `__class_contains__`, `__class_len__`,
  `__class_hash__`, `__class_setitem__`, `__class_delitem__`,
  `__class_getattr__`, `__class_setattr__`, `__class_delattr__`
  (`__class_eq__`/`__class_ne__`/`__class_getitem__` deliberately
  excluded). `__class_init__` is a chained hook never shadowed.
  `setItemPhase`: refuses `__del__` unless `trustMeBro`, refuses
  shadowed or unbound class hooks, then `_validateName` for near
  misses. `preCompilePhase`: for each routed hook not in the body, if a
  class on the lookup order supplies it, validate it is not a plain
  function/staticmethod; else seed `METACALL`.
- interactions: Declared on `AbstractNamespace`; what makes the
  `__class_*__` routing of `AbstractMetaclass` safe.

### LoadSpaceHook
- package: mcls
- module: mcls/space_hooks/_load_space_hook.py
- kind: hook
- bases: AbstractSpaceHook
- metaclass: MetaType
- uses:
  - AbstractSpaceHook | implements phases of | Overrides `setItemPhase` (claiming overloads) and `postCompilePhase` (building dispatchers).
  - overload | claims from class body | `setItemPhase` recognises `overload` values, records their concrete signatures (as copies via `sig()`), variadics, fallback and finalizer on the namespace, and blocks the default store by returning True; a second binding of the same `overload` object aliases the first name.
  - Dispatcher | assembles | `_buildDispatcher(name)` creates a `Dispatcher()` and feeds it `addSigFunc`/`addVariadicSigFunc` with distances plus `setFallbackFunction`/`setFinalizerFunction`; `postCompilePhase` writes it into the compiled dict for each overloaded name not bound to a plain definition.
  - TypeSig | copies | Each registered signature is copied with `sig()` so the `overload` object keeps `THIS` and can be bound in another class body.
  - BaseSpace | stores registrations in | Calls `hasOverloads`, `addPlainName`, `getPlainNames`, `getClaimedName`, `addClaimedName`, `addOverload`, `addVariadic`, `addFallback`, `addFinalizer`, `collectOverloads`, `collectVariadics`, `collectFallback`, `collectFinalizer`, `getOverloadNames` and `getClassName` on `self.space`, which `BaseSpace` provides.
- support: `waitaminute.meta.OverloadConflict` is raised when one class
  body gives a name both a plain definition and an overload.
- description: The bridge from `dispatch` into class construction. During
  the body it claims each `overload`; after the body it builds one
  `Dispatcher` per overloaded name from the registrations the namespace
  merges across the MRO (own first, inherited with distance), skipping
  names the body bound to a plain definition and names where a plain
  definition in a base shadows every registration.
- interactions: Declared on `BaseSpace`. The `Dispatcher` it writes is
  placed by `type.__new__` and gets `__set_name__`, which swaps `THIS`.

### AbstractNamespace
- package: mcls
- module: mcls/_abstract_namespace.py
- kind: namespace
- bases: none
- metaclass: none
- uses:
  - ReservedNamespaceHook | declares | The class attribute `reservedNameHook = ReservedNamespaceHook()` registers the hook through `__set_name__`/`addHook`.
  - NamespaceHook | declares | The class attribute `nameHook = NamespaceHook()` registers the name-screening hook the same way.
  - AbstractSpaceHook | runs phases of | `__init__` calls `preparePhase`, `__getitem__` calls `getItemPhase`, `__setitem__` calls `setItemPhase` (a True return claims the binding), `preCompile`/`postCompile` call `preCompilePhase`/`postCompilePhase`; `getHooks` binds each hook's `__space_object__` to this namespace first, and `addHook` is the classmethod hooks register through.
  - AbstractMetaclass | is prepared by | `__init__(mcls, name, bases, **kwargs)` matches the `__prepare__` signature of `AbstractMetaclass`, which instantiates it and later calls `compile()`.
- support: `utilities.maybe` for defaults; `utilities.textFmt` for
  `__str__`; `utilities.resolveMRO` computes the C3 MRO of the bases
  (a `TypeError` for inconsistent bases is re-raised unless
  `_strictMRO=False`); `waitaminute.TypeException` for a non-dict passed
  to `preCompile`; `waitaminute.meta.HookException` wraps an exception
  raised by a hook's `getItemPhase`; `waitaminute.meta.DuplicateHook` when
  two different hooks share a field name; `waitaminute.meta.ClaimedName`
  when the class body deleted a name a hook claimed.
- description: `dict` subclass used as the class-body namespace. Stores
  `__metaclass__`, `__class_name__`, `__base_classes__`, `__class_mro__`
  (from `resolveMRO`), `__key_args__`, `__compiled_space__`,
  `__shadow_space__` (every assignment, claimed or not, so a claimed
  name stays readable in the body) and `__claimed_deletions__`. Hooks
  are kept per namespace class in a list attribute named
  `__hook_objects__` and collected over the class MRO by
  `classGetHooks`. `__getitem__` reads the dict then the shadow space,
  runs `getItemPhase` on each hook, and re-raises a miss. `__setitem__`
  records in the shadow space, offers `setItemPhase` to each hook and
  stores only if none claims it. `__delitem__` removes from both, and
  records a deletion of a claimed name for `compile` to refuse.
  `getMROSpace`/`deepGetItem` merge the `__compiled_space__` dicts of
  bases found via their `__namespace__`. `compile()` refuses claimed
  deletions, runs `preCompile`, merges the body's own names, runs
  `postCompile`, and adds `__metaclass__`, `__namespace__` and
  `__keyword_arguments__` before recording the result.
- interactions: Returned by `AbstractMetaclass.__prepare__`; its
  `compile()` output is what `AbstractMetaclass.__new__` hands to
  `MetaType.__new__`, so the class keeps `__namespace__`. `BaseSpace`
  subclasses it and adds the overload registries `LoadSpaceHook` needs.
  Sibling in role to `ControlSpace` in `core`.

### AbstractMetaclass
- package: mcls
- module: mcls/_abstract_metaclass.py
- kind: metaclass
- bases: MetaType
- metaclass: MetaType
- uses:
  - MetaType | builds classes through | `__new__` calls `MetaType.__new__` with the compiled dict; `__init__`, `__call__`, `__instancecheck__`, `__subclasscheck__`, `__str__`, `__repr__`, `__setattr__`, `__delattr__` fall back to the `MetaType`/`type` implementations when a hook is `METACALL`.
  - AbstractNamespace | prepares and compiles | `__prepare__` returns `AbstractNamespace(mcls, name, bases, **kwargs)`; `__new__` copies a plain dict into one if needed, calls `space.compile()` and then `newClassPhase` of each hook; `getNamespace`/`getNamespaceClass` expose it.
  - AbstractSpaceHook | runs final phase of | After the class exists `__new__` calls `hook.newClassPhase(cls)` for every hook of the namespace and keeps a non-None return.
  - METACALL | routes class hooks with | Every `__class_*__` lookup compares against `METACALL` (identity) to decide between the class-level hook and the metaclass default; the metaclass itself seeds `__class_getattr__`, `__class_setattr__`, `__class_delattr__`, `__class_call__` with it.
  - SentinelMeta | annotates hooks as | The four seeded hook attributes are annotated with `SentinelMeta` as their type (they hold the `METACALL` sentinel class).
  - _Chill | respects flag of | `__hash__` skips bases whose `__skip_hash__` is True (`_skipHash`), the flag `_Chill` and `MetaType` maintain.
- support: `utilities.maybe` keeps the class when `newClassPhase`
  returns None; `waitaminute.MissingVariable` is raised by
  `__getattr__` for a missing class attribute when no
  `__class_getattr__` hook exists.
- description: The base of the worktoy metaclasses. `__prepare__` ->
  `AbstractNamespace`; `__new__` compiles it and builds the class;
  `__init__` runs `MetaType.__init__`, then `__class_init__(name, bases,
  space, **kw)` if provided, then `_notifySubclassHook` which calls
  `base.__subclasshook__(cls)` on each base (return ignored). The
  routed operations: `__call__` -> `__class_call__`, `__instancecheck__`,
  `__subclasscheck__`, `__str__`, `__repr__`, `__iter__`, `__next__`,
  `__bool__` (falls back to `__class_len__`, then `__class_iter__`, then
  True), `__contains__` (falls back to iteration), `__len__` (falls back
  to counting iteration), `__hash__` (default hashes class name, base
  names minus skipped/`object`, and metaclass name), `__setitem__`,
  `__delitem__`, `__getattr__`, `__setattr__`, `__delattr__`.
  `__eq__`/`__ne__`/`__getitem__` are deliberately not routed.
  `__abstract_metaclass__ = True`.
- interactions: `BaseMeta` subclasses it and swaps the namespace for
  `BaseSpace`. `NamespaceHook` seeds the hook names with `METACALL` and
  refuses hooks a metaclass in front of `AbstractMetaclass` would
  shadow. Leaf metaclasses (`KeeMeta`, `EZMeta`) build on it.

### BaseSpace
- package: mcls
- module: mcls/_base_space.py
- kind: namespace
- bases: AbstractNamespace
- metaclass: none
- uses:
  - AbstractNamespace | extends registries of | Inherits the hook machinery, shadow space and `_getLookupOrder`, adding the per-name overload, variadic, fallback, finalizer, plain-name and claimed-overload registries.
  - LoadSpaceHook | declares | The class attribute `loadSpaceHook = LoadSpaceHook()` registers the hook that fills and reads these registries.
  - TypeSig | compares registrations by | `addOverload` and `_mergeSigFuncs` use `TypeSig.__eq__` to skip or refuse an equal signature; registrations are kept in lists because a signature holding `THIS` hashes differently before and after its class exists.
  - Dispatcher | recognises built dispatchers | `_definesPlainly` treats a `Dispatcher` that a `BaseSpace` built on compilation as not shadowing inherited registrations, while a body-written `Dispatcher` or any other value is a plain definition that stops the MRO walk.
  - overload | records claims of | `addClaimedName`/`getClaimedName` remember which name an `overload` object was first bound to in this body (typed `Claim = tuple[overload, str]`).
- support: `utilities.maybe` defaults the registries;
  `waitaminute.dispatch.DuplicateSignature` for an equal signature with
  a different function, or a second fallback/finalizer in one body.
- description: The namespace `BaseMeta` prepares. Registries:
  `__overload_map__`, `__variadic_overload_map__`, `__fallback_map__`,
  `__finalizer_map__` (name -> registrations of this body only),
  `__plain_names__`, `__claimed_overloads__`. `collectOverloads`,
  `collectVariadics`, `collectFallback`, `collectFinalizer` merge the
  body's own registrations (distance 0) with those of the `BaseSpace`
  namespaces of classes along `_getLookupOrder` (distance 1, 2, ...),
  stopping at the first class that `_definesPlainly` holds the name,
  and skipping equal signatures so the nearest wins.
  `getOverloadNames` lists every name any space on the lookup order
  registered. Setters: `addOverload`, `addVariadic`, `addPlainName`,
  `addClaimedName`, `addFallback`, `addFinalizer`.
- interactions: Filled by `LoadSpaceHook.setItemPhase` and read by its
  `postCompilePhase`; the distances it records drive the ordering of
  the `Dispatcher` passes. Its `__compiled_space__`/`__namespace__`
  survive on the class so subclasses can inherit registrations.

### BaseMeta
- package: mcls
- module: mcls/_base_meta.py
- kind: metaclass
- bases: AbstractMetaclass
- metaclass: MetaType
- uses:
  - BaseSpace | prepares as namespace | `__prepare__` returns `BaseSpace(mcls, name, bases, **kwargs)`, the one override it makes.
  - AbstractMetaclass | inherits construction from | Everything else (compile, `newClassPhase`, class hooks, `__class_init__`, subclass notification) is inherited unchanged.
- support: none
- description: `AbstractMetaclass` with `BaseSpace` as the class-body
  namespace, so classes built by it get `LoadSpaceHook` (overloads)
  in addition to `NamespaceHook` and `ReservedNamespaceHook`.
- interactions: Metaclass of `BaseObject`; placing the `Dispatcher`
  objects `LoadSpaceHook` wrote into the compiled dict is done by
  `type.__new__` inside `MetaType.__new__`, which fires
  `Dispatcher.__set_name__` and thereby `swapAllTHIS`. Leaf metaclasses
  (`KeeMeta`, `EZMeta`) derive from it.

### BaseObject
- package: mcls
- module: mcls/_base_object.py
- kind: class
- bases: Object
- metaclass: BaseMeta
- uses: none
- support: none
- description: `class BaseObject(Object, metaclass=BaseMeta)` with an
  empty body. The standard entry point: `Object` gives constructor
  argument capture, the descriptor context protocol and the read-only
  class-attribute semantics; `BaseMeta` gives `@overload` dispatch and
  the namespace hooks.
- interactions: The class users subclass to combine `AttriBox`, `Field`,
  `Alias` and `@overload` methods. Every leaf package (`ezdata`,
  `keenum`, `work_test`) builds on it.

# Research notes: the non-leaf packages of worktoy

Read of 2026-10-19, every line of `core`, `dispatch`, `desc` and `mcls`
in the import order of each package `__init__`, with `utilities` and
`waitaminute` opened where a non-leaf item reaches for them. One entry
per item, appended as soon as the item was read.

Entry format. Each entry opens with `## package.Item`, then a `File:`
line, a `Kind:` line (metaclass, class, descriptor, function, sentinel,
signal, namespace, package) and prose. Interactions with the other
non-leaf items are listed as edge lines, one per actual use, so that the
map can be drawn from the notes rather than from the imports:

- `EDGE base <target> :: <verb phrase> :: <one or two sentences>`
  the item is a class based on the target class
- `EDGE meta <target> :: <verb phrase> :: <one or two sentences>`
  the item is a class derived from the target metaclass
- `EDGE use <target> :: <verb phrase> :: <one or two sentences>`
  any other use of the target by the item
- `SUPPORT <utilities.x or waitaminute.x> :: <what for>`
  a reliance on the support packages, kept out of the graph
- `Recommendations:` closes the prose of every entry, either as the
  line `Recommendations: none.` or as a list of `- RECOMMEND [severity]`
  lines, each a recommendation of this read about the item; severities
  are `medium`, `low` and `note`, with `docstring`, `message` or
  `typing` added where only text changes

Targets are written `package.Item`; subpackages are flattened into their
top-level package for grouping, so `core.sentinels.THIS` is a node of
the `core` group. Private helpers get entries of their own when they do
real work.

Packages and the order read: `core` (`_meta_type`, `sentinels`,
`control_flow`, `_instance_owner`, `_object`), then `dispatch`, `desc`,
`mcls`.

---

## core (package)
File: src/worktoy/core/__init__.py
Kind: package

Exports `MetaType`, the `sentinels` and `control_flow` subpackages,
`ContextInstance`, `ContextOwner` and `Object`, in that load order.
`_meta_type` loads first because every other metaclass of the library,
`SentinelMeta` and `MetaFlow` included, is built from it. The docstring
names the package as the primitive runtime types the metaclass framework
and the descriptor layer build on, which the read confirms: nothing in
`core` imports from `dispatch`, `desc` or `mcls`.

Recommendations: none.

## core._Chill
File: src/worktoy/core/_meta_type.py (lines 21-32)
Kind: class (private base)

A plain class that `MetaType.__new__` appends as the last base of every
class whose last declared base is not already a worktoy-built class. It
has one job: its `__init_subclass__` is a classmethod taking `**kwargs`
that calls no `super()`, so a class keyword written on any worktoy class
statement ends its `__init_subclass__` chain here instead of at
`object.__init_subclass__`, which refuses keywords. It sets
`__skip_hash__` to False on each subclass; the class itself holds
`__skip_hash__ = True`, and `AbstractMetaclass._skipHash` in `mcls`
reads that attribute. It sits at the very end of every resolution order
(`Object.__mro__` is `Object, _Chill, object`; `SkipSet.__mro__` ends
`BaseException, _Chill, object`).

Recommendations: none.

- EDGE use core.MetaType :: is appended by :: MetaType.__new__ adds _Chill to the bases of every class whose last base is not a MetaType-built class, so keyword class statements are absorbed here.

## core.MetaType
File: src/worktoy/core/_meta_type.py (lines 35-92)
Kind: metaclass (meta-metaclass)

The root metaclass. `__new__` does four things: appends `_Chill` when
the last base is not an instance of `MetaType`; drops `object` from the
bases; on Python 3.10 and up, when the class being built is itself a
metaclass (a base is a subclass of `type`) and its body carries
annotations, replaces the eager `__annotations__` dict with an
`_AnnotationsDescriptor`; and, unless the namespace already has one,
binds `__namespace__` to the namespace itself for the duration of
`type.__new__`, deleting it from the namespace afterwards. Because
`type.__new__` copies the namespace, every class built by any worktoy
metaclass keeps the namespace that built it in its own `__dict__` under
`__namespace__` (verified: `'__namespace__' in Object.__dict__` is
True while the dict it points to no longer holds the key). Consumers
are in `mcls` (`AbstractNamespace`, `AbstractMetaclass`, `BaseSpace`)
and the leaf packages. `__init__` deliberately does not call
`type.__init__`, which refuses keywords, and sets `__skip_hash__` to
False. `__str__` and `__repr__` render a class as
`Name[metaclass=Meta]`, so `repr(Object)` is `Object[metaclass=MetaType]`.
Forwards `**kw` to `type.__new__`, so class keywords reach
`__init_subclass__` and are absorbed by `_Chill`.

Recommendations:
- RECOMMEND [low, docstring] State in the class docstring that every class built by a worktoy metaclass keeps the namespace that built it in its own `__dict__` under `__namespace__`; today only a comment in `__new__` and the `AbstractNamespace` docstring say so, while `mcls` and the leaf packages depend on it.

- EDGE use core._Chill :: appends as last base :: Ensures every worktoy class ends its __init_subclass__ chain at _Chill so class keywords never reach object.__init_subclass__.
- EDGE use core._AnnotationsDescriptor :: installs on metaclasses :: When a metaclass body carries annotations, the eager dict is wrapped so cls.__annotations__ on its classes answers for the class alone (Python 3.10 and up).

## core._AnnotationsDescriptor
File: src/worktoy/core/_annotations_descriptor.py
Kind: descriptor (private)

Wraps the annotations dict of a metaclass body. `__get__` with no
instance (read on the metaclass itself) returns the stored metaclass
annotations; read on a class it delegates to the getset descriptor
`type.__dict__['__annotations__']` so the class answers with its own
annotations, not a base's. `__set__` and `__delete__` delegate the
same way. Declares `__objclass__ = type`. The module also computes
`HAS_TYPE_ANNOTATIONS`, True where `type` carries that descriptor
(3.10 and up); `MetaType` installs nothing where it is False.

Recommendations:
- RECOMMEND [low, docstring] The three method docstrings restate the method names and the one on `__get__` is inaccurate (it says the owner's annotations are returned for class and instance access alike, while a read on the metaclass returns the metaclass's own). Replace them with the two-way rule the class docstring already gives, or drop them.

- SUPPORT utilities.maybe :: picks the explicit owner over type(cls) in __get__.

## core.sentinels (package)
File: src/worktoy/core/sentinels/__init__.py
Kind: package

Load order: `_sentinel` (Sentinel, SentinelMeta), then DELETED, OWNER,
THIS, DESC, METACALL, ARGS. The docstring assigns each sentinel its
role; the uses it describes (DELETED by descriptors, THIS/OWNER/DESC in
deferred AttriBox arguments and overload signatures, METACALL by
AbstractMetaclass, ARGS in overload signatures) are confirmed in the
later packages and recorded as edges from the users.

Recommendations: none.

## core.sentinels.SentinelMeta
File: src/worktoy/core/sentinels/_sentinel.py (lines 76-168)
Kind: metaclass

Subclasses `MetaType` and derives from it (`metaclass=MetaType`), so its
own resolution order is `SentinelMeta, MetaType, type, _Chill, object`.
Keeps one process-wide registry, a list on `SentinelMeta` itself
(`__registered_sentinels__`, rebuilt as a new list on each register),
shared by every subclass of `SentinelMeta` such as `_MetaARGS`.
`__prepare__` returns a plain dict. `__new__` looks the name up and
raises `DuplicateSentinel` for a second class statement at a registered
name, passing the refused statement's `__module__`; otherwise builds
through `MetaType.__new__` and registers. `__call__` raises
`IllegalInstantiation`, so a sentinel class cannot be instantiated.
`__hash__` hashes the tuple of metaclass module, metaclass name, class
module and class name, so a sentinel hashes the same wherever it is
seen; `__eq__` is identity. `__str__` renders `<Sentinel: 'NAME'>`.

Recommendations: none.

- EDGE meta core.MetaType :: derives from :: Declared with metaclass=MetaType so a sentinel declared with a class keyword has it absorbed by _Chill.
- EDGE base core.MetaType :: is based on :: Subclasses MetaType, so sentinel classes are built through MetaType.__new__ (namespace binding, _Chill appending).
- SUPPORT utilities.maybe :: empty registry fallback.
- SUPPORT waitaminute.meta.DuplicateSentinel :: raised for a second class statement at a registered name.
- SUPPORT waitaminute.meta.IllegalInstantiation :: raised by __call__.

## core.sentinels.Sentinel
File: src/worktoy/core/sentinels/_sentinel.py (lines 171-178)
Kind: sentinel (base)

The empty base class built by `SentinelMeta`; every sentinel is based on
it. It carries no behaviour of its own: uniqueness, non-instantiation
and rendering all come from the metaclass. Its MRO is
`Sentinel, _Chill, object`.

Recommendations: none.

- EDGE meta core.sentinels.SentinelMeta :: derives from :: Built by SentinelMeta, which registers it, forbids calling it and renders it.

## core.sentinels.DELETED
File: src/worktoy/core/sentinels/_deleted.py
Kind: sentinel

The value a descriptor stores in its backing slot to mark deletion.
`Object._deletedGuard` translates a `DELETED` read into
`MissingVariable`, so a deleted attribute reads as absent without a
separate flag in each of the three lookups a descriptor may make.

Recommendations: none.

- EDGE base core.sentinels.Sentinel :: is based on :: A plain Sentinel subclass; identity is its whole meaning.

## core.sentinels.THIS
File: src/worktoy/core/sentinels/_this.py
Kind: sentinel

Placeholder for the enclosing class inside its own body. Two roles:
in a deferred `AttriBox` argument it is replaced by the accessing
instance at `__get__` time (through `Object.getContextualSentinels`),
and in an `@overload` signature it stands for the class itself, like
`typing.Self`.

Recommendations: none.

- EDGE base core.sentinels.Sentinel :: is based on :: A plain Sentinel subclass.

## core.sentinels.OWNER
File: src/worktoy/core/sentinels/_owner.py
Kind: sentinel

Placeholder for the owner class passed to `__get__`; replaced by that
class in deferred `AttriBox` arguments. No role in overload signatures.

Recommendations: none.

- EDGE base core.sentinels.Sentinel :: is based on :: A plain Sentinel subclass.

## core.sentinels.DESC
File: src/worktoy/core/sentinels/_desc.py
Kind: sentinel

Placeholder for the descriptor object itself in deferred `AttriBox`
arguments; `Object.getContextualSentinels` maps it to `self`.

Recommendations: none.

- EDGE base core.sentinels.Sentinel :: is based on :: A plain Sentinel subclass.

## core.sentinels.METACALL
File: src/worktoy/core/sentinels/_meta_call.py
Kind: sentinel

Marker placed as the value of a class-level hook such as
`__class_str__` or `__class_iter__` to say "defer to the metaclass";
`AbstractMetaclass` in `mcls` falls back to its own implementation when
it finds it.

Recommendations: none.

- EDGE base core.sentinels.Sentinel :: is based on :: A plain Sentinel subclass.

## core.sentinels._MetaARGS
File: src/worktoy/core/sentinels/_args.py (lines 17-33)
Kind: metaclass (private)

Subclass of `SentinelMeta` (its metaclass is inherited: `MetaType`).
It overrides `__call__` alone: `ARGS(type_)` builds an instance through
`type.__call__` and stores `type_` under `__inner_type__`, so `ARGS` is
the one sentinel that can be instantiated. Registration and duplicate
refusal still come from `SentinelMeta.__new__`.

Recommendations:
- RECOMMEND [low, typing] `__call__` is annotated as returning `_MetaARGS` but returns an instance of the sentinel class; annotate it as `ARGS` (or `Self` of the class called).

- EDGE base core.sentinels.SentinelMeta :: is based on :: Inherits the registry, duplicate refusal and rendering; replaces only __call__.

## core.sentinels.ARGS
File: src/worktoy/core/sentinels/_args.py (lines 36-77)
Kind: sentinel (instantiable)

Placeholder for the starred tail of an overload signature. `ARGS[int]`
goes through `__class_getitem__` to `cls(type_)`, so every subscript
is a new instance; instances compare equal and hash alike when their
inner types are the same object, which lets a variadic signature in a
subclass be recognised as the one it overrides. `__iter__` yields the
instance itself, so unpacking an `ARGS` instance where a signature is
flattened leaves it in place. `__str__` renders `ARGS[int]`.

Recommendations:
- RECOMMEND [low] No non-leaf item iterates an `ARGS` instance (`TypeSig` iterates its raw types and reads `__inner_type__` directly), so `__iter__` yielding the instance itself has no visible purpose here. Check the leaf packages and tests for a user; if none, remove it or say in the docstring what it is for.

- EDGE meta core.sentinels._MetaARGS :: derives from :: Declared with metaclass=_MetaARGS so that calling the class is allowed.

## core.control_flow (package)
File: src/worktoy/core/control_flow/__init__.py
Kind: package

Load order: `ControlSpace`, `MetaFlow`, `ControlFlow`, `SkipSet`. The
signals are exceptions raised to steer a protocol, used by type alone
as sentinels are used by identity, which is why both families live in
`core`. `ControlClassError`, the refusal of a body attribute, lives in
`waitaminute.meta`; `waitaminute.control_flow` re-exports these names
for 1.x.

Recommendations: none.

## core.control_flow.ControlSpace
File: src/worktoy/core/control_flow/_control_space.py
Kind: namespace

A `dict` subclass `MetaFlow.__prepare__` returns. `__init__` records the
metaclass, bases and class name, reads the `_root` keyword, and binds
`__namespace__` to itself (so `MetaType.__new__` sees a namespace that
already has one and leaves it alone). `__setitem__` admits the
whitelist (`__firstlineno__`, `__str__`, `__repr__`, `__namespace__`,
`__static_attributes__`, `__classcell__`, `__classdictcell__`); for a
non-root class every other key is refused with `ControlClassError`
unless `Exception` has a non-callable attribute of that name (so
`__doc__`, `__module__`, `__qualname__` pass). The root class accepts
anything. A body annotation would be refused, since `__annotations__`
is neither whitelisted nor an attribute of `Exception`.

Recommendations:
- RECOMMEND [low] Rootness is recorded twice: `__init__` keeps it as the `__is_root__` attribute of the namespace, and `MetaFlow.__prepare__` writes an `__is_root__` key into the same namespace for the class. One record would do; the attribute is the one `__setitem__` reads.

- EDGE use core.control_flow.MetaFlow :: is prepared by :: MetaFlow.__prepare__ builds one per signal class statement and writes __str__, __repr__ and __is_root__ into it with dict.__setitem__ to bypass the refusal.
- SUPPORT utilities.maybe :: whitelist and root-flag fallbacks.
- SUPPORT waitaminute.meta.ControlClassError :: raised for a refused body attribute; it reads the space's metaclass and class name to render.

## core.control_flow.MetaFlow
File: src/worktoy/core/control_flow/_meta_flow.py
Kind: metaclass

Subclasses `MetaType` and derives from it, as `SentinelMeta` does.
`__prepare__` returns a `ControlSpace` carrying a generated `__str__`
(the instance renders as its class) and `__is_root__` from the `_root`
keyword. `__new__` builds through `MetaType.__new__`, which appends
`_Chill` (the signal's last declared base is `Exception`) and so
absorbs `_root`; a root class is registered once on the metaclass,
a second root raising `VariableNotNone`. `__str__` renders
`<Root: [Root]>` for the root and `<Root: Name>` for a signal
(`repr(SkipSet)` is `<ControlFlow: SkipSet>`, and so is
`str(SkipSet())`).

Recommendations: none.

- EDGE meta core.MetaType :: derives from :: Declared with metaclass=MetaType so the signals' class keyword (_root) is absorbed by _Chill.
- EDGE base core.MetaType :: is based on :: Signal classes are built through MetaType.__new__.
- EDGE use core.control_flow.ControlSpace :: prepares :: Returns a ControlSpace from __prepare__ so that the class body is policed while it executes.
- SUPPORT waitaminute.VariableNotNone :: raised when a second root signal is declared.

## core.control_flow.ControlFlow
File: src/worktoy/core/control_flow/_control_flow.py
Kind: signal (root)

`class ControlFlow(Exception, metaclass=MetaFlow, _root=True)`: the one
root signal. Its MRO is `ControlFlow, Exception, BaseException, _Chill,
object`. It adds nothing; being the registered root is its role.

Recommendations: none.

- EDGE meta core.control_flow.MetaFlow :: derives from :: Built by MetaFlow, which registers it as the root through the _root keyword.

## core.control_flow.SkipSet
File: src/worktoy/core/control_flow/_skip_set.py
Kind: signal

The only signal the library raises itself. A descriptor's `hookPreSet`
raises it to tell `Object.__set__` to skip `__instance_set__` and
`hookOnSet`; the caller sees nothing. The docstring restricts the
recommended use to redundant-set elision.

Recommendations: none.

- EDGE base core.control_flow.ControlFlow :: is based on :: A signal class with an empty body, as ControlSpace requires.
- EDGE use core.Object :: is caught by :: Object.__set__ catches SkipSet raised from hookPreSet and skips the write silently.

## core.ContextInstance
File: src/worktoy/core/_instance_owner.py (lines 16-32)
Kind: descriptor

Non-data descriptor (only `__get__`). On a class it returns itself; on
an `Object` it returns `instance.getContextInstance()`, the top of the
descriptor's context stack. Placed on `Object` as `instance`.

Recommendations:
- RECOMMEND [low, docstring] The docstring says a read with no frame raises `WithoutException`; `Object.getContextInstance` raises a plain `AttributeError` for a value no class holds and `WithoutException` only for a placed descriptor. Say both.

- EDGE use core.Object :: reads the context stack of :: Object.instance is a ContextInstance; __get__ calls Object.getContextInstance on the descriptor it is read from.

## core.ContextOwner
File: src/worktoy/core/_instance_owner.py (lines 35-51)
Kind: descriptor

The owner-side twin: returns `instance.getContextOwner()`. Placed on
`Object` as `owner`.

Recommendations:
- RECOMMEND [low, docstring] Same as `ContextInstance`: the docstring names only `WithoutException`, while an unplaced value raises a plain `AttributeError`.

- EDGE use core.Object :: reads the context stack of :: Object.owner is a ContextOwner; __get__ calls Object.getContextOwner.

## core.Object
File: src/worktoy/core/_object.py
Kind: class (descriptor base)

The primitive base of every worktoy value and descriptor, built by
`MetaType` (MRO `Object, _Chill, object`). State, all set with
`object.__setattr__` to bypass any subclass `__setattr__`:
`__field_owner__` and `__field_name__` from `__set_name__`,
`__private_name__` (cache), `__pos_args__` and `__key_args__` captured
by `__init__` from whatever the constructor received, and
`__call_chain__`, a list of `(instance, owner)` frames. Three class
attributes: `directory` (a `utilities.Directory`), `instance`
(`ContextInstance`) and `owner` (`ContextOwner`).

The descriptor protocol. `__set_name__(owner, name, **kw)` records the
pair and calls `hookSetName`. `__get__` on a class returns `self`; on an
instance it pushes a frame, runs `hookPreGet`, `__instance_get__
(instance, owner)`, `_deletedGuard` and `hookOnGet`, and pops in
`finally`. `__set__` pushes `(instance, type(instance))`, runs
`hookPreSet` and, unless that raised `SkipSet`, `__instance_set__` and
then `hookOnSet` with the value `__instance_set__` returned or, when it
returned None, the value as assigned. `__delete__` first reads the old
value through `__instance_get__(..., _deleting=True)` (an
`AttributeError` there gives None), guards it, then `hookPreDelete`,
`__instance_delete__(instance, old)`, `hookOnDelete`. The default hooks
make a bare `Object` in a class body a read-only class attribute:
`__instance_get__` returns `self`, `__instance_set__` raises
`ReadOnlyError`, `__instance_delete__` raises `ProtectedError`. The six
notification hooks are empty.

Context. `createContext` and `exitContext` rebuild the frame list on
each push and pop; `exitContext` on an empty stack raises
`WithoutException`. `getContextInstance` and `getContextOwner` return
the top frame, raise a plain `AttributeError` on a value no class holds
(so `hasattr` works on an unplaced value), and `WithoutException` on a
placed descriptor outside any frame. `hasContext` is the truth of the
list.

Sentinel substitution. `getContextualSentinels` maps `THIS` to the
current instance, `OWNER` to the current owner and `DESC` to `self`,
each falling back to the sentinel itself when no frame is active.
`filterSentinels` looks an argument up in that dict (an unhashable
argument is returned as is), `getPosArgs` and `getKeyArgs` apply it to
the captured constructor arguments, and `hasSentinelArgs` reports
whether any captured argument is one of the three, by identity.

`_deletedGuard` turns a `DELETED` value into `MissingVariable` naming
the field. `getPrivateName` converts the camelCase field name into
`__snake_case__` with the one compiled regular expression of the
library and caches it. `parseKwargs` is a classmethod that pulls the
first of several keys out of keyword arguments, checking the value
against the types given (a wider number type admits the narrower ones,
`bool` passes as `int`), returning the value and the remaining
keywords, or `(None, kwargs)` when no key is present, and raising
`TypeException` when a key is present with the wrong type.

Recommendations:
- RECOMMEND [low] `getContextInstance` and `getContextOwner` each hold an unreachable branch: `hasContext()` is the truth of `__call_chain__`, so the `MissingVariable` raised when the chain is None inside that branch can never fire. Drop the two branches.
- RECOMMEND [low, message] `_deletedGuard` raises `MissingVariable(instance, '__field_name__', str)` when the descriptor has no field name, naming the instance as the object missing the variable; the variable missing is the descriptor's own, so `self` is the right first argument, as `getPrivateName` passes.

- EDGE meta core.MetaType :: derives from :: Built by MetaType, which appends _Chill and records the namespace.
- EDGE use core.ContextInstance :: exposes as 'instance' :: The instance attribute is a ContextInstance that reads the top of the context stack.
- EDGE use core.ContextOwner :: exposes as 'owner' :: The owner attribute is a ContextOwner that reads the top of the context stack.
- EDGE use core.sentinels.THIS :: substitutes with the instance :: getContextualSentinels maps THIS to the active instance for deferred arguments.
- EDGE use core.sentinels.OWNER :: substitutes with the owner :: getContextualSentinels maps OWNER to the active owner class.
- EDGE use core.sentinels.DESC :: substitutes with itself :: getContextualSentinels maps DESC to the descriptor.
- EDGE use core.sentinels.DELETED :: translates into MissingVariable :: _deletedGuard raises MissingVariable when __instance_get__ returns DELETED.
- EDGE use core.control_flow.SkipSet :: catches in __set__ :: A SkipSet from hookPreSet skips __instance_set__ and hookOnSet.
- SUPPORT utilities.Directory :: the 'directory' class attribute, resolving the owner's source directory.
- SUPPORT utilities.maybe :: fallbacks throughout (stored value, empty chain, captured args).
- SUPPORT waitaminute.MissingVariable :: raised for a DELETED read and for a missing field name in getPrivateName.
- SUPPORT waitaminute.TypeException :: raised by parseKwargs and by getPrivateName on a non-string cache.
- SUPPORT waitaminute.desc.WithoutException :: raised for a context read outside any frame and for an unpaired exitContext.
- SUPPORT waitaminute.desc.ReadOnlyError :: the default __instance_set__.
- SUPPORT waitaminute.desc.ProtectedError :: the default __instance_delete__.

---

## dispatch (package)
File: src/worktoy/dispatch/__init__.py
Kind: package

Load order: `flexCall` and `isFlex`, `CallMeMaybe`, `Permuter`,
`PermuterMethod`, `TypeSig`, `Dispatcher`, `overload`. The docstring is
explicit that this is machinery, not a ready-made facility: `overload`
only records signatures, and `BaseMeta` in `mcls` compiles them into a
`Dispatcher` during class construction. `dispatch` imports from `core`
(`Object`, the sentinels) and never from `desc` or `mcls`.

Recommendations: none.

## dispatch.isFlex
File: src/worktoy/dispatch/_flex_call.py (lines 215-235)
Kind: function

Reports whether a function carries the `__flex_wrapped__` marker
`flexCall` sets, by `getattr` in a try block. No non-leaf uses.

Recommendations: none.

## dispatch.flexCall
File: src/worktoy/dispatch/_flex_call.py (lines 238-355)
Kind: function

Wraps a plain function so that surplus positional arguments are dropped
at the declared positional count, and a missing required positional
parameter (one with no default, not supplied by position or by name)
raises a `TypeError` naming the missing names through the private
helper `_missingNames`. Keyword arguments pass through. The wrapper
copies `__dict__`, name, qualname, module, doc and annotations, sets
`__wrapped__` and the marker. It returns the function itself, not a
wrapper, for an already wrapped function, a `*args` function (code flag
`0x04`), or a dunder. Anything but a `types.FunctionType` is refused
with `TypeException`. Positional-only parameters named by keyword pass
the check here and fail in the wrapped function. The docstring names
its two users: the notification callbacks of `BaseDescriptor` in
`desc`, and every plain function in a class body whose namespace
declares `FlexCallHook` in `mcls`; both are recorded as edges from
those items.

Recommendations: none.

- SUPPORT utilities.joinWords :: renders the missing names.
- SUPPORT utilities.textFmt :: formats the error text.
- SUPPORT waitaminute.TypeException :: raised for a non-function.

## dispatch._Wrapped
File: src/worktoy/dispatch/_call_me_maybe.py (lines 20-33)
Kind: descriptor (private)

A `utilities.QuickDesc` subclass, generic in the wrapped type, whose
`__get__` reads the one-tuple stored under the private key on the
instance and returns its first element, so `CallMeMaybe.__wrapped__`
hands out the function unbound. A missing tuple raises
`MissingVariable`, a non-tuple `TypeException`. On the class it returns
itself.

Recommendations: none.

- EDGE use dispatch.CallMeMaybe :: serves '__wrapped__' on :: CallMeMaybe declares __wrapped__ as a _Wrapped over '__function_case__', so reads give the function without descriptor binding.
- SUPPORT utilities.QuickDesc :: the base class; its private-key bookkeeping and read-only refusals.
- SUPPORT waitaminute.MissingVariable :: unset key or unset tuple.
- SUPPORT waitaminute.TypeException :: key or storage of the wrong type.

## dispatch.CallMeMaybe
File: src/worktoy/dispatch/_call_me_maybe.py (lines 36-194)
Kind: class (callable wrapper)

Holds one function and forwards calls to it. The function lives in
`__function_case__` as a one-tuple so that reading it never triggers
`FunctionType.__get__`; `_getWrappedFunction` unpacks it and
`setFunction` packs it. `__init__` accepts an optional callable and
refuses a non-callable with `TypeException`. `__call__` fetches the
function and hands it to `invoke(func, *args, **kwargs)`, the one hook
subclasses override. It is deliberately not a descriptor: `__set_name__`
raises `TypeError`, so an instance cannot sit in a class body; it is
meant to be held inside a `Dispatcher` registry. `__getattr__` forwards
unknown attribute reads to the wrapped function, guarding its own two
storage names against recursion, and falls back to
`object.__getattribute__` so a genuinely missing attribute still
raises. Not based on `Object`.

Recommendations: none.

- EDGE use dispatch._Wrapped :: exposes the function through :: The class attribute __wrapped__ is a _Wrapped reading the one-tuple, which __getattr__ also goes through.
- SUPPORT utilities.textFmt :: the __set_name__ refusal text.
- SUPPORT waitaminute.MissingVariable :: calling before a function is set.
- SUPPORT waitaminute.TypeException :: a non-callable given to __init__.

## dispatch.Permuter
File: src/worktoy/dispatch/_permuter.py
Kind: class (callable wrapper)

A `CallMeMaybe` holding a `utilities.combinatorics.Arrangement`.
Received positional arguments are in the arrangement's `values` order;
`invoke` runs `arrangement.restoreFrom(*args)` to put them back into
the canonical `items` order before calling the function. The
constructor takes at most two positional arguments, a `FunctionType`
and an `Arrangement` in either order, refusing a third, a duplicate of
either kind (`ValueError`) and anything else (`TypeException`); the
function goes to `CallMeMaybe.__init__`, the arrangement to
`setArrangement`, which is write-once (`WriteOnceError`) and typed. The
`arrangement` attribute is a `QuickDesc`. `newArrangement` builds a new
`Permuter` over the same function; `<<` does the same, `<<=` sets in
place, and `>>` reflected delegates to `<<`. Keeps the inherited
refusal of `__set_name__`.

Recommendations:
- RECOMMEND [low] The constructor accepts the function only as a `types.FunctionType`, while `CallMeMaybe.__init__` accepts any callable, so a `Permuter` cannot wrap a builtin or a bound method that `CallMeMaybe` would. Either accept any callable or state the narrower contract in the docstring.

- EDGE base dispatch.CallMeMaybe :: is based on :: Inherits the one-tuple storage, __call__ and __getattr__ forwarding, overriding invoke to restore the argument order.
- SUPPORT utilities.combinatorics.Arrangement :: the permutation and its restoreFrom.
- SUPPORT utilities.QuickDesc :: the read-only 'arrangement' attribute.
- SUPPORT utilities.textFmt :: error texts.
- SUPPORT waitaminute.TypeException :: wrong constructor argument or arrangement type.
- SUPPORT waitaminute.MissingVariable :: invoking before an arrangement is set.
- SUPPORT waitaminute.desc.WriteOnceError :: a second arrangement.

## dispatch.PermuterMethod
File: src/worktoy/dispatch/_permuter_method.py
Kind: class (callable wrapper)

A `Permuter` whose `invoke(func, instance, *args, **kwargs)` forwards
the calling instance first and the restored arguments after it, so it
can stand in a `Dispatcher` registry where every function is called as
`func(instance, *args)`. This is what `overload.flex` and
`Dispatcher.flex` register, one per arrangement of the declared types.

Recommendations: none.

- EDGE base dispatch.Permuter :: is based on :: Same arrangement machinery; only invoke changes, to pass the instance ahead of the restored arguments.

## dispatch.TypeSig
File: src/worktoy/dispatch/_type_sig.py
Kind: class (dispatch key)

An ordered tuple of types used as a dispatch key. It keeps two tuples:
`__raw_types__`, what it dispatches on, and `__declared_types__`, what
it was written with; `swapTHIS` rewrites the former in place (a
trailing `ARGS[THIS]` becomes `ARGS[cls]`) and `restoreTHIS` copies the
latter back. `__allow_flex__` (default True) says whether the cast
passes of the dispatcher may try it. Hash is the hash of the raw tuple;
equality is identity per entry, with an `ARGS` entry compared by its
inner type; `in` is identity; `len` and iteration go over the raw
types. `fromArgs(*args)` builds the key of a call from the argument
types. `validateTypes(*types, variadic=True)` refuses a non-class entry
with `TypeException` (the test is that the entry's type is a metaclass,
since `isinstance(list[int], type)` is True on 3.9 and 3.10), refuses
`OWNER` with `TypeError`, probes `isinstance(None, entry)` so an entry
`isinstance` cannot take (such as `typing.Any`) fails at declaration,
and allows a trailing `ARGS` only when `variadic` is True. `namesTHIS`
reports a `THIS` entry or `ARGS[THIS]`. `__call__(this, owner)` returns
a substituted copy carrying the same flex flag; its docstring says
`Dispatcher._copySig` relies on it, but `_copySig` as read rebuilds
from the declared types directly and never calls the signature.
`__str__` renders `<TypeSig: [int, str]>` and `__repr__`
`TypeSig(int, str)`, an `ARGS` entry in subscript form. Not based on
`Object`.

Recommendations:
- RECOMMEND [low, docstring] The `__call__` docstring says `Dispatcher._copySig` relies on the no-argument copy; `_copySig` rebuilds from the declared types and never calls the signature. The caller that does rely on it is `LoadSpaceHook.setItemPhase`, which registers `sig()` so the `overload` object keeps `THIS`. Name that caller instead.
- RECOMMEND [low, typing] The `HASHABLE` alias is `Union[type, int]`; nothing in the class puts an `int` into a signature, and the entries that are not classes are `ARGS` instances. Make the alias say what the entries are.

- EDGE use core.sentinels.THIS :: stands for the class in :: swapTHIS replaces THIS by the finished class; namesTHIS and __call__ look for it.
- EDGE use core.sentinels.OWNER :: refuses :: validateTypes raises TypeError for OWNER, which has no meaning in a signature; __call__ would substitute it.
- EDGE use core.sentinels.ARGS :: marks the variadic tail of :: An ARGS instance as the last entry is compared by inner type, rendered as ARGS[T], and rebuilt by swapTHIS.
- SUPPORT utilities.textFmt :: error and rendering text.
- SUPPORT waitaminute.TypeException :: a non-class entry.

## dispatch._uniformType
File: src/worktoy/dispatch/_dispatcher.py (lines 32-43)
Kind: function (private)

Returns the one type every entry of a tuple is, by identity, or None.
The exact-type pass uses it on the trailing argument types of a call so
a variadic signature can be looked up by `(prefix length, prefix types,
inner type)` in one dict read.

Recommendations: none.

- EDGE use dispatch.Dispatcher :: keys the exact variadic lookup for :: The compiled dispatch calls it on the tail of the call's argument types before reading the tailed table.

## dispatch.Dispatcher
File: src/worktoy/dispatch/_dispatcher.py (lines 46-1217)
Kind: descriptor (overload registry and compiled dispatch)

Based on `Object` but replacing its whole descriptor entry: `__get__`,
`__set__`, `__delete__` and `__set_name__` are overridden outright, so
the context stack and the notification hooks never run; `Object` gives
it the two field attributes and `__init__`'s argument capture.

Registry. `__sig_funcs__` is a list of `(TypeSig, func)` for concrete
signatures with a parallel `__sig_distances__` (0 for the owning class,
1 for the nearest base, and so on, supplied by `BaseSpace` in `mcls`);
`__variadic_funcs__` and `__variadic_distances__` hold the
`ARGS`-terminated ones. `addSigFunc` first runs `_resolveTHIS` (swap
`THIS` to the owner if already placed), refuses an equal signature with
`DuplicateSignature`, appends and clears the compiled cache;
`addVariadicSigFunc` appends without a duplicate check, since of
several accepting one call the most recent of the nearest class wins.
`setFallbackFunction` and `setFinalizerFunction` require a callable and
refuse a second one with `DuplicateSignature` carrying the role name.
The decorator methods `overload(*types, strict=None)`, `flex(*types)`,
`fallback` and `finalize` mirror the `overload` class: each returns the
dispatcher so decorators stack, `_stackedFunction` resolving "the
dispatcher itself" back to the function of the stack through
`__latest_func__`. `overload` validates through `TypeSig.validateTypes`,
sets `__allow_flex__` False for a `THIS` signature unless
`strict=False`, and routes a trailing `ARGS` to the variadic list.
`flex` builds a `PermuterMethod` per `Arrangements(*types)` entry with
the cast disabled.

Compiled dispatch. `_createCachedFunction` precomputes: the exact map
(`_getExactFuncMap`, where a nearer variadic that covers a concrete
signature exactly, per `_coversExactly`, takes its function), the two
exact variadic tables and prefix lengths (`_getExactVariadics`, ranked
by distance then most recent), the `isinstance` order of variadics
(nearest first), the cast orders (farthest first, `_getCastOrder` and
`_getVariadicOrder(False)`), and the keyword bindings
(`_getKeywordBindings`: per concrete registration with a readable
`__code__`, the parameter names the signature covers, the optional
names after them, whether `**kwargs` is taken, the types, the target
and the flex flag; a `PermuterMethod` is unwrapped to its function and
listed once with its canonical `arrangement.items`, `THIS` in those
items replaced by the owner since `swapTHIS` only rewrites the
`TypeSig`). The closure `dispatch(instance, *args, **kwargs)` then
runs: keyword calls through `bindKeywords` and `keywordDispatch` (exact
type, then `isinstance`, then cast where allowed, in registration
order), else the exact-map read, the exact variadic read, FAST
concrete, FAST variadic, SLOW concrete, SLOW variadic, the fallback,
else `DispatchException`. A `TypeError` from hashing an argument's
class skips the exact reads. `castArg` goes through `typeCast` and
refuses to call the owning class on the sole argument of an `__init__`
dispatch, since that would be the call being dispatched. The finalizer
runs in `finally`, its own exception chained from the call's. The
compiled function takes the field name, the owner's qualname and
module, and the docstring of the first registered function
(`_getDocumentedFunction`). `_getCachedFunction` builds lazily with the
`_recursion` sentinel pattern.

Placement. `__set_name__` records name and owner and runs `swapAllTHIS`
over every signature. `__get__` first runs `_adoptOwner`, which names a
dispatcher installed with `setattr` after the class along the owner's
MRO whose `__dict__` holds it, then returns the compiled function on
class access and a fresh `MethodType` on instance access, storing
nothing on the instance. `__set__` raises `ReadOnlyError`, `__delete__`
`ProtectedError`. `clone` copies every signature through `_copySig`
(same raw and declared types and flex flag) with the distances, and
shares the fallback and finalizer; `restoreTHIS` puts the sentinel back
in every signature so a clone placed on a subclass resolves `THIS` to
that subclass. `__str__` lists the declared signatures under the
owner and field name.

Recommendations:
- RECOMMEND [medium] `addVariadicSigFunc` is public and says the trailing `ARGS` is not validated; a signature registered through it without one reaches `_getExactVariadics` and the variadic passes, which read `raw[-1].__inner_type__` and fail with a bare `AttributeError` at the first call. Refuse such a signature at registration, as `addSigFunc` refuses a duplicate.

- EDGE base core.Object :: is based on :: Takes the field name and owner storage; overrides __get__, __set__, __delete__ and __set_name__, so the context stack and hooks are out of play.
- EDGE use dispatch.TypeSig :: keys registrations by :: Signatures are TypeSig objects: validated at declaration, swapped and restored for THIS, hashed in the exact map, and built from call arguments with fromArgs.
- EDGE use dispatch.PermuterMethod :: registers for flex :: flex wraps the function in one PermuterMethod per arrangement; keyword bindings unwrap it to the canonical function and items.
- EDGE use dispatch._uniformType :: reads the call tail through :: The exact variadic lookup needs the one type the trailing arguments share.
- EDGE use core.sentinels.ARGS :: detects variadic signatures by :: A trailing ARGS entry routes a signature to the variadic list; its inner type is read in every variadic pass.
- EDGE use core.sentinels.THIS :: resolves to the owner :: _resolveTHIS and swapAllTHIS replace THIS once placed; keyword bindings replace it in flex items.
- SUPPORT utilities.maybe :: fallbacks for the registry lists.
- SUPPORT utilities.typeCast :: the cast passes, with allowInstantiation controlled per argument.
- SUPPORT utilities.textFmt :: the __str__ text.
- SUPPORT utilities.combinatorics.Arrangements :: every ordering of the flex types.
- SUPPORT waitaminute.TypeException :: a non-callable fallback or finalizer.
- SUPPORT waitaminute.MissingVariable :: compiling before placement, or a stack with no function.
- SUPPORT waitaminute.desc.ReadOnlyError :: __set__.
- SUPPORT waitaminute.desc.ProtectedError :: __delete__.
- SUPPORT waitaminute.dispatch.DispatchException :: no overload matched; it renders by reading the dispatcher's owner, name and declared signatures.
- SUPPORT waitaminute.dispatch.DuplicateSignature :: a repeated concrete signature, fallback or finalizer.

## dispatch.overload
File: src/worktoy/dispatch/_overload.py
Kind: class (decorator factory and signature record)

The user-facing decorator. `overload(*types, strict=None)` is a call of
`__new__`, which refuses any keyword but `strict`
(`_refuseKeywords`), validates the entries through
`TypeSig.validateTypes`, and returns a decorator function, not an
instance (so `__init__` does nothing and never runs for that path).
Applying the decorator builds a `TypeSig`, sets `__allow_flex__` False
when `strict` is True or, by default, when the signature names `THIS`,
and either extends an `overload` instance already on the function
(`_extendLatest`, so stacked decorators register one function under
several signatures) or refuses a staticmethod, classmethod or
non-callable (`_refuseMethodKinds`) and creates the instance through
`super().__new__` with `_root=True` semantics. `_addSigFunc` puts a
trailing-`ARGS` signature in `__variadic_sig_func_list__` and every
other in `__sig_func_dict__`, where an equal signature stacked again
keeps its first place, and records `__latest_func__`. The classmethods
`flex` (one `PermuterMethod` per `Arrangements(*types)` entry, cast
disabled, `__latest_func__` reset to the function itself), `fallback`
and `finalize` go through `_stackOn`, which reuses the overload from a
decorator below or makes a fresh root instance. `__iter__` yields the
concrete pairs, `getVariadics` the variadic ones, `isFallback`,
`getFallback`, `isFinalizer`, `getFinalizer` the roles. `__getattr__`
forwards to the latest function, else the fallback, else raises
`MissingVariable`. `__str__` lists every role. Nothing here dispatches:
`LoadSpaceHook` and `BaseSpace` in `mcls` read these records into a
`Dispatcher`. Not based on `Object`.

Recommendations: none.

- EDGE use dispatch.TypeSig :: records signatures as :: Each decorator builds a TypeSig, validates it, and keys the registry by it.
- EDGE use dispatch.PermuterMethod :: registers for flex :: overload.flex stores one PermuterMethod per arrangement so the caller may pass the typed arguments in any order.
- EDGE use core.sentinels.ARGS :: separates variadic signatures by :: A trailing ARGS entry goes to the variadic list instead of the concrete dict.
- SUPPORT utilities.maybe :: empty registry fallbacks.
- SUPPORT utilities.textFmt :: __str__ text.
- SUPPORT utilities.combinatorics.Arrangements :: every ordering of the flex types.
- SUPPORT waitaminute.MissingVariable :: attribute forwarding with no function.
- SUPPORT waitaminute.TypeException :: a staticmethod, classmethod or non-callable decorated.

---

## desc (package)
File: src/worktoy/desc/__init__.py
Kind: package

Load order: `_RootAlias` (private, first, since both boxes need it),
`FastBox`, `BaseDescriptor`, `Alias`, `Field`, `AttriBox`, `FixBox`,
`SymbolicName`. The docstring describes the descriptor context that
`Object` in `core` supplies and the pickling rule of a placed box.
`desc` imports from `core` and from `dispatch` (`flexCall` only), never
from `mcls`.

Recommendations: none.

## desc._RootAlias
File: src/worktoy/desc/_root_alias.py
Kind: class (private, typing alias)

A subclass of `typing._GenericAlias` declared with `_root=True`. When a
box is subscripted with anything but a plain class (a `TypeVar`, as in
`class Sub(AttriBox[T])`, or `list[int]`), the generic machinery hands
back a plain alias, which a class body would store silently. `fromAlias`
rebuilds that alias as a `_RootAlias` (origin, args, `_name`, `_inst`),
and `copy_with` keeps the class through the copies `typing` makes while
substituting type variables. `__set_name__` raises `PhantomBoxError`
naming owner and attribute, so binding the alias in a class body fails
as the class is created; `__get__` raises it too for an alias installed
with `setattr`. A base-class entry is not a namespace value, so
`class FixBox(AttriBox[T])` passes through `__mro_entries__` untouched.

Recommendations:
- RECOMMEND [note] The class reaches into private `typing` internals (`_GenericAlias`, `_name`, `_inst`, `copy_with`) that have shifted between Python 3.7 and 3.14. The floor and ceiling test runs are what guard it; keep both running whenever this file changes.

- SUPPORT waitaminute.desc.PhantomBoxError :: raised on binding or reading the alias.

## desc.FastBox
File: src/worktoy/desc/_fast_box.py
Kind: descriptor

A lean typed attribute not based on `Object`: no context, no hooks, no
sentinel substitution. `__class_getitem__` makes a fresh instance
carrying the field type when the subscript's type is a metaclass, else
forwards to `Generic` and re-clothes the result as a `_RootAlias`
(`TypeException` if even that fails). `__call__` captures default
arguments. `__set_name__` refuses a missing field type with
`MissingVariable` and sets the storage key `__fast_<name>__`. `__get__`
reads `instance.__dict__` directly and on a `KeyError` builds the
default through `_build` and stores it; `__set__` requires an instance
of the field type (`TypeException` otherwise), no casting; `__delete__`
removes the key, `MissingVariable` if absent, so the next read rebuilds.
`_build` follows the `AttriBox` rules: a builtin container refuses a
lone text argument, a number field (by `castRule`) casts a lone argument
through `typeCast` (`_castNumber`), `_callFieldType` tries the field
type on the arguments as separate and, for the five builtin containers
and no keywords, once more with the arguments as one iterable, and the
result must be an instance of the field type.

Recommendations:
- RECOMMEND [low] `__get__`, `__set__` and `__delete__` read `instance.__dict__` directly, so an owner with `__slots__` and no `__dict__` fails with the interpreter's bare `AttributeError`, where `AttriBox._store` raises `MissingInstanceDict` naming the field. Raise the same exception here for the same owner.

- EDGE use desc._RootAlias :: re-clothes non-class subscripts as :: __class_getitem__ returns _RootAlias.fromAlias for a TypeVar or parametrized generic so a class-body binding is refused.
- SUPPORT utilities.typeCast :: lone number defaults.
- SUPPORT utilities.castRule :: whether the field type is held to a number rule.
- SUPPORT waitaminute.TypeException :: wrong value type, refused default, bad subscript.
- SUPPORT waitaminute.MissingVariable :: no field type, or deleting an unset field.
- SUPPORT waitaminute.dispatch.TypeCastException :: caught from typeCast and re-raised as TypeException.

## desc.BaseDescriptor
File: src/worktoy/desc/_base_descriptor.py
Kind: descriptor (base)

`Object` plus `Generic[T]`, adding the seven callback decorators
`preGet`, `onGet`, `preSet`, `onSet`, `preDelete`, `onDelete` and
`setName`. Each records the callback's `__name__` in a tuple on the
descriptor (`_getCallbackName` refuses a lambda or a nameless callable
with `NamelessCallback`) and returns the callback wrapped by
`flexCall`, so a callback may declare fewer parameters than it is
handed. The `Object` hooks are overridden to look each recorded name up
on `type(instance)` at access time (`_getCallback`, which unwraps a
bound method's `__func__` and wraps with `flexCall` again) and call it
with the instance and the value, in registration order; `hookSetName`
calls each set-name callback as `callback(owner, self)`. Because lookup
is by name on the instance's class, a subclass overrides a callback by
redefining the name. The descriptor behaviour itself is still
`Object`'s: read gives the descriptor, write raises `ReadOnlyError`,
deletion `ProtectedError`. Typing-only `__get__` and `__set__`
overloads are declared under `TYPE_CHECKING`.

Recommendations:
- RECOMMEND [low] `hookSetName` unwraps a bound method's `__func__` by hand and calls the callback as it is, while the six access hooks go through `_getCallback`, which also wraps with `flexCall`. An override of a set-name callback that was never decorated is therefore the one callback not given the flex treatment the class docstring promises. Route it through `_getCallback` too.

- EDGE base core.Object :: is based on :: Keeps Object's __get__, __set__, __delete__ and context stack, overriding the six notification hooks and hookSetName to dispatch by name.
- EDGE use dispatch.flexCall :: wraps callbacks with :: Every decorator returns flexCall(callback), and _getCallback wraps the resolved method again, so surplus positional arguments are dropped.
- SUPPORT utilities.maybe :: empty key tuples.
- SUPPORT waitaminute.desc.NamelessCallback :: a lambda or nameless callable given to a decorator.

## desc.Alias
File: src/worktoy/desc/_alias.py
Kind: descriptor

Re-exposes another attribute under a second name. Based on `Object`
but, like `Dispatcher`, replacing the entry points: `__get__`,
`__set__` and `__delete__` find the real object through
`_getRealObject(owner)`, the first entry under the real name in the
`__dict__` of a class along the owner's MRO (so a staticmethod or
classmethod is seen raw), else `getattr(owner, name)`, and then call the
`__get__`, `__set__` or `__delete__` of the real object's type; a plain
value is returned as is on read, and refused with `ReadOnlyError` or
`ProtectedError` on write or delete. `__set_name__` tries the lookup at
class creation and, when it succeeds, writes the real object into the
owner under the alias name with `setattr`, so the alias removes itself;
then `Object.__set_name__` records owner and name regardless. `__init__`
hands the real name to `Object.__init__` and stores it.

Recommendations: none.

- EDGE base core.Object :: is based on :: Takes the field bookkeeping and argument capture; overrides the three entry points, so the context stack and hooks are out of play.
- SUPPORT waitaminute.desc.ReadOnlyError :: a write through an alias of a non-descriptor.
- SUPPORT waitaminute.desc.ProtectedError :: a deletion through an alias of a non-descriptor.

## desc.Field
File: src/worktoy/desc/_field.py
Kind: descriptor

A property-like descriptor whose accessors are methods decorated below
it in the class body. `GET` records one getter name (a second replaces
it), `SET` and `DELETE` record any number, all through
`_getCallbackName`, so a lambda is refused. `__instance_get__` looks
the getter name up on the `owner` passed to `__get__` and calls it with
the instance (`AccessError` when no getter was registered); a read made
with `_deleting=True` goes to `_peekValue`, which swallows anything the
getter raises and returns None. `__instance_set__` calls every setter
on `type(instance)` with the value, or raises `ReadOnlyError` with none;
`__instance_delete__` calls every deleter, or raises `ProtectedError`
carrying the old value. `__init__(other)` copies the accessor and
callback name tuples from another `Field`, refusing anything else with
`TypeException`. Name-based lookup means a subclass changes what an
inherited `Field` returns just by redefining the getter's name.

Recommendations: none.

- EDGE base desc.BaseDescriptor :: is based on :: Reuses the name-recording helper and the notification hooks; implements the three __instance_ methods by name lookup.
- SUPPORT utilities.maybe :: empty key tuples.
- SUPPORT waitaminute.TypeException :: a non-Field passed to __init__, or a non-string getter key.
- SUPPORT waitaminute.desc.AccessError :: a read with no getter.
- SUPPORT waitaminute.desc.ReadOnlyError :: a write with no setter.
- SUPPORT waitaminute.desc.ProtectedError :: a deletion with no deleter.

## desc.AttriBox
File: src/worktoy/desc/_attri_box.py
Kind: descriptor (typed, lazily built attribute)

Declared as `x = AttriBox[T](*args, **kwargs)`. `__class_getitem__`
makes a fresh instance of the box class with `__field_type__` set when
the subscript is a plain class (test: its type is a metaclass), else
hands the subscript to `Generic` and re-clothes the alias as a
`_RootAlias`. `__call__` captures the deferred default by calling
`Object.__init__` on the instance, refusing with `TypeError` once the
box is placed. `__set_name__` refuses a missing field type with
`MissingVariable`, runs `BaseDescriptor.__init__` for a box written
without the trailing call, delegates to the inherited `__set_name__`
(owner, name, `hookSetName`), then `_refuseStorageCollision` raises
`StorageCollision` when another box of the same class on the owner
derives the same storage name (`fooBar` and `foo_bar` both give
`__foo_bar__attribox_field_object__`, the private name from
`Object.getPrivateName` plus the lower-case box class name).
`fieldType` is a `Field` whose getter is `getFieldType`.

Reading. `__get__` refuses an instance read on a box with no field
type, then defers to `Object.__get__`. `__instance_get__` reads the
storage with `object.__getattribute__`; on `AttributeError` it raises
through when `_deleting`, else builds the default from `getPosArgs` and
`getKeyArgs` (the captured arguments with `THIS`, `OWNER` and `DESC`
substituted from the context) through `_resolve`, stores it, and
re-reads with the `_recursion` guard. `_resolve`: a lone argument
already of the field type is deep-copied per instance (a value that
refuses to copy is shared), unless a sentinel was captured or keywords
are present; a text field type (`str`, `bytes`, `bytearray` or a
subclass) with one argument goes to `resolveText`; a lone number
(`castRule` in `bool`, `int`, `float`, `complex`) to `resolveNumber`;
everything else to `_callFieldType`, where a builtin container takes a
single argument whole, several arguments as its elements, and refuses
lone text. The result must be an instance of the field type
(`TypeException`), and `_applyTags` writes `__field_name__`,
`__field_owner__` and `__field_box__` on it unless it is one of the
arguments, a class, an `Enum` member, an instance of a class with
`__no_box_tag__`, or has no `__dict__`.

Writing. `__instance_set__` stores an instance of the field type as is
and returns it (so `hookOnSet` sees the stored value). A text field
resolves the assigned arguments through `resolveText`. Otherwise
`typeCast(fieldType, value, allowInstantiation=False)` is tried; a
refused cast re-raises a chained `OverflowError`, refuses a non-tuple
for a number field with `TypeException`, and else builds through
`_resolve(*self._assignedArgs(value))`, where an assigned tuple is the
argument list (taken whole for a container) and sentinels are filtered
through `Object.filterSentinels`. `_store` writes with
`object.__setattr__` and turns the `AttributeError` of a slots-only
instance into `MissingInstanceDict`. `__instance_delete__` stores
`DELETED`, which the next read turns into `MissingVariable`.

Copying and pickling. `__copy__` and `__deepcopy__` return the box
itself, so a tagged object or an owner copied deeply keeps naming the
box declared on the class. `__reduce__` pickles a placed box as
`getattr(owner, name)`, and an unplaced one through
`copyreg.__newobj__` with its `__dict__`.

Recommendations:
- RECOMMEND [medium] `_applyTags` writes `__field_name__` and `__field_owner__` onto the object the box created, and those are the very names `Object` uses for its own placement record. A default built from an `Object` subclass (a `BaseObject` instance, say) is thereby marked as placed: `getContextInstance` on it raises `WithoutException` instead of the plain `AttributeError` meant for a value no class holds, and `getPrivateName` answers with the field's name. Either document the overlap as intended or give the tags names of their own; the tags themselves are a feature other code relies on, so this is about the names, not their presence.
- RECOMMEND [low] The rule for text and for numbers differs: `_isNumberField` uses `castRule`, so a number subclass with a constructor of its own is trusted, while `_isTextField` uses `issubclass`, so a `str` subclass with a constructor of its own is still sent through `resolveText` and never reaches that constructor for a single argument. Use `castRule` for the text types as well, or state the asymmetry.
- RECOMMEND [low, message] `_callFieldType` raises `TypeException('value', ...)` with the literal name `value`, where `resolveText`, `resolveNumber` and `_resolve` name the field. Name the field here too.

- EDGE base desc.BaseDescriptor :: is based on :: Takes the callback decorators and the Object protocol; implements the three __instance_ methods over per-instance storage.
- EDGE use desc.Field :: exposes 'fieldType' through :: The class attribute fieldType is a Field whose GET is getFieldType.
- EDGE use desc._RootAlias :: re-clothes non-class subscripts as :: __class_getitem__ returns _RootAlias.fromAlias for a TypeVar or parametrized generic.
- EDGE use core.Object :: captures the default through :: __call__ runs Object.__init__ on the box to stash the deferred arguments; getPosArgs, getKeyArgs, filterSentinels, hasSentinelArgs and getPrivateName are read from it.
- EDGE use core.sentinels.DELETED :: marks deletion with :: __instance_delete__ stores DELETED under the storage name.
- EDGE use core.sentinels.THIS :: substitutes in the default :: A captured THIS becomes the instance when the default is built, and suppresses the lone-argument copy.
- EDGE use core.sentinels.OWNER :: substitutes in the default :: A captured OWNER becomes the owner class when the default is built.
- EDGE use core.sentinels.DESC :: substitutes in the default :: A captured DESC becomes the box itself when the default is built.
- SUPPORT utilities.typeCast :: lossless casts on assignment and in resolveText and resolveNumber.
- SUPPORT utilities.castRule :: whether the field type is held to a number rule.
- SUPPORT utilities.textFmt :: the refusal of a call on a placed box.
- SUPPORT waitaminute.TypeException :: refused values, constructor results of the wrong type, bad subscripts.
- SUPPORT waitaminute.MissingVariable :: no field type.
- SUPPORT waitaminute.desc.MissingInstanceDict :: storing on a slots-only instance.
- SUPPORT waitaminute.desc.StorageCollision :: two boxes deriving one storage name.
- SUPPORT waitaminute.dispatch.TypeCastException :: caught from typeCast.

## desc.FixBox
File: src/worktoy/desc/_fix_box.py
Kind: descriptor (write-once box)

`class FixBox(AttriBox[T])`: the `TypeVar` subscript goes through the
generic path of `__class_getitem__`, so the base entry is a
`_RootAlias` whose `__mro_entries__` resolves to `AttriBox`.
`__instance_set__` reads the storage with `object.__getattribute__` and
raises `WriteOnceError` when anything is there (so the lazily built
default consumes the one write), else delegates to
`AttriBox.__instance_set__`. `__instance_delete__` calls
`Object.__instance_delete__` directly, which raises `ProtectedError`.

Recommendations: none.

- EDGE base desc.AttriBox :: is based on :: Same storage, casting and tagging; only the write-once check and the deletion refusal are added.
- EDGE use core.Object :: refuses deletion through :: __instance_delete__ calls Object.__instance_delete__ by name, which raises ProtectedError.
- SUPPORT waitaminute.desc.WriteOnceError :: a second write.

## desc.SymbolicName
File: src/worktoy/desc/_symbolic_name.py
Kind: class (value, Object-based)

Holds a tuple of words and renders them as `snake`, `pascal`, `camel`,
`kebab`, `screamingSnake` and `screamingKebab`, each a `Field` with a
`GET` method, `words` a `Field` too (raising `MissingVariable` when
unset). `__init__` refuses a non-string word with `TypeException` and
does not call `Object.__init__`. Supports `bool`, `len`, iteration,
indexing by `int` and `slice` (`TypeException` otherwise), `in`,
`__str__` and `__repr__`. Equality and hash use the lower-cased words,
so two names of the same words in different case are one key. Being an
`Object`, an instance placed in a class body is a read-only class
attribute.

Recommendations: none.

- EDGE base core.Object :: is based on :: Inherits the data-descriptor protocol, which makes a name in a class body a shared read-only attribute.
- EDGE use desc.Field :: renders through :: Seven Field attributes, each with a GET-decorated getter, give the words and the six renderings.
- SUPPORT utilities.textFmt :: __str__ and __repr__.
- SUPPORT waitaminute.MissingVariable :: words read before any were set.
- SUPPORT waitaminute.TypeException :: a non-string word or a bad subscript.

---

## mcls (package)
File: src/worktoy/mcls/__init__.py
Kind: package

Load order: the `space_hooks` subpackage first (its hooks are declared
in the namespace class bodies), then `AbstractNamespace`,
`AbstractMetaclass`, `BaseSpace`, `BaseMeta`, `BaseObject`. The
docstring states the pattern: the metaclass returns a namespace object
from `__prepare__`, the namespace's `compile` produces the dict handed
to `type.__new__`, per-name validation happens during the class body
through hooks, and each base's `__subclasshook__` is called with the
new class. `mcls` imports from `core`, `dispatch` and (nothing from)
`desc`; it is the top of the non-leaf stack.

Recommendations: none.

## mcls.space_hooks (package)
File: src/worktoy/mcls/space_hooks/__init__.py
Kind: package

Load order: `SpaceDesc`, `ReservedNames`, `AbstractSpaceHook`,
`FlexCallHook`, `ReservedNamespaceHook`, `NamespaceHook`,
`LoadSpaceHook`. A hook is declared in a namespace class body and opts
into the phases prepare, set-item, get-item, pre-compile, post-compile
and new-class.

Recommendations: none.

## mcls.space_hooks.SpaceDesc
File: src/worktoy/mcls/space_hooks/_space_desc.py
Kind: descriptor

A non-data descriptor, generic in the namespace type, that returns the
`__space_object__` of the hook it is read from, or itself on the class.
`AbstractSpaceHook` declares it as `space`.

Recommendations: none.

- EDGE use mcls.space_hooks.AbstractSpaceHook :: reads the bound namespace of :: __get__ returns the hook's __space_object__, the namespace the hook was last bound to.

## mcls.space_hooks.ReservedNames
File: src/worktoy/mcls/space_hooks/_reserved_names.py
Kind: descriptor

A non-data descriptor returning the tuple of fourteen names the
interpreter sets itself (`__dict__`, `__weakref__`, `__module__`,
`__annotations__`, `__match_args__`, `__doc__`, `__name__`,
`__qualname__`, `__firstlineno__`, `__static_attributes__`,
`__classcell__`, `__classdictcell__`, `__orig_bases__`,
`__type_params__`), or itself on the class. No non-leaf user but
`ReservedNamespaceHook`.

Recommendations: none.

## mcls.space_hooks.AbstractSpaceHook
File: src/worktoy/mcls/space_hooks/_abstract_space_hook.py
Kind: descriptor (hook base)

Based on `Object`, with the entry points replaced: `__get__` on a
namespace instance binds `__space_object__` to that instance and
returns the hook itself (one hook object serves every namespace of its
class, re-bound before each call), and on the class returns the hook
unchanged; `__set_name__` runs `Object.__set_name__` and then
`owner.addHook(self)`, registering the hook on the namespace class.
`space` is a `SpaceDesc`. The six phase methods are no-ops by default:
`preparePhase(space)`, `getItemPhase(key, value)` (signals only by
raising), `setItemPhase(key, val, old)` returning True to claim the
binding, `preCompilePhase(dict)` and `postCompilePhase(dict)` returning
the dict, and `newClassPhase(cls)` returning the class.

Recommendations:
- RECOMMEND [note] One hook object serves every namespace of its class, and `__get__` rebinds its `__space_object__` on each access. `AbstractNamespace` rebinds before every phase call, so each call sees the right namespace, but a hook method that itself runs a class statement using the same namespace class would come back to a hook bound to the inner namespace. Nothing in the library does that; worth a sentence in the docstring.

- EDGE base core.Object :: is based on :: Takes the field name and owner that __set_name__ records; overrides __get__ and __set_name__, so the context stack is out of play.
- EDGE use mcls.space_hooks.SpaceDesc :: exposes the namespace through :: The 'space' attribute is a SpaceDesc reading __space_object__.
- EDGE use mcls.AbstractNamespace :: registers itself on :: __set_name__ calls the owning namespace class's addHook, so declaring a hook in a namespace body registers it.

## mcls.space_hooks.FlexCallHook
File: src/worktoy/mcls/space_hooks/_flex_call_hook.py
Kind: hook

`postCompilePhase` replaces every `FunctionType` value of the compiled
namespace with its `flexCall` wrapper. No namespace in worktoy declares
it; a namespace opts in by declaring `flexCallHook = FlexCallHook()`.

Recommendations: none.

- EDGE base mcls.space_hooks.AbstractSpaceHook :: is based on :: Implements postCompilePhase alone.
- EDGE use dispatch.flexCall :: wraps class-body functions with :: Each plain function in the compiled namespace is replaced by flexCall(func).

## mcls.space_hooks.ReservedNamespaceHook
File: src/worktoy/mcls/space_hooks/_reserved_namespace_hook.py
Kind: hook

`setItemPhase` raises `ReservedName` when the key is one of the
reserved names and is already present in the namespace, so the
interpreter's own first binding passes and a reassignment fails.
Declared on `AbstractNamespace` as `reservedNameHook`, the first hook
to run.

Recommendations: none.

- EDGE base mcls.space_hooks.AbstractSpaceHook :: is based on :: Implements setItemPhase alone.
- EDGE use mcls.space_hooks.ReservedNames :: reads the reserved names from :: The 'reservedNames' attribute is a ReservedNames descriptor.
- SUPPORT waitaminute.meta.ReservedName :: a reassignment of a reserved name.

## mcls.space_hooks.NamespaceHook
File: src/worktoy/mcls/space_hooks/_name_hook.py
Kind: hook

Declared on `AbstractNamespace` as `nameHook`. `setItemPhase`: a
`__del__` raises `DelException` unless the class keyword `trustMeBro`
is truthy (read from the namespace's keyword arguments); one of the
seventeen routed `__class_*__` names (listed in `_getClassDunders`,
`__class_getitem__` deliberately left out since the interpreter handles
it) raises `ShadowedClassHook` when a metaclass before
`AbstractMetaclass` in the building metaclass's MRO implements the
operation itself (`_getShadowingMetaclass`, `__class_init__` exempt),
and `UnboundClassHook` when bound to a plain function or staticmethod;
a near-miss dunder (`__setname__`, `__get_item__`, `__set_item__`,
`__del_item__`) raises `QuestionableSyntax`. `preCompilePhase` seeds
every routed hook name the class body did not bind with `METACALL`,
unless a class along the lookup order supplies it, in which case a
plain-base function or staticmethod is refused with `UnboundClassHook`
naming the base. This seeding is what lets `AbstractMetaclass` test
each hook against `METACALL` (verified: a `BaseObject` carries all
seventeen names in its `__dict__`).

Recommendations:
- RECOMMEND [low] `_getClassDunders` lists the seventeen routed hook names by hand, and `AbstractMetaclass` implements the same seventeen by hand; nothing ties the two lists together. A test asserting that every name in the list has its operation on `AbstractMetaclass`, and the reverse, would catch a hook added on one side only.

- EDGE base mcls.space_hooks.AbstractSpaceHook :: is based on :: Implements setItemPhase and preCompilePhase.
- EDGE use core.sentinels.METACALL :: seeds routed hooks with :: preCompilePhase writes METACALL under every unbound __class_*__ name so the metaclass routes the operation to its own implementation.
- EDGE use mcls.AbstractMetaclass :: locates in the metaclass MRO :: _getShadowingMetaclass searches the metaclasses before AbstractMetaclass for an implementation of the operation that would shadow the hook (local import).
- SUPPORT waitaminute.meta.QuestionableSyntax :: a near-miss dunder.
- SUPPORT waitaminute.meta.DelException :: __del__ without trustMeBro.
- SUPPORT waitaminute.meta.UnboundClassHook :: a routed hook that is not a classmethod, own or inherited from a plain base.
- SUPPORT waitaminute.meta.ShadowedClassHook :: a routed hook whose operation the metaclass takes over.

## mcls.space_hooks.LoadSpaceHook
File: src/worktoy/mcls/space_hooks/_load_space_hook.py
Kind: hook

Declared on `BaseSpace` as `loadSpaceHook`, the third hook to run.
`setItemPhase`: a value that is not an `overload` raises
`OverloadConflict` when the name already has registrations, else is
noted as a plain name and left to the namespace (so it also notes a
value a later hook of a namespace subclass claims). An `overload` under
a name already bound plainly raises `OverloadConflict`. The first name
an `overload` object is bound to is recorded; a later binding of the
same object under another name in the same body is an alias, and copies
every registration collected under the first name (inherited ones
included) to the new name. Otherwise the fallback and finalizer roles
are recorded, and each concrete and variadic signature is registered as
a copy made by calling the `TypeSig` with no arguments, so the
`overload` object keeps `THIS` and may be bound in another class body.
Every `overload` is claimed (returns True) and never reaches the
namespace dict. `postCompilePhase` builds, for every name the class
body or a class in its lookup order registered anything under and that
the body did not bind plainly, one `Dispatcher` through
`_buildDispatcher`: `addSigFunc` and `addVariadicSigFunc` with the
collected distances, then the fallback and finalizer; a name whose
registrations a plain base definition shadows gets none.

Recommendations: none.

- EDGE base mcls.space_hooks.AbstractSpaceHook :: is based on :: Implements setItemPhase and postCompilePhase.
- EDGE use dispatch.overload :: claims and reads :: Each overload bound in the class body is taken out of the namespace and its signatures, variadics, fallback and finalizer are read into the namespace registries.
- EDGE use dispatch.TypeSig :: copies signatures with :: Calling the signature with no arguments gives the copy registered, so THIS in the overload's own signature is never rewritten.
- EDGE use dispatch.Dispatcher :: builds one per name :: postCompilePhase creates a Dispatcher and feeds it the collected registrations with their distances, the fallback and the finalizer.
- EDGE use mcls.BaseSpace :: records into and collects from :: The hook's space is a BaseSpace; it calls addOverload, addVariadic, addFallback, addFinalizer, addPlainName, addClaimedName and the collect methods.
- SUPPORT waitaminute.meta.OverloadConflict :: a name bound both plainly and to overloads.

## mcls.AbstractNamespace
File: src/worktoy/mcls/_abstract_namespace.py
Kind: namespace

A `dict` subclass used as the class-body namespace. Declares
`reservedNameHook` and `nameHook`; hooks register through `addHook`,
which keeps a per-class list under `__hook_objects__` and refuses a
different hook at a registered field name with `DuplicateHook`;
`classGetHooks` collects the lists along the namespace class's MRO,
de-duplicated, and `getHooks` binds each to the instance. `__init__`
records the metaclass, class name, bases and keyword arguments, resolves
the MRO of the bases with `resolveMRO` (a `TypeError` for inconsistent
bases is re-raised unless `_strictMRO=False`, in which case
`_getLookupOrder` falls back to each base's own order), and runs
`preparePhase`. `__getitem__` reads the dict, falls back to the shadow
space (every assignment ever made, claimed or not), runs each hook's
`getItemPhase` with any exception wrapped in `HookException`, then
raises the `KeyError` for a miss. `__setitem__` records the shadow,
reads the old value, and lets the first hook returning True from
`setItemPhase` claim the binding; otherwise stores. `__delitem__`
removes from both, raises `KeyError` for a name never bound, and
records the deletion of a claimed name (`_isClaimed`: the shadow and
the dict disagree), which `compile` turns into `ClaimedName`.
`compile` runs `preCompile` (hooks' `preCompilePhase` on a fresh dict),
merges the class-body items, runs `postCompile`, adds `__metaclass__`,
`__namespace__` (the namespace itself, which is why `MetaType.__new__`
finds one already present) and `__keyword_arguments__`, and keeps the
result as `__compiled_space__`. `getMROSpace` combines the compiled
spaces of the classes along the lookup order into lists per key, and
`deepGetItem` reads through it. `__str__` and `__repr__` describe the
class statement.

Recommendations: none.

- EDGE use mcls.space_hooks.ReservedNamespaceHook :: declares :: The class attribute reservedNameHook; it runs first on every binding.
- EDGE use mcls.space_hooks.NamespaceHook :: declares :: The class attribute nameHook; it runs second on every binding and seeds METACALL at pre-compile.
- EDGE use mcls.space_hooks.AbstractSpaceHook :: runs the phases of :: getHooks binds every registered hook, and __init__, __getitem__, __setitem__, preCompile and postCompile call the phase methods in order.
- SUPPORT utilities.maybe :: fallbacks for the lazy registries.
- SUPPORT utilities.textFmt :: __str__ text.
- SUPPORT utilities.resolveMRO :: the C3 order of the bases.
- SUPPORT waitaminute.TypeException :: a non-dict given to preCompile.
- SUPPORT waitaminute.meta.HookException :: wraps an exception from getItemPhase.
- SUPPORT waitaminute.meta.DuplicateHook :: two hooks at one field name.
- SUPPORT waitaminute.meta.ClaimedName :: a deleted name a hook had claimed.

## mcls.AbstractMetaclass
File: src/worktoy/mcls/_abstract_metaclass.py
Kind: metaclass

Subclasses `MetaType` and derives from it (MRO `AbstractMetaclass,
MetaType, type, _Chill, object`). Its body annotates the four
metaclass-level defaults `__class_getattr__`, `__class_setattr__`,
`__class_delattr__` and `__class_call__` as `METACALL`, so
`MetaType.__new__` installs `_AnnotationsDescriptor` on it (verified).
`__prepare__` returns an `AbstractNamespace`. `__new__` accepts a plain
dict by copying it into a fresh namespace (so the hooks run), calls
`space.compile()`, builds through `MetaType.__new__`, and hands the
class to each hook's `newClassPhase`, taking a returned class in place
of the built one. `__init__` runs `MetaType.__init__`, then
`__class_init__` when it is not `METACALL`, then every base's
`__subclasshook__` with the class. Every routed operation tests the
class attribute against `METACALL`: `__call__`, `__instancecheck__`,
`__subclasscheck__`, `__str__`, `__repr__`, `__setattr__`,
`__delattr__` fall back to `MetaType`; `__iter__`, `__next__`,
`__setitem__`, `__delitem__` raise the builtin `TypeError` text;
`__bool__` falls back to `__class_len__`, then `__class_iter__`, then
True; `__contains__` and `__len__` fall back to iteration; `__getattr__`
raises `MissingVariable` (an `AttributeError`, so `hasattr` works);
`__hash__` hashes the tuple of the class name, the names of the bases
that are neither `object` nor flagged `__skip_hash__` (which excludes
`_Chill`; verified `hash(BaseObject)` equals the hash of
`('BaseObject', 'Object', 'BaseMeta')`), and the metaclass name.
`__eq__`, `__ne__` and `__getitem__` are deliberately not implemented.
`getNamespace` reads `__namespace__` through `type.__getattribute__`;
`getNamespaceClass` builds a throwaway namespace through `__prepare__`
and returns its type.

Recommendations:
- RECOMMEND [low, docstring] The class docstring shows the default `__class_hash__` as hashing `clsName.__bases__` directly; the implementation first drops `object` and every base flagged `__skip_hash__` (so `_Chill`). Show the rule as implemented.

- EDGE meta core.MetaType :: derives from :: Declared with metaclass=MetaType so metaclasses of this family combine without conflict and class keywords end at _Chill.
- EDGE base core.MetaType :: is based on :: Falls back to MetaType for __new__, __init__, __call__, __str__, __setattr__ and the checks when a hook is METACALL.
- EDGE use mcls.AbstractNamespace :: prepares and compiles :: __prepare__ returns one, and __new__ calls its compile for the dict handed to MetaType.__new__.
- EDGE use mcls.space_hooks.AbstractSpaceHook :: runs newClassPhase of :: After the class exists, each hook of the namespace may replace it.
- EDGE use core.sentinels.METACALL :: routes operations by :: Every __class_*__ hook equal to METACALL falls back to the metaclass's own implementation.
- EDGE use core._Chill :: skips in the class hash :: _skipHash reads the __skip_hash__ flag _Chill carries, so the appended base never enters the hash tuple.
- SUPPORT utilities.maybe :: a hook returning None from newClassPhase keeps the class.
- SUPPORT waitaminute.MissingVariable :: a missing class attribute with no __class_getattr__.

## mcls.BaseSpace
File: src/worktoy/mcls/_base_space.py
Kind: namespace

The namespace of `BaseMeta`; adds `loadSpaceHook` to the two inherited
hooks (verified order: `ReservedNamespaceHook`, `NamespaceHook`,
`LoadSpaceHook`). Keeps the class body's own registrations: concrete
and variadic signatures per name (lists of `(TypeSig, func)`),
fallbacks, finalizers, the plain names, and which name each `overload`
object was first bound to. `addOverload` refuses a different function
under an equal signature with `DuplicateSignature` and ignores the same
function again; `addVariadic` appends; `addFallback` and `addFinalizer`
refuse a different second function. Inheritance is resolved at compile
time: `_getInheritedSpaces(name)` walks the lookup order, stopping at
the first class that `_definesPlainly` holds the name (anything in its
`__dict__` except a `Dispatcher` that a `BaseSpace` built from
registrations, detected by the name being absent from that namespace's
own dict), and collects the `BaseSpace` of each class before that.
`collectOverloads` and `collectVariadics` merge own registrations at
distance 0 and inherited ones at increasing distance, skipping equal
signatures (`_mergeSigFuncs`); `collectFallback` and `collectFinalizer`
take the nearest. `getOverloadNames` lists every name any namespace in
the lookup order registered under. The docstring explains why lists
rather than dicts: a `THIS` signature hashes differently before and
after its class exists.

Recommendations: none.

- EDGE base mcls.AbstractNamespace :: is based on :: Inherits the hook machinery, the shadow space and compile; adds the overload registries.
- EDGE use mcls.space_hooks.LoadSpaceHook :: declares :: The class attribute loadSpaceHook, which fills and reads the registries.
- EDGE use dispatch.TypeSig :: compares registrations by :: Equal signatures are merged nearest-first and refused when the functions differ.
- EDGE use dispatch.Dispatcher :: recognises built ones :: _definesPlainly tells a Dispatcher built from registrations from one written in a class body.
- SUPPORT utilities.maybe :: empty registries.
- SUPPORT waitaminute.dispatch.DuplicateSignature :: a second function under one signature, or a second fallback or finalizer, in one body.

## mcls.BaseMeta
File: src/worktoy/mcls/_base_meta.py
Kind: metaclass

`AbstractMetaclass` with `__prepare__` returning a `BaseSpace`; nothing
else. Its own metaclass is `MetaType` by inheritance (verified MRO
`BaseMeta, AbstractMetaclass, MetaType, type, _Chill, object`).

Recommendations: none.

- EDGE base mcls.AbstractMetaclass :: is based on :: Inherits the whole routed-hook protocol; overrides __prepare__ alone.
- EDGE use mcls.BaseSpace :: prepares :: __prepare__ returns a BaseSpace so overloads are collected and compiled.

## mcls.BaseObject
File: src/worktoy/mcls/_base_object.py
Kind: class (entry point)

`class BaseObject(Object, metaclass=BaseMeta)` with an empty body: the
standard entry point, combining the descriptor protocol of `Object`
with the overload-aware class construction of `BaseMeta`. MRO
`BaseObject, Object, _Chill, object`.

Recommendations: none.

- EDGE base core.Object :: is based on :: Inherits the descriptor protocol and the argument capture.
- EDGE meta mcls.BaseMeta :: derives from :: Built through BaseSpace, so overloads in its subclasses compile into Dispatcher objects.

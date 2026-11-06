# Research notes: the ezdata package of worktoy

Read of 2026-10-20, every line of `worktoy.ezdata` in the import order
of its `__init__`, with `utilities`, `waitaminute` and the non-leaf
packages opened where `ezdata` reaches for them. One entry per item,
appended as soon as the item was read. The format is that of
`research_notes.md`, which covers `core`, `dispatch`, `desc` and
`mcls`; the non-leaf items are referred to by the same `package.Item`
names, so the two files can be joined.

Entry format. Each entry opens with `## ezdata.Item`, then a `File:`
line, a `Kind:` line and prose. Interactions are listed as edge lines,
one per actual use:

- `EDGE base <target> :: <verb phrase> :: <one or two sentences>`
  the item is a class based on the target class
- `EDGE meta <target> :: <verb phrase> :: <one or two sentences>`
  the item is a class derived from the target metaclass
- `EDGE use <target> :: <verb phrase> :: <one or two sentences>`
  any other use of the target by the item
- `SUPPORT <utilities.x or waitaminute.x> :: <what for>`
  a reliance on the support packages
- `Recommendations:` closes the prose of every entry, either as the
  line `Recommendations: none.` or as a list of `- RECOMMEND [severity]`
  lines; severities are `medium`, `low` and `note`, with `docstring`,
  `message` or `typing` added where only text changes. Every behaviour a
  recommendation claims was run and confirmed on Python 3.14.5.

Load order read: `_black_listed_types`, `_ez_field`, `_ez_store`,
`_ez_hook`, `_ez_space`, `_ez_meta`, `_ez_data`, `_fields`.

---

## ezdata (package)
File: src/worktoy/ezdata/__init__.py
Kind: package

Exports `EZField`, `EZStore`, `EZHook`, `EZSpace`, `EZMeta`, `EZData`
and `fields`, after loading the private `_BLACK_LISTED_TYPES` tuple
first. The docstring states the contract: a dataclass-style base with
generated construction, equality, iteration and conversion, a
`__post_init__` hook, hashing on `frozen` and ordering on `ordered`.
The package is built on all four non-leaf packages: `EZField` is a
`BaseObject`, `EZHook` an `AbstractSpaceHook`, `EZSpace` a `BaseSpace`,
`EZMeta` a `BaseMeta`, `EZData` an `Object`; it reads `Field` from
`desc` and `TypeSig` from `dispatch`. It is the canonical example of
the metaclass-plus-hook pattern: the factories that generate the
methods live as classmethods on `EZHook`.

Recommendations: none.

## ezdata._BLACK_LISTED_TYPES
File: src/worktoy/ezdata/_black_listed_types.py
Kind: constant (private)

The tuple `(Alias, Dispatcher)`. `EZHook.setItemPhase` refuses a value
of either type in an EZData class body with `BlackListedType` before
anything else is considered. Both are `Object` subclasses that
override `__get__` directly rather than `__instance_get__`, which is
the test `EZHook._isDescriptor` applies to an `Object`, so without the
list each would be wrapped as a field of its own type (confirmed:
`EZHook._isDescriptor(Alias('x'))` is False). The list is therefore a
patch over that blind spot; see the `EZHook` entry. The two imports are
absolute (`from worktoy.desc import Alias`) where every other module of
the library imports its siblings relatively.

- EDGE use desc.Alias :: lists :: An Alias in an EZData body is refused with BlackListedType.
- EDGE use dispatch.Dispatcher :: lists :: A Dispatcher object written in an EZData body is refused with BlackListedType; one built from overloads at post-compile never passes through setItemPhase.

Recommendations:
- RECOMMEND [low] The list exists because `EZHook._isDescriptor` tests an `Object` by `__instance_get__` and `__instance_set__` alone; see the `EZHook` recommendation to test the entry points instead, after which this list is empty and the module can go.
- RECOMMEND [low] Use relative imports (`from ..desc import Alias`) as the rest of the package does.

## ezdata.EZField
File: src/worktoy/ezdata/_ez_field.py
Kind: descriptor (field declaration)

The per-field record, declared as `x = EZField[T](*args, **kwargs)`. It
is a `BaseObject` with `Generic[T]`, but it is never placed on the
class: `EZHook.setItemPhase` claims it, so Python's `__set_name__`
never runs on it, `EZSpace.registerEZField` writes `__field_name__` by
hand and `EZMeta.__init__` writes `__field_owner__`. The six public
attributes `fieldOwner`, `fieldName`, `fieldType`, `posArgs`, `keyArgs`
and `defaultValue` are `Field` descriptors whose getters raise
`MissingVariable` when unset and `TypeException` when the private slot
holds the wrong type. `__class_getitem__` requires the subscript's
type to be a metaclass (so `list[int]` and a `TypeVar` are refused with
`TypeException`), makes the instance with `cls.__new__` and sets the
type; `__call__` binds the construction arguments and returns the
field, and does so again on a field already registered, replacing the
default. `__init__` stores the two argument buckets and does not call
`Object.__init__`. `fromValue(v)` builds a field of `type(v)` with `v`
as the one argument, the route `EZHook` takes for a bare class-body
value. `clone_` (a classmethod taking the field) and `clone` build an
independent field with the same type and arguments and no name or
owner, which `EZSpace` uses for inherited fields and for a field object
bound a second time.

`_construct(fieldType, name, args, kwargs)` is the one builder for
defaults, used by `defaultValue` and by the default recipes the
generated `__init__` captures: a lone argument already of the field
type is `copy.copy`-ed per instance; a lone argument for a text type
(`issubclass` of `str`, `bytes`, `bytearray`) or a number type
(`castRule` in `bool`, `int`, `float`, `complex`) goes through
`typeCast` in `_castValue`, refused as `TypeException` naming the
field; a lone text argument for a builtin container is refused; else
the field type is called, and its result must be an instance of it.
`__str__` renders `Owner.name: type(args)` and `__repr__`
`EZField[type](args)`, both with placeholders when unbound.

- EDGE base mcls.BaseObject :: is based on :: Takes the Object descriptor protocol and BaseMeta construction; the class is never placed on an owner, so only the attribute storage is exercised.
- EDGE use desc.Field :: exposes its record through :: Six Field attributes with GET-decorated getters give the owner, name, type, arguments and a fresh default.
- SUPPORT utilities.maybe :: placeholders in __str__, __repr__ and the default's name.
- SUPPORT utilities.typeCast :: lone text and number defaults.
- SUPPORT utilities.castRule :: whether the field type is held to a number rule.
- SUPPORT waitaminute.MissingVariable :: an unset owner, name, type or argument bucket.
- SUPPORT waitaminute.TypeException :: a bad subscript, a wrong-typed slot, a refused default or a constructor result of the wrong type.
- SUPPORT waitaminute.dispatch.TypeCastException :: caught from typeCast in _castValue.

Recommendations:
- RECOMMEND [medium] `__class_getitem__` admits any subscript whose type is a metaclass, which `typing.Any` satisfies, and nothing probes whether `isinstance` can take it. `class A(EZData): v = EZField[typing.Any](1)` is accepted and `A()` fails with the interpreter's own `TypeError` from inside `_construct`. Add the `isinstance(None, type_)` probe that `TypeSig.validateTypes` makes, so the class statement refuses it.
- RECOMMEND [low] `__call__` on a field already registered replaces its default without a word, while `AttriBox.__call__` refuses the call once the box is placed. Refuse it once `__field_name__` is set, for the same reason: the field is shared by every instance yet to be built.
- RECOMMEND [low] `_construct` holds text to `issubclass` and numbers to `castRule`, the asymmetry `AttriBox._resolve` has: a `str` subclass with a constructor of its own never reaches that constructor for a lone argument, while an `int` subclass with one is trusted. Decide the rule once for both packages.
- RECOMMEND [low] `clone_` is a classmethod whose first parameter is the field, and `clone` is its instance alias; nothing in the library calls `clone_` by name. One instance method would do.

## ezdata.EZStore
File: src/worktoy/ezdata/_ez_store.py
Kind: descriptor

A small data descriptor (`__get__` and `__set__`, no `__delete__`) that
reads and writes `instance.__dict__[fieldName]`. `EZHook.storeFactory`
installs one at a field's name only when a data descriptor further
along the method resolution order would otherwise take the name over
from the instance dict, such as `Object.directory` or a `Field` on a
mixin. Read through the class it returns itself; read on an instance
that never received a value (one made by `__new__` alone) it raises
`MissingVariable`. Not based on `Object`, so it is a plain class
attribute and not itself a worktoy value.

- SUPPORT waitaminute.MissingVariable :: a read on an instance holding no value.

Recommendations: none.

## ezdata._unorderable
File: src/worktoy/ezdata/_ez_hook.py (lines 37-46)
Kind: function (private)

Returns `NotImplemented` unconditionally. `EZHook.postCompilePhase`
installs it as `__lt__`, `__le__`, `__gt__` and `__ge__` on every
class not declared `ordered`, so the interpreter raises its standard
`TypeError` and an ordered base's comparisons are shadowed. `_qualify`
leaves its name alone since it is shared.

Recommendations: none.

## ezdata.EZHook
File: src/worktoy/ezdata/_ez_hook.py (lines 49-1051)
Kind: hook (code generator)

The one hook `EZSpace` adds to the three it inherits from `BaseSpace`
(confirmed order: `ReservedNamespaceHook`, `NamespaceHook`,
`LoadSpaceHook`, `EZHook`). Every generated method is a classmethod
factory on this class.

`setItemPhase`, in order: a value of a blacklisted type raises
`BlackListedType`; a key in `EZSpace.__reserved_ez_methods__` raises
`ReservedMethodError` and one in `__reserved_ez_attributes__`
`ReservedAttributeError`, whatever the value; an interpreter-set name
(`ReservedNames`) passes; an `EZField` is checked by
`_assertCompleteField` (a type and at least one argument bucket, else
`IncompleteFieldException`) and registered through
`EZSpace.registerEZField`, claimed; a Python or builtin function
passes; a class raises `ClassFieldError`; a descriptor passes; a bare
`None` raises `IncompleteFieldException`; anything else is wrapped by
`EZField.fromValue` and registered. `_isDescriptor` calls a non-Object
a descriptor when its type has `__get__` or `__set__`, and an `Object`
a descriptor only when its type overrides `__instance_get__` or
`__instance_set__`.

`postCompilePhase`: writes `__ez_fields__` (the merged mapping from
`EZSpace.getFields`); resolves `__is_frozen__`, `__is_ordered__` and
`__kw_only__` from the class's own keyword arguments through the
inherited `Object.parseKwargs` over the three synonym tuples, coerced
to truth; settles the optional names (`__field_pairs__`, `asDict`,
`asTuple`, `replace`, `__repr__`, `__str__`, `__match_args__`) through
`_settleOptional`, where the class body's own entry wins (a
`Dispatcher` built by `LoadSpaceHook` included, since that hook's
post-compile runs first), then the first hand-written one along the
lookup order (`_findHandWritten`, skipping `object` and names a base
lists in its `__ez_generated__`), else the factory, and records the
generated names in `__ez_generated__`; installs `__init__`, `__iter__`,
`__len__`, `__eq__`, `__delattr__` and the stores from `storeFactory`
unconditionally; on a frozen class `__hash__` and a refusing
`__setattr__`, otherwise `__hash__ = None` and a casting `__setattr__`;
the four comparisons from `orderingFactory` or `_unorderable`; and
`_qualify` sets `__qualname__` of each generated function to
`Owner.name`.

The factories. `initFactory` captures per field its type and a default
recipe closing over `EZField._construct`; the `__init__` applies
positional arguments in order (`ExtraPositionalException` beyond the
field count, `KwargsOnlyException` for any on a keyword-only class),
refuses unknown keywords (`ExtraKeywordException`) and a field given
twice (`RepeatedFieldException`), applies keywords, fills every field
absent from the instance dict with its default, then calls
`__post_init__` looked up on the class. Values are assigned through
`castField` (`typeCast` with the constructor fallback allowed) and
`object.__setattr__`, which is why the frozen `__setattr__` does not
get in the way. `setAttrFactory` casts assignments to field names and
stores others as given; `badSetAttrFactory` and `badDelAttrFactory`
raise `AttributeError`. `iterFactory`, `lenFactory`, `asDictFactory`,
`asTupleFactory`, `fieldPairsFactory`, `strFactory` and `reprFactory`
read `__ez_fields__` and `__kw_only__` from the instance's class at
call time; `replace` rebuilds through `type(self)(**{**asDict(),
**changes})` after refusing unknown names with a plain `TypeError`.
`eqFactory` returns `NotImplemented` for a non-EZData other, False for
a class that is not congruent (`EZMeta.isCongruent`), else compares
the value tuples; `hashFactory` hashes the value tuple;
`orderingFactory(op)` compares value tuples of the same exact class.
`storeFactory` asks `_needsStore` whether the first class along the
lookup order holding the name holds a data descriptor there.

- EDGE base mcls.space_hooks.AbstractSpaceHook :: is based on :: Implements setItemPhase and postCompilePhase; 'space' resolves to the EZSpace under construction.
- EDGE use ezdata.EZField :: claims and wraps :: An EZField in the body is validated and registered; a bare value is wrapped by EZField.fromValue; the default recipes of the generated __init__ call EZField._construct.
- EDGE use ezdata.EZStore :: installs for shadowed fields :: storeFactory creates one per field whose name a data descriptor further along the MRO would take over.
- EDGE use ezdata._BLACK_LISTED_TYPES :: refuses values of :: The first test of setItemPhase raises BlackListedType for an Alias or a Dispatcher.
- EDGE use ezdata._unorderable :: installs on unordered classes :: The four comparison dunders of a class not declared ordered.
- EDGE use ezdata.EZSpace :: records into and reads :: registerEZField, getFields, getKwargs, getClassName, _getLookupOrder and the two reserved tuples.
- EDGE use core.Object :: tells values from descriptors by :: _isDescriptor compares an Object's __instance_get__ and __instance_set__ with Object's own; parseKwargs, inherited from Object, resolves the option flags.
- EDGE use mcls.space_hooks.ReservedNames :: passes interpreter names through :: The 'reservedNames' attribute; a key in it is left to the namespace.
- SUPPORT utilities.typeCast :: castField, used by the generated __init__ and __setattr__.
- SUPPORT utilities.textFmt :: the __delattr__ message.
- SUPPORT waitaminute.TypeException :: a refused cast.
- SUPPORT waitaminute.dispatch.TypeCastException :: caught from typeCast in castField.
- SUPPORT waitaminute.ezdata.BlackListedType :: an Alias or Dispatcher in the body.
- SUPPORT waitaminute.ezdata.ReservedMethodError :: a body definition of a generated method.
- SUPPORT waitaminute.ezdata.ReservedAttributeError :: a body binding of an attribute EZData sets.
- SUPPORT waitaminute.ezdata.IncompleteFieldException :: a field without type or arguments, or a bare None.
- SUPPORT waitaminute.ezdata.ClassFieldError :: a class bound in the body.
- SUPPORT waitaminute.ezdata.ExtraPositionalException :: more positional arguments than fields.
- SUPPORT waitaminute.ezdata.KwargsOnlyException :: positional arguments to a keyword-only class.
- SUPPORT waitaminute.ezdata.ExtraKeywordException :: a keyword naming no field.
- SUPPORT waitaminute.ezdata.RepeatedFieldException :: a field given by position and by keyword.

Recommendations:
- RECOMMEND [medium] An `@overload` stacked on a reserved generated method is accepted and silently discarded. `LoadSpaceHook.setItemPhase` runs before this hook and claims every `overload`, so `ReservedMethodError` is never raised for it; `LoadSpaceHook.postCompilePhase` then writes a `Dispatcher` at `__init__`, and this hook's `postCompilePhase` overwrites it. Confirmed: a class with `@overload(int) def __init__` builds, and the overload body never runs. Refuse the names of `__installed__` in `postCompilePhase` when `compiledSpace` already holds them, with `ReservedMethodError`.
- RECOMMEND [medium] `_isDescriptor` judges an `Object` by `__instance_get__` and `__instance_set__`, so an `Object` subclass that replaces `__get__` or `__set__` directly is taken for a value: `Alias` and `Dispatcher` are, which the blacklist covers, and `AbstractSpaceHook` is too, which it does not. Confirmed: `hook = LoadSpaceHook()` in an EZData body becomes a field named `hook` of type `LoadSpaceHook`. Compare `__get__`, `__set__` and `__delete__` of the type against `Object`'s as well, which covers all three cases and leaves the blacklist with nothing to do.
- RECOMMEND [medium] The options are read from the class's own keyword arguments alone, so a subclass of a frozen class declared without `frozen=True` gets a casting `__setattr__` and `__hash__ = None` of its own. Confirmed: `class G(F)` with `F` frozen accepts `g.x = 3` and is unhashable, while `G.isFrozen` is False. Either inherit each option from the nearest EZData base when the subclass names none, or refuse the mix as `dataclasses` does for frozen over non-frozen.
- RECOMMEND [low] The option flags are coerced to truth: `parseKwargs` is called with keys only, so `frozen='no'` freezes the class (confirmed). Pass `bool` to `parseKwargs` so a non-bool value raises `TypeException`.
- RECOMMEND [low] `replace` refuses an unknown name with a plain `TypeError` while the generated `__init__` raises `ExtraKeywordException` for the same mistake (confirmed, both). Raise the typed exception in both places, or let `__init__` do the refusing.
- RECOMMEND [low] `replace` rebuilds from `asDict`, which is an optional name a class body or base may hand-write; a hand-written `asDict` that renders values or drops fields silently changes what `replace` constructs. Read the field values directly, as `__iter__` does.
- RECOMMEND [low] `_qualify` sets `__qualname__` but not `__module__`, so every generated method reports `worktoy.ezdata._ez_hook` as its module (confirmed for `asDict`), where the compiled function of a `Dispatcher` takes the owner's module. Set `__module__` to the class's module as well.
- RECOMMEND [note] The frozen `__setattr__` refuses every name, so a `__post_init__` on a frozen class cannot set derived state (`self.double = ...` raises `AttributeError`, confirmed). That is defensible, and it is what `dataclasses` does, but the docstrings name `__post_init__` as the place for derived state without saying so; a sentence pointing at `object.__setattr__` would settle it.
- RECOMMEND [note] A misspelled option keyword (`frozne=True`) is absorbed by `_Chill` and ignored. This is the author's open question on class keywords and no guard is proposed here.

## ezdata.EZSpace
File: src/worktoy/ezdata/_ez_space.py
Kind: namespace

The `BaseSpace` of `EZMeta`. Declares `ezHook = EZHook()` and three
tuples: `__reserved_ez_names__` (the optional names plus
`__post_init__`, which may not be field names but may be methods),
`__reserved_ez_methods__` (the eleven generated methods a body may not
define at all) and `__reserved_ez_attributes__` (the attributes EZData
sets on every class, plus `__key_args__` and `__slots__`). Keeps two
ordered mappings: own fields and inherited fields. `__init__` runs
`BaseSpace.__init__`, then walks the lookup order from the far end and,
for every base whose `__namespace__` is an `EZSpace`, registers that
base's own fields through `registerBaseField`, which clones each one
and names the clone; the farthest class fixes a field's position and
the nearest its definition. `registerEZField` refuses a reserved name
with `ReservedFieldError` and a second own binding with
`DuplicateError`, clones a field object that already carries a name
(bound earlier in the body or in another class), names it and records
it. `getFields` merges inherited then own, own winning on a repeated
name. The module imports `AbstractMetaclass` at runtime for an
annotation only, which the future import keeps as a string.

- EDGE base mcls.BaseSpace :: is based on :: Inherits the three hooks, the shadow space and overload registries, and the compile protocol.
- EDGE use ezdata.EZHook :: declares :: The class attribute ezHook, fourth and last hook of the namespace.
- EDGE use ezdata.EZField :: clones and names :: registerBaseField and registerEZField call clone and write __field_name__ on the copy.
- SUPPORT utilities.maybe :: empty field mappings.
- SUPPORT waitaminute.ezdata.DuplicateError :: a field name bound twice in one body.
- SUPPORT waitaminute.ezdata.ReservedFieldError :: a field at an optional or post_init name.

Recommendations:
- RECOMMEND [low] The `AbstractMetaclass` import is used only in the `__init__` annotation, a string under the future import; move it under `TYPE_CHECKING` with the other annotation-only imports of the module.

## ezdata.EZMeta
File: src/worktoy/ezdata/_ez_meta.py
Kind: metaclass

A `BaseMeta` whose `__prepare__` returns an `EZSpace`. Its body
annotates the three option flags, so `MetaType` installs
`_AnnotationsDescriptor` on it, and declares five `Field` descriptors
on the metaclass itself: `fields` (the merged field tuple read from
the class's `__namespace__`), `sig` (a `TypeSig` of the field types,
built on every read), `isFrozen`, `isOrdered` and `kwOnly` (the flags
as truth). A `Field` on a metaclass works because `Object.__get__`
receives the class as the instance and the getter is looked up on the
metaclass. `__iter__`, `__len__` and `__contains__` (by identity) run
over the fields, so the routed hooks `__class_iter__`, `__class_len__`
and `__class_contains__` are shadowed for EZData bodies, which
`NamespaceHook` refuses with `ShadowedClassHook`. `__init__` writes
`__field_owner__` on every field, own and inherited clones, before
handing over to `BaseMeta.__init__`, so a `__class_init__` hook sees
the owners. `isCongruent(other)` requires `other` to be an EZData
class, one of the two to be a subclass of the other, and the two
`sig` values to compare equal; the generated `__eq__` admits
cross-class equality on that basis.

- EDGE base mcls.BaseMeta :: is based on :: Inherits the routed-hook protocol and the overload compilation; overrides __prepare__ and __init__ and adds the class-level accessors.
- EDGE use ezdata.EZSpace :: prepares and reads :: __prepare__ returns one; the fields getter reads the class's __namespace__ and calls getFields.
- EDGE use ezdata.EZField :: binds owners and iterates :: __init__ writes __field_owner__ on each field; iteration, length and membership of a class run over them.
- EDGE use desc.Field :: exposes class accessors through :: Five Field attributes with GET-decorated getters on the metaclass.
- EDGE use dispatch.TypeSig :: compares field layouts with :: sig wraps the field types in a TypeSig and isCongruent compares two of them.

Recommendations:
- RECOMMEND [low, docstring] `isCongruent` says "a base it derives from"; in the library's own vocabulary a class is based on its bases and derives from its metaclass. Say "a base it is based on".

## ezdata.EZData
File: src/worktoy/ezdata/_ez_data.py
Kind: class (entry point)

`class EZData(Object, metaclass=EZMeta)` with an empty runtime body;
the typing-only stubs under `TYPE_CHECKING` shadow the generated
dunders for checkers. Everything it offers is generated per subclass
by `EZHook`; `EZData` itself is an EZData class with no fields, equal
to every other `EZData()` and of length 0. Being an `Object`, an
instance placed in another class body is a read-only class attribute,
and `EZHook._isDescriptor` reads it as a value, so an EZData instance
in another EZData body becomes a field. A field name is not a class
attribute: `Point.x` raises `MissingVariable` through
`AbstractMetaclass.__getattr__` (confirmed), and the field records are
reached through `fields` or iteration of the class.

- EDGE base core.Object :: is based on :: Inherits the descriptor protocol and argument capture; the generated __init__ never calls Object.__init__.
- EDGE meta ezdata.EZMeta :: derives from :: Built through EZSpace and EZHook, which generate its methods.

Recommendations: none.

## ezdata.fields
File: src/worktoy/ezdata/_fields.py
Kind: function

Returns `cls.fields` for an EZData class or an instance of one, and
raises a plain `TypeError` for anything else, mirroring
`dataclasses.fields`.

- EDGE use ezdata.EZMeta :: recognises classes by and reads :: An isinstance test against EZMeta, then the class-level fields accessor.
- SUPPORT utilities.textFmt :: the refusal text.

Recommendations: none.

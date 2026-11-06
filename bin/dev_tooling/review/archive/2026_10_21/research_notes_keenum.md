# Research notes: the keenum package of worktoy

Read of 2026-10-20, every line of `worktoy.keenum` in the import order
of its `__init__`, with `utilities`, `waitaminute` and the non-leaf
packages opened where `keenum` reaches for them. One entry per item,
appended as soon as the item was read. The format is that of
`research_notes.md` (`core`, `dispatch`, `desc`, `mcls`) and
`research_notes_ezdata.md`; non-leaf items are referred to by the same
`package.Item` names, so the files can be joined.

Entry format. Each entry opens with `## keenum.Item`, then a `File:`
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
  `message` or `typing` added where only text changes. A behaviour a
  recommendation calls confirmed was run on Python 3.14.5.

Load order read: `_kee_member` (Kee), `_kee_num` (KeeBase),
`_kee_flag`, `_kee_space_hook`, `_kee_flags_hook`, `_kee_space`,
`_kee_meta_meta`, `_kee_meta` (KeeMeta, KeeNum), `_kee_flags_space`,
`_kee_flags_meta`, `_kee_flags`, `_kee_box`, `_access_num`.

---

## keenum (package)
File: src/worktoy/keenum/__init__.py
Kind: package

Two enumeration systems on the `mcls` and `desc` machinery. `KeeNum`:
`Kee` declarations in a class body are claimed by `KeeSpaceHook` into
`KeeSpace`, and `KeeMeta` freezes them into `KeeBase` members; the root
class `KeeNum` is not a class statement but the cached `keeNum` of
`KeeMetaMeta`. `KeeFlags`: `KeeFlag` declarations are claimed by
`KeeFlagsHook` into `KeeFlagsSpace`, and `KeeFlagsMeta` materialises one
member per combination. `KeeBox` adapts either as an `AttriBox` field
type, and `AccessNum` is a small enumeration of the three descriptor
operations. The package reads `AttriBox` and `Field` from `desc`,
`BaseSpace`, `BaseMeta` and `AbstractSpaceHook` from `mcls`, `Object`
and `MetaType` from `core`; nothing from `dispatch` directly.

Recommendations: none.

## keenum.Kee
File: src/worktoy/keenum/_kee_member.py
Kind: descriptor (member declaration)

An `AttriBox[T]` subclass declaring one member: `RED = Kee[int](1)`.
The subscript and the call are `AttriBox`'s (`__class_getitem__`
captures the type, `__call__` the arguments through `Object.__init__`),
so the value is built lazily by `AttriBox._resolve` with its copying,
text, number and container rules, and `_applyTags` runs on the built
value. Three `Field` attributes: `value` (built once; `__value_built__`
marks a built `None`, so `Kee[object](None)` works, confirmed), `name`
and `index`, the last two with setters that refuse a non-upper-case
name with `KeeCaseException`, a wrong-typed index with `TypeException`,
and a second write with `VariableNotNone`. `KeeSpace.addNum` writes
the name through the setter and the index directly. A `Kee` in a
`KeeNum` body never reaches `__set_name__`, since `KeeSpaceHook` claims
it; the method accepts a `KeeMeta` owner and refuses any other with
`TypeException`. `clone` builds a fresh `Kee` of the same type and
arguments carrying the name and no index, for a subclass namespace to
register. `__int__` is the index; `__str__` renders `<Kee member:
NAME>` or `- N/A -` when unnamed. The two annotations `valueType` and
`kee` name attributes the class never defines.

- EDGE base desc.AttriBox :: is based on :: Takes the subscript, the argument capture and the lazy, rule-based building of the value.
- EDGE use desc.Field :: exposes name, index and value through :: Three Field attributes with GET and, for name and index, SET decorators.
- EDGE use keenum.KeeMeta :: accepts as owner :: __set_name__ returns to AttriBox for a KeeMeta owner and refuses every other (local import).
- SUPPORT utilities.textFmt :: __str__.
- SUPPORT waitaminute.VariableNotNone :: a second name or index.
- SUPPORT waitaminute.MissingVariable :: name or index read before set.
- SUPPORT waitaminute.TypeException :: wrong-typed slots, a wrong index, a non-KeeMeta owner.
- SUPPORT waitaminute.keenum.KeeCaseException :: a name that is not upper case.

Recommendations:
- RECOMMEND [low] The value is built by `AttriBox._resolve`, whose `_applyTags` writes `__field_name__ = None`, `__field_owner__ = None` and `__field_box__` onto a value that has a `__dict__` (confirmed on a `Kee[Thing](1)`): a `Kee` has no field name or owner in `Object`'s sense, its name lives in `__num_name__`. Either override `_applyTags` to tag with the member name and the enumeration, or to tag nothing, since the value is reached through the member.
- RECOMMEND [low, typing] The annotations `valueType: Field[Type[T]]` and `kee: Field[Type[Self]]` describe attributes `Kee` does not have; `KeeBase` has them. Reading `kee.valueType` raises `AttributeError`. Drop the two annotations.
- RECOMMEND [note] The `KeeMeta` branch of `__set_name__` is reachable only by a `Kee` that lands in a `KeeMeta`-built body without `KeeSpaceHook` claiming it, which no namespace of the library allows; a comment saying the branch guards a namespace subclass without the hook would save the next reader the search.

## keenum.KeeBase
File: src/worktoy/keenum/_kee_num.py
Kind: class (member base)

An `Object` wrapping one `Kee`: `__init__(member)` stores it under
`__field_kee__` between lowering and raising `__frozen_state__`, after
which `__setattr__` raises `KeeWriteOnceError` and `__delattr__` always
does. Five `Field` attributes (`kee`, `name`, `index`, `value`,
`valueType`) read through the `Kee`. The descriptor entry points are
replaced: `__set_name__` is a no-op (so a member placed in another
class body is not written to), `__get__` returns the member for class
and instance access alike, `__set__` raises `ReadOnlyError` and
`__delete__` `ProtectedError` (confirmed: a write through an instance
of a class holding `mode = Level.LOW` reports `'Game.mode'`, the name
found by `DescriptorException._fieldName`). `__copy__` and
`__deepcopy__` return the member, `__reduce__` pickles it as
`getattr(type, name)`. `__hash__` first hashes the value, so a member
with an unhashable value is unhashable, then hashes the bytes of
`Class::NAME`; `__eq__` is identity within one class and
`NotImplemented` across classes. `__int__` and `__index__` give the
index; `__str__` renders `Class.NAME`. `__no_box_tag__` keeps a box
from tagging a member.

- EDGE base core.Object :: is based on :: Takes the value and context protocol; replaces __get__, __set__, __delete__ and __set_name__ so a member in a class body is a read-only constant.
- EDGE use keenum.Kee :: wraps :: The member holds its Kee and answers name, index, value and valueType from it.
- EDGE use desc.Field :: exposes the record through :: Five Field attributes with GET-decorated getters.
- SUPPORT utilities.textFmt :: the unhashable message.
- SUPPORT waitaminute.MissingVariable :: a member without a Kee.
- SUPPORT waitaminute.desc.ReadOnlyError :: a write through an instance.
- SUPPORT waitaminute.desc.ProtectedError :: a deletion through an instance.
- SUPPORT waitaminute.keenum.KeeWriteOnceError :: an attribute set or deleted on a frozen member.

Recommendations: none.

## keenum.KeeFlag
File: src/worktoy/keenum/_kee_flag.py
Kind: class (flag declaration)

A plain class, not an `Object`, declaring one bit in a `KeeFlags` body.
`__init__` stores positional and keyword arguments that nothing in the
package consumes except `clone` and `__repr__`. Seven `Field`
attributes: `fieldName`, `fieldOwner`, `index`, `name` (each raising
`MissingVariable` when unset), `args`, `kwargs`, and `valueType`,
which has no getter. `__set_name__` always raises `TypeException`,
since a flag in a `KeeFlags` body is claimed by `KeeFlagsHook` and the
owner is written by `clone(owner, index)`, which `KeeFlagsSpace` uses to
give each class its own flag objects with contiguous indices. Equality
is by owner identity and index, hash by `(owner, fieldName, index)`;
`__int__` and `__index__` give the index; `__iter__` raises
`TypeError`. Typing-only overloads promise `|`, `&`, `^` and `~`.

- EDGE use desc.Field :: exposes the record through :: Seven Field attributes, six with GET-decorated getters.
- EDGE use keenum.KeeFlagsMeta :: names in refusals :: The owner getter and __set_name__ import it locally for the expected type.
- SUPPORT utilities.textFmt :: __str__ and __repr__.
- SUPPORT utilities.maybe :: empty argument fallbacks and the clone's index.
- SUPPORT waitaminute.MissingVariable :: an unset name, index, field name or owner.
- SUPPORT waitaminute.TypeException :: a wrong-typed slot, or any owner in __set_name__.

Recommendations:
- RECOMMEND [low] The constructor arguments are stored and never read by the metaclass or the members; the `KeeBox` docstring nevertheless writes `SHIFT = KeeFlag(0)` as if the argument mattered. Say what they are for, or drop them and the example's arguments.
- RECOMMEND [low] `valueType` is a `Field` with no getter, so reading it raises `AccessError` (confirmed). Give it a getter returning `fieldOwner.valueType`, or remove it.
- RECOMMEND [low, typing] The `TYPE_CHECKING` overloads declare `|`, `&`, `^` and `~` on a flag, but at runtime `flag | flag` raises `TypeError` (confirmed); the operators belong to the members. Remove the stubs or implement the operators through the owner's `memberDict`.

## keenum.KeeSpaceHook
File: src/worktoy/keenum/_kee_space_hook.py
Kind: hook

`setItemPhase`: a `__class_resolve__` bound to a plain function or
staticmethod raises `UnboundClassHook`; a `Kee` at a name the body
already bound raises `KeeMemberNameError`, else it is handed to
`KeeSpace.addNum` and claimed; a plain value at a name a member holds,
declared or inherited, raises `KeeMemberNameError`; anything else is
left to the namespace.

- EDGE base mcls.space_hooks.AbstractSpaceHook :: is based on :: Implements setItemPhase alone.
- EDGE use keenum.Kee :: claims :: Every Kee bound in the body is routed to addNum and never stored in the namespace.
- EDGE use keenum.KeeSpace :: registers into :: addNum and hasNum on the namespace under construction.
- SUPPORT waitaminute.keenum.KeeMemberNameError :: a name bound both to a member and to a plain value.
- SUPPORT waitaminute.meta.UnboundClassHook :: an unbound __class_resolve__ in the body.

Recommendations: none.

## keenum.KeeFlagsHook
File: src/worktoy/keenum/_kee_flags_hook.py
Kind: hook

`setItemPhase` routes every `KeeFlag` to `KeeFlagsSpace.addKeeFlag` and
claims it; everything else passes.

- EDGE base mcls.space_hooks.AbstractSpaceHook :: is based on :: Implements setItemPhase alone.
- EDGE use keenum.KeeFlag :: claims :: Every KeeFlag bound in the body is routed to addKeeFlag.
- EDGE use keenum.KeeFlagsSpace :: registers into :: addKeeFlag on the namespace under construction.

Recommendations: none.

## keenum.KeeSpace
File: src/worktoy/keenum/_kee_space.py
Kind: namespace

The `BaseSpace` of `KeeMeta`, declaring `keeSpaceHook`. `__init__`
creates the ordered member dict before `BaseSpace.__init__`, then for
each base reads the base namespace's `__member_type__` and
`__enumeration_members__`, refusing a name two bases share with
`KeeDuplicate` and registering a `clone` of each inherited `Kee`.
`addNum(name, member)` refuses a repeated name with `KeeDuplicate`,
writes the name through the `Kee` setter when the member has none and
refuses a different existing name with `KeeNameConflict`, writes the
index directly as the count so far, runs `typeGuard` (the first
member's `__field_type__` pins the type by identity; a later member of
another type raises `KeeTypeException`), and stores. `hasNum` answers
for declared and inherited members. `postCompile` adds
`__member_type__` to the compiled namespace.

- EDGE base mcls.BaseSpace :: is based on :: Inherits the hooks, shadow space and compile protocol; adds the member registry.
- EDGE use keenum.KeeSpaceHook :: declares :: The class attribute keeSpaceHook, fourth hook of the namespace.
- EDGE use keenum.Kee :: names, indexes and clones :: addNum writes the name and index; __init__ registers clones of inherited members; typeGuard reads the field type.
- SUPPORT waitaminute.keenum.KeeDuplicate :: a name declared twice, in one body or across bases.
- SUPPORT waitaminute.keenum.KeeTypeException :: a member of a second value type.
- SUPPORT waitaminute.keenum.KeeNameConflict :: a Kee already named differently.

Recommendations:
- RECOMMEND [medium] `addNum` writes `member.__num_index__` directly, past the write-once setter, so a `Kee` object bound in two enumerations has its index overwritten by the second. Confirmed: with `K = Kee[int](7)`, `class A(KeeNum): X = K` and `class B(KeeNum): Y = Kee[int](1); X = K`, `A.X.index` is 1, and `A.X.kee is B.X.kee`. Clone a `Kee` that already carries a name, as `__init__` clones inherited ones (and as `EZSpace.registerEZField` clones a named `EZField`), or refuse the second registration.

## keenum.KeeMetaMeta
File: src/worktoy/keenum/_kee_meta_meta.py
Kind: metaclass (meta-metaclass)

A `MetaType` subclass, itself built by `type` (its MRO is
`KeeMetaMeta, MetaType, type, object`, no `_Chill`; confirmed). It
hosts one `Field`, `keeNum`, whose getter builds the root enumeration
of the metaclass it is read on: the namespace from that metaclass's
`__prepare__` with `_root=True`, the docstring of `KeeBase`, the class
from `__new__`, cached under `__kee_num__` before `__init__` runs (so
`_createBase` recognises the root by identity), named `KeeNum` for
`KeeMeta` itself and `<Meta>Num` for a subclass. `KeeMeta` resets the
cache in `__init_subclass__`, so each subclass of `KeeMeta` builds its
own root through its own machinery. The docstring explains why: an
enumeration of a customised metaclass must be based on that
metaclass's root, not on `KeeNum`.

- EDGE base core.MetaType :: is based on :: Takes MetaType.__new__ for the metaclasses it builds, which is how KeeMeta gets _Chill and the namespace record.
- EDGE use desc.Field :: exposes the root through :: keeNum is a Field on the meta-metaclass, read on a metaclass.
- EDGE use keenum.KeeBase :: bases the root on :: The root class is built with (KeeBase,) as its bases and KeeBase's docstring.
- EDGE use keenum.KeeMeta :: builds the root through :: The getter calls the metaclass's __prepare__, __new__ and __init__ by hand, with the _root keyword.

Recommendations:
- RECOMMEND [low] The root carries `__module__` `worktoy.core._meta_type` (confirmed for `KeeNum`), since the hand-built namespace holds no `__module__` and `type.__new__` reads the module of the frame that calls it, which is `MetaType.__new__`. Write `numSpace['__module__'] = mcls.__module__` before building.
- RECOMMEND [note] `KeeMetaMeta` is the one metaclass of the library not built by `MetaType`, so its own class statement, unlike every other, would refuse a class keyword. Nothing subclasses it with one; a sentence in the docstring would record the exception.

## keenum.KeeMeta
File: src/worktoy/keenum/_kee_meta.py (lines 30-661)
Kind: metaclass

`class KeeMeta(BaseMeta, metaclass=KeeMetaMeta)`. Seven `Field`
accessors (`base`, `space`, `mroNum`, `members`, `valueType`,
`namedMembers`, `valuedMembers`) over private slots that `__init__`
fills through the creators, each getter carrying the `_recursion`
guard. `__init__` runs `_createSpace` (the class's `__namespace__`
must be a `KeeSpace`), `_createBase` (the root is its own base, so is
a class based directly on the root; otherwise exactly one base of the
metaclass, else `ValueError`), `_createMembers` (with the write guard
down: for each registered `Kee`, the base's member of that name if it
has one, the very same object, else `cls(kee)` through
`KeeBase.__init__`; bound with `setattr`), `_createNamedMembers`
(lower-cased names), `_createValuedMembers` (hashable values to first
member, collapsing to an `__unhashable__` marker on the first
unhashable value), `_validateClassResolve` (any callable
`__class_resolve__` found along the class is accepted), then
`BaseMeta.__init__` so `__class_init__` sees the members.

Resolution. `__call__` refuses keywords and any count but one with a
plain `TypeError` and resolves; `__getitem__` resolves with the index
step allowed. `_resolveMember`: identity, then name for a `str`
(case-insensitive through `namedMembers`), then the hook (returning
`NotImplemented` to defer), then a non-bool `int` as a position when
allowed, then value when the identifier is an instance of `valueType`
(`bool` refused for `int` enumerations, unhashable identifiers and
values scanned by equality), else `KeeResolveError`. `fromValue` is
the value step alone. `__getattr__` resolves a missed attribute
through the same case-insensitive name lookup on the class and its
base, so `Base.red` and `Base.Red` give `Base.RED` (confirmed).
`__setattr__` and `__delattr__` refuse rebinding or deleting a member
name with `KeeWriteOnceError` once the guard is up. `__iter__`,
`__len__`, `__bool__` and `__contains__` run over the members, the
last by `isinstance`; `__instancecheck__` is identity with the members
or a Python subclass relation, so a base member is an instance of every
derived enumeration (confirmed `isinstance(Base.RED, Sub)`);
`__subclasscheck__` scans the MRO. `__str__` renders `<KeeNum 'Name':
N members>`. `__init_subclass__` resets `__kee_num__`.

- EDGE base mcls.BaseMeta :: is based on :: Inherits the routed hooks and overload compilation; overrides __prepare__, __new__, __init__, __call__ and the container and attribute operations, which NamespaceHook therefore refuses as class hooks.
- EDGE meta keenum.KeeMetaMeta :: derives from :: Gains the keeNum root builder; its own class statement goes through MetaType.__new__.
- EDGE use keenum.KeeSpace :: prepares and reads :: __prepare__ returns one; the creators read its member dict and member type.
- EDGE use keenum.KeeBase :: instantiates members as :: cls(kee) with the guard down builds a KeeBase; the write guards test for KeeBase values.
- EDGE use desc.Field :: exposes the record through :: Seven Field attributes on the metaclass, read on the enumeration classes.
- SUPPORT utilities.textFmt :: refusal texts.
- SUPPORT utilities.joinWords :: the keyword list in the call refusal.
- SUPPORT utilities.maybe :: the base fallback in __getattr__.
- SUPPORT waitaminute.TypeException :: a non-KeeSpace namespace, a non-callable hook, a value of the wrong type.
- SUPPORT waitaminute.keenum.KeeResolveError :: no step resolved the identifier.
- SUPPORT waitaminute.keenum.KeeWriteOnceError :: rebinding or deleting a member name.

Recommendations:
- RECOMMEND [low] Attribute access on an enumeration is case-insensitive through `__getattr__` (confirmed), which no docstring states and which `KeeFlags` classes do not share; `Flags.read` raises there. Either state it on `KeeMeta` and `KeeBase`, or restrict attribute access to the exact name and leave case-insensitivity to call and subscript, as the class docstring describes.
- RECOMMEND [low] `_validateClassResolve` accepts any callable, so a `__class_resolve__` written as a plain function on a plain mixin base passes, where the same definition in the enumeration body is refused by `KeeSpaceHook` with `UnboundClassHook`; called as `cls.__class_resolve__(identifier)` it then receives the identifier in the `cls` slot. Hold the inherited hook to the body rule, as `NamespaceHook._validateInheritedHook` does for the routed hooks.
- RECOMMEND [note] A base member is an instance of every derived enumeration, and `Sub.RED is Base.RED` (confirmed). The `__instancecheck__` docstring says so; `KeeBase` does not, and `KeeBox[Sub]` accepts base members through it, so a reader of `KeeBase` should find the sentence too.

## keenum.KeeNum
File: src/worktoy/keenum/_kee_meta.py (lines 664-687)
Kind: class (root enumeration)

Not a class statement: `KeeNum = KeeMeta.keeNum`, the root the
meta-metaclass builds, based on `KeeBase` and derived from `KeeMeta`.
Under `TYPE_CHECKING` a stub class with the metaclass operations
stands in for checkers (the "samizdat" docstring is deliberate). It has
no members (`bool(KeeNum)` is False) and is its own base.

- EDGE base keenum.KeeBase :: is based on :: The root is built with KeeBase as its one base.
- EDGE meta keenum.KeeMeta :: derives from :: Built through KeeMeta's __prepare__, __new__ and __init__ with the _root keyword.
- EDGE use keenum.KeeMetaMeta :: is the cached keeNum of :: The module binds the name to KeeMeta.keeNum at import.

Recommendations: none.

## keenum.KeeFlagsSpace
File: src/worktoy/keenum/_kee_flags_space.py
Kind: namespace

The `BaseSpace` of `KeeFlagsMeta`, declaring `keeFlagsHook`. `__init__`
runs `BaseSpace.__init__` and, unless `_root`, records the `flags` of
every base built by `KeeFlagsMeta` as base flags. `addKeeFlag` refuses
a name holding `_` or equal to `NULL` with `KeeFlagNameError`, a
non-upper-case name with `KeeCaseException`, and a name already
declared or inherited with `KeeFlagDuplicate`, then writes the member
name and field name onto the flag; the index is left for `getKeeFlags`.
`getKeeFlags` merges inherited then own. `postCompile`, for a non-root
class, writes `__kee_flags__` (that merged dict) and a `getKeeFlags`
classmethod built by `_getKeeFlagsFactory`, which clones each flag onto
the class with a fresh contiguous index.

- EDGE base mcls.BaseSpace :: is based on :: Inherits the hooks and the compile protocol; adds the flag registries and postCompile.
- EDGE use keenum.KeeFlagsHook :: declares :: The class attribute keeFlagsHook.
- EDGE use keenum.KeeFlag :: names and clones :: addKeeFlag writes the names; the installed getKeeFlags clones each flag with its index.
- EDGE use keenum.KeeFlagsMeta :: recognises bases by :: __init__ records flags only from bases built by KeeFlagsMeta (local import).
- SUPPORT utilities.maybe :: empty registries.
- SUPPORT waitaminute.keenum.KeeFlagDuplicate :: a repeated flag name, own or inherited.
- SUPPORT waitaminute.keenum.KeeFlagNameError :: a flag name with an underscore or NULL.
- SUPPORT waitaminute.keenum.KeeCaseException :: a flag name that is not upper case.

Recommendations:
- RECOMMEND [low] `postCompile` writes `getKeeFlags` over whatever the class body bound at that name without a word (confirmed: a body classmethod `getKeeFlags` returning a marker is gone on the class). Refuse the name in the body as `KeeMemberNameError`, or install the classmethod only when the body bound nothing there.

## keenum.KeeFlagsMeta
File: src/worktoy/keenum/_kee_flags_meta.py
Kind: metaclass

A `BaseMeta` whose `__prepare__` returns a `KeeFlagsSpace`. `__new__`
builds the class through `BaseMeta.__new__`; for the root (`_root`) it
records the class as `__kee_class__` on the metaclass; for any other it
lowers the write guard, instantiates `2 ** N` members as `cls(i)`,
refuses a member name the body bound with `KeeMemberNameError`, stamps
owner and name on each, binds it, fills `memberList` and `memberDict`
(keyed by the frozenset of high names) and freezes the member. Four
`Field` accessors: `flags` (clones made once through the installed
`getKeeFlags` and kept under `__flag_clones__`), `valueType` (the type
of `NULL.value`), `memberList`, `memberDict`. `__subclasscheck__` walks
`__kee_bases__`, with the root never a subclass of a flags class.
`__call__` refuses keywords and resolves; `__getitem__` resolves;
`__contains__` is resolve-based, so `'read' in Flags` is True; `__len__`
and `__iter__` run over `memberList`; `__hash__` is by name and
module. `_resolveMember`: no identifier gives `NULL`; several, or one
container, give the union through `_resolveNames`; a member passes
through `isinstance`; a non-bool `int` is an index (linear scan); a
`str` goes to `_resolveName` (canonical name ignoring case, or any
order of `_`-joined flag names), which raises on a miss; anything else
to `_resolveValue` (first member whose value equals it, comparing only
with values of a type the identifier is an instance of, `bool` only
with `bool`). `__setattr__` and `__delattr__` guard member names with
`KeeWriteOnceError`.

- EDGE base mcls.BaseMeta :: is based on :: Inherits the routed hooks; overrides __prepare__, __new__, __call__, the container operations, __hash__, __subclasscheck__ and the attribute guards.
- EDGE use keenum.KeeFlagsSpace :: prepares :: __prepare__ returns one; __new__ reads the compiled flags through getKeeFlags.
- EDGE use keenum.KeeFlag :: clones and reads :: flags holds the per-class clones; members report their highs from them.
- EDGE use keenum.KeeFlags :: records the root and instantiates members of :: The root class statement is stored as __kee_class__; every member is an instance of the class under construction, built by cls(i).
- EDGE use desc.Field :: exposes the record through :: Four Field attributes on the metaclass.
- SUPPORT utilities.textFmt :: the keyword refusal.
- SUPPORT utilities.joinWords :: the keyword list.
- SUPPORT waitaminute.keenum.KeeResolveError :: a miss by index, name or value.
- SUPPORT waitaminute.keenum.KeeWriteOnceError :: rebinding or deleting a member name.
- SUPPORT waitaminute.keenum.KeeMemberNameError :: a body attribute at a member name.

Recommendations:
- RECOMMEND [medium] The identity step of `_resolveMember` uses `isinstance`, and a member of a derived flags class is an instance of the base class, so `FBase(FSub.READ) is FSub.READ` and `FSub.READ in FBase` hold, while `FBase.READ == FSub.READ` is False and `FBase.READ | FSub.WRITE` raises `TypeError` (all confirmed). The three views disagree. Resolve a derived member into the base's own member of the same names (`cls.memberDict[identifier.names]` when every name is a flag of `cls`), or refuse it, and let `__eq__` and `in` follow the same rule.
- RECOMMEND [low] A `str` identifier goes to `_resolveName`, which raises on a miss rather than deferring, so a class whose `_getValue` returns strings cannot be resolved by value: `S('rw')` raises although `S.R_W.value == 'rw'` (confirmed), and the `KeeFlags._getValue` docstring points to a `fromValue` the metaclass does not have (confirmed). Fall through to `_resolveValue` on a name miss, and add `fromValue` or correct the docstring.
- RECOMMEND [low] `_resolveIndex` scans `memberList` for a matching index, although the members are built in index order and `memberList[index]` is that member; a bounds check and one subscript would do.

## keenum.KeeFlags
File: src/worktoy/keenum/_kee_flags.py
Kind: class (root flags enumeration)

`class KeeFlags(metaclass=KeeFlagsMeta, _root=True)`. A member holds
`__member_index__`, its bitmask, set by `__init__(index)`; `__frozen_state__`
is raised by the metaclass after stamping. Seven `Field` attributes:
`index`; `flags` (mirroring the metaclass descriptor for instances);
`lows` and `highs`, generators over the class's flags by bit; `value`,
by default the index, the hook a subclass overrides for other values;
`name`, the high names joined by `_` or `NULL`; `names`, their
frozenset. `__setattr__` and `__delattr__` raise `KeeWriteOnceError`
once frozen; `__copy__`, `__deepcopy__` and `__reduce__` keep the
singleton; `__bool__` is the bitmask; `__iter__` yields the high flags;
`__eq__` compares owner identity and index and returns `NotImplemented`
for a non-flags other; `__hash__` hashes the class hash with the high
flags. `|`, `&`, `^` and `~` look the result up in `memberDict` and
accept only the exact same class. `__no_box_tag__` keeps a box from
tagging a member.

- EDGE meta keenum.KeeFlagsMeta :: derives from :: The root is marked by the _root keyword; every subclass has its members materialised by the metaclass.
- EDGE use desc.Field :: exposes the record through :: Seven Field attributes with GET-decorated getters.
- EDGE use keenum.KeeFlag :: reads bits through :: highs and lows test the member index against each flag's bit.
- SUPPORT utilities.textFmt :: __str__.
- SUPPORT waitaminute.MissingVariable :: an index read before set.
- SUPPORT waitaminute.TypeException :: a wrong-typed index.
- SUPPORT waitaminute.keenum.KeeWriteOnceError :: an attribute set or deleted on a frozen member.

Recommendations:
- RECOMMEND [note] Membership differs between the two families: `'read' in Flags` is True because `KeeFlagsMeta.__contains__` resolves, while `'red' in Colors` is False because `KeeMeta.__contains__` is identity. Both are documented on their metaclass; a sentence on the two roots saying which rule each follows would stop a reader from assuming one from the other.

## keenum.KeeBox
File: src/worktoy/keenum/_kee_box.py
Kind: descriptor (enumeration-valued box)

An `AttriBox` whose `__class_getitem__` accepts only a class derived
from `KeeMeta` or `KeeFlagsMeta` (`TypeException` otherwise). It
replaces `_resolve`, `__instance_get__` and `__instance_set__`: a read
builds from the captured arguments through `_resolve()` and stores with
`_store`; an assignment stores a member of the field enumeration as it
is (a member of a derived enumeration passes `isinstance` too) and
resolves anything else through `_resolve(value)`. `_resolveNum`: with
one argument, a member passes, a `str` matches a name exactly then
ignoring case, an `int` in range is an index, an instance of
`valueType` matches a value; otherwise the arguments build a
`valueType` and the first member of equal value is taken
(`KeeBoxTypeError` when the build fails, `KeeBoxValueError` when no
value matches). `_resolveFlags`: the captured or assigned arguments,
one container splatted, each resolved by subscripting the flags class
and the union taken from `memberDict`. `_resolve` accepts keywords it
never reads. Deletion is `AttriBox`'s, storing `DELETED`.

- EDGE base desc.AttriBox :: is based on :: Takes the subscript, argument capture, storage and deletion; replaces the building and the instance get and set.
- EDGE use keenum.KeeMeta :: resolves members of :: The subscript test, and _resolveNum walking the enumeration's members, names, indices and valueType.
- EDGE use keenum.KeeFlagsMeta :: resolves members of :: The subscript test, and _resolveFlags subscripting the flags class and reading memberDict.
- SUPPORT waitaminute.TypeException :: a subscript that is not an enumeration class.
- SUPPORT waitaminute.keenum.KeeBoxException :: a field type that is neither family (unreachable through the subscript).
- SUPPORT waitaminute.keenum.KeeBoxTypeError :: the value type refusing the arguments.
- SUPPORT waitaminute.keenum.KeeBoxValueError :: a well-typed value matching no member.

Recommendations:
- RECOMMEND [low] An `int` is read as an index before a value, so `KeeBox[Level](2)` on members valued 2, 5, 9 gives `HIGH` (index 2) while `Level(2)` gives `LOW` (confirmed). The box docstring lists that order, but it reverses what calling the enumeration does. Resolve a lone argument through `fieldNum(arg)` so the box accepts exactly what the class does, as `_resolveFlags` already does through subscripting, or state the divergence beside the `Level(2)` case.
- RECOMMEND [low] A `bool` assigned to a box over an `int` enumeration passes `isinstance(value, int)` and `0 <= value < len`, reaches `fieldNum[True]`, and the enumeration refuses it with `KeeResolveError` (confirmed). Exclude `bool` from the index step as `KeeMeta` does, so it falls to the value and build steps with a message naming the box.
- RECOMMEND [low] `_resolve(*args, **kwargs)` takes keywords and drops them, while `_resolveNum` reads the captured keywords itself. Drop the parameter.

## keenum.AccessNum
File: src/worktoy/keenum/_access_num.py
Kind: class (enumeration)

A `KeeNum` of three `str` members, `GET`, `SET` and `DELETE`, valued
`__get__`, `__set__` and `__delete__`, for naming a descriptor
operation.

- EDGE base keenum.KeeNum :: is based on :: An ordinary enumeration of the root.
- EDGE use keenum.Kee :: declares members with :: Three Kee[str] declarations.

Recommendations: none.

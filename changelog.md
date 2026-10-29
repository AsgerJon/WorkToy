# Changelog

This changelog covers stable releases. Development ('-dev') and release
candidate ('-rc') builds are not logged on their own; their changes are
rolled into the release they lead up to.

## [1.1.0] - unreleased

### FastBox takes one value, checked at the class-body line

`FastBox` handed the arguments in its parentheses to the constructor of
its field type at the first read, so `FastBox[int]('abc')` passed the
class body and failed only when an instance first read the field. The
parentheses now take one value, checked by `FastBox.__call__` at the
class-body line: a value of the field type is kept as it is, and any
other goes through `typeCast`, which converts only among the numbers and
among `str`, `bytes` and `bytearray`, without loss, or through a
`__cast_as__` of the field type, and otherwise raises `TypeCastException`
there. `FastBox[float](1)` holds `1.0`; `FastBox[int]('abc')` and
`FastBox[int](2.5)` raise. Every instance shares the value, so one that
cannot be hashed, such as a `list`, raises `TypeError`, as do several
arguments or a keyword. Empty parentheses, or none, give each instance
`fieldType()` at its first read, and the constructor's own exceptions now
pass through as they are instead of turning into `TypeException`. A write
is checked as before, by `isinstance` alone.

### A class attribute no longer replaces a metaclass helper

`AbstractMetaclass` called its helpers `_notifySubclassHook` and
`_skipHash` through the class it had built, so a class body defining
either name answered in their place: a method named `_notifySubclassHook`
kept the `__subclasshook__` of every base from being asked, for that class
and its subclasses, and a `_skipHash` attribute broke `hash` of the class.
Both are now called through the metaclass.

### A word is in a SymbolicName ignoring case

A `SymbolicName` ignores case for equality and hashing, so
`SymbolicName('Font', 'Size') == SymbolicName('font', 'size')`, but `in`
compared the words as written: `'Font' in SymbolicName('font', 'size')`
was False. `in` now ignores case as well, and anything but a `str` is in
no name.

### ARGS without a type is a tail of any type, with or without the star

`@overload(int, *ARGS)` now declares an `int` followed by any number of
arguments of any type, as `@overload(int, *ARGS[object])` does; it used
to fail with `Value after * must be an iterable`. A bare `ARGS`, written
without the star, means the same. It used to be accepted as a signature
whose last entry is the class `ARGS`, which no call could match, so
`@overload(int, ARGS)` failed only at the first call, with a
`DispatchException` listing `<TypeSig: [int, ARGS]>`. `overload`,
`overload.flex`, `Dispatcher.overload` and `Dispatcher.flex` read every
bare `ARGS` as `*ARGS` through the new `TypeSig.starARGS`, so `flex`
refuses it with `TypeException`, as it refuses `*ARGS`.

### The field object of an AttriBox is an instance of its field type

At the first read an `AttriBox` calls the constructor of its field type on
the arguments in its parentheses and keeps what it returns as the field
object. A constructor returning something else, such as a `__new__` that
returns another object or forgets to return at all, was kept without a
check: a foreign object with a `__dict__` sat in the field, and one
without failed in the tagging with an `AttributeError`, which `hasattr`
read as the field being absent. Such a field object now raises
`TypeException` naming the field, the object and the field type, at the
read, as `FastBox` and an assignment already did. A constructor returning
an instance of a subclass passes.

### An overload is bound once per class body

Binding an `overload` a second time in the class body that declared it,
as in `__radd__ = __add__`, gave the second name a copy of the overloads
of the first, but the copy counted the overloads the class inherits as
its own. The dispatcher tries a subclass's overloads before inherited
ones by exact type and through `isinstance`, and inherited ones first
through a cast, so the two names could call different functions: with
`@overload(complex)` declared beside an inherited `@overload(float)`,
`z + 1` reached the inherited function and `1 + z` the subclass's. A
second binding of one `overload` object in one class body, under another
name or the same one, now raises `ReboundOverload`, a `SyntaxError` new
in `worktoy.waitaminute.meta`, at its line. The second name takes a
method of its own, which may call the first, as in `def __radd__(self,
other): return self.__add__(other)`. Another class body may still bind
the same `overload` object.

### A sentinel as the field type of a box is refused

`AttriBox[THIS]()`, a natural attempt at a field holding an instance of
the enclosing class, was accepted as the class was created and failed at
the first read, when the box called `THIS()`, with `Expected object at
name 'next' to be an instance of 'THIS', but received object: '()' of
type 'tuple'!`. A sentinel stands for a meaning, such as the enclosing
class, and is no type of value a field could hold. `AttriBox`, the boxes
based on it, and `FastBox` now refuse a sentinel, any class built by
`SentinelMeta`, `ARGS` included, at the subscript itself: `AttriBox[THIS]`
raises a `TypeError` naming the subscript, before any class body binds
it.

### An overloaded method takes a keyword named 'instance'

The function an overloaded method compiles to named its first parameter
`instance`, and the wrapper of an `overload.flex` registration named its
first one `func`, so a call passing a keyword of either name, such as
`Serializer(data, instance=obj)`, failed with `got multiple values for
argument`, naming the method as if its own signature were at fault, while
a plain method with the same signature accepted it. Both now take those
arguments from their positional arguments without naming them, as
`functools.partial` and `functools.singledispatchmethod` do, so every
keyword passes through to the function the call selects. Called through
the class with no arguments, the compiled function refuses as before,
now naming `self` as the function of a plain method does. The `invoke`
methods of `CallMeMaybe`, `Permuter` and `PermuterMethod` take the
function, and the instance, by position only.

### A descriptor is placed on one class

One box object bound in the bodies of two classes, as `shared =
AttriBox[Point]()` followed by `p = shared` in `A` and in `B`, served
both: the second class took the box over, and the values the box built
for the instances of `A` named `B` as their owner in their tags. A
descriptor based on `BaseDescriptor`, such as an `AttriBox`, a `FixBox`
or a `Field`, placed on a second class, at the same name or another, is
now refused with `SharedDescriptor`, a `SyntaxError` new in
`worktoy.waitaminute.desc`, as that class is created (wrapped in a
`RuntimeError` on Python 3.7 through 3.11, as anything raised from
`__set_name__`). A field meant for several classes is declared in a common
base, or each class takes a descriptor of its own. Bound to
a second name in the same class body, every such descriptor places a
clone of itself, made by its `clone`, at that name, as a box already did;
`BaseDescriptor.__set_name__` now decides both cases. A `Field` bound to
two names used to be one object recording the second name, so its
messages named the wrong attribute.

### A renamed class keeps its place in a dict

The default hash of a class built by a metaclass based on
`AbstractMetaclass`, made from the names of the class, its bases and its
metaclass, was computed afresh at every hash. A class renamed after it
was hashed, as a factory names the class it built, then hashed by its new
name, and a dict or set holding it, such as a registry filled in
`__init_subclass__`, no longer found it. The default is now computed at
the first hash and kept in the class's own `__dict__` under
`__class_hash_value__`, so a class keeps its hash for life, as a plain
class does. The values are those of before, a class defining
`__class_hash__` is asked at every hash as before, and a subclass
computes its own. Hashing a class, which an overloaded call does for
every argument class on its exact-type pass, now costs less than a
quarter of what it did.

### A subclass overload wins every call it accepts

An overload a subclass declares beside inherited ones now takes every
call it accepts, by exact type or through `isinstance`, before any
inherited overload is tried. An inherited signature matching a call
exactly used to keep it, so with `@overload(int)` inherited and
`@overload(object)` declared in the subclass, `f(1)` reached the parent
while `f(True)` reached the subclass. Both now reach the subclass, and
the inherited overload keeps the calls the subclass does not accept. The
cast passes still try the inherited signatures first, so a signature a
subclass adds never takes a call its parent handles through a cast.

### The latest subclass variadic takes a call its parent declares

A variadic signature of a subclass that accepts a call a parent declares
explicitly, such as `ARGS[int]` beside the parent's `(int, int)`, takes
that call, so the subclass implementation wins. With two such variadics
in the subclass, `ARGS[int]` and `(int, ARGS[int])`, the parent's call
went to the one declared first, while every other call the two share
went to the most recent, as documented. The most recent declaration of
the nearest class now takes the parent's call as well: with
`(int, ARGS[int])` declared last, `f(69, 420)` reaches it, by exact type
and through `isinstance` alike.

### A private callback is found

Notification callbacks and `Field` accessors are recorded by name and
looked up on the class of the instance at each access. A callback written
with two leading underscores, such as `def __audit` decorated with
`@balance.onSet` in `Account`, was recorded as `__audit` while the class
body stores it as `_Account__audit`: the class was created, and the first
access failed with `AttributeError`, or, on an owner defining
`__getattr__`, silently read that method's answer in place of the field.
The decorators now record a private name as the class body stores it,
taking the class from the callback's `__qualname__`; like any private
name it is not overridden by a subclass. A private function whose
qualified name names no class, such as one made inside another function,
is refused with `NamelessCallback`.

### Two names bound to one box are two fields

`width = height = AttriBox[int](0)` binds one box to two names, and the
box took the last name for both, so the two attributes read and wrote one
storage slot: assigning `width` changed `height`. The box now keeps the
first name, and the second name receives a clone of it as the class is
created, carrying the field type, the captured default and the callbacks
registered on the box by then. `FixBox` and the other boxes based on
`AttriBox` follow, and so does `FastBox`, which gains a `clone` method
for it.

### A base listed after an Object class is initialized

`Object.__init__` called `object.__init__` directly, so the chain of
`__init__` calls stopped at `Object`: a base listed after a worktoy
class, as in `class Worker(BaseObject, threading.Thread)`, never had its
`__init__` run, and the object failed later, at its first use
(`RuntimeError: thread.__init__() not called`). `Object.__init__` now
records its arguments and then calls the next `__init__` along the
resolution order without them, so `threading.Thread`, `logging.Handler`
and cooperative mixins listed after a worktoy class are initialized as
in a plain class. A base whose `__init__` requires arguments, listed
after a worktoy class, now refuses at construction with its own
`TypeError` instead of being skipped; listed before it, it receives its
arguments as before.

### A box refuses an owner without an instance dict as the class is created

`AttriBox`, every box based on it (`FixBox`, `KeeBox`, `Kee`), and
`FastBox` keep the value of a field in the instance dict. Placed on a
class declaring `__slots__` without `__dict__`, `AttriBox` refused only
at the first access, and `FastBox` failed there with the bare
`AttributeError` of the missing `__dict__`, so `hasattr` answered `False`
as if the field were absent. Both now raise `MissingInstanceDict` from
`__set_name__`, as the class is created (wrapped in `RuntimeError` on
Python 3.7 through 3.11, as every `__set_name__` exception is), and a box
installed on such a class with `setattr` afterwards is refused with the
same exception at every access.

### A metaclass mixed in beside BaseMeta takes part

`AbstractMetaclass` called `MetaType` by name in `__new__`, in
`__init__` and in the defaults that apply when a class declares no hook,
those of `__call__`, `__instancecheck__`, `__subclasscheck__`, `__str__`,
`__repr__`, `__setattr__` and `__delattr__`. A metaclass of a project's
own, based on `MetaType` and mixed in beside `BaseMeta` as in
`class Meta(BaseMeta, OtherMeta)`, sits between `AbstractMetaclass` and
`MetaType` in the resolution order, and none of its versions of those
methods ever ran. They now hand over with `super()`, so they run in the
order of the metaclass resolution order, while a class hook still takes
its operation first. In the metaclasses of the library the next class
after `AbstractMetaclass` is `MetaType`, so nothing changes for them.

### Plain lookups read past the attribute hooks of a class

Where the library needs the ordinary attribute lookup on a class or on an
object it does not own, it now reads with `type.__getattribute__` or
`object.__getattribute__` instead of `getattr`, so no `__getattr__`,
`__class_getattr__` or reimplemented `__getattribute__` can answer in
its place. This covers:

- the `__no_box_tag__` opt-out `AttriBox` reads before tagging an object
  it built: a class whose hooks answered every name used to opt out of
  the tags without asking to, and its objects lost the link to the box
  that built them;
- the notification and `setName` callbacks of a descriptor, and the
  accessors of a `Field`, found by name on the class of the instance;
- the `__skip_hash__` flag the default class hash reads off each base,
  and the `__namespace__` that `getMROSpace` collects from the classes
  along the resolution order;
- the resolution order a `Dispatcher` installed with `setattr` searches
  for its owner, and the marker `isFlex` reads.

A name the class does not hold now raises the plain `AttributeError` of
the lookup there, rather than whatever a hook answers for it.

### A variadic signature declared twice in one class body is refused

`BaseSpace.addVariadic` recorded every variadic declaration, and
collecting them for the `Dispatcher` kept the first of two equal
signatures, so a second `@overload(ARGS[int])` under one name in one
class body was dropped without a word, although the docstrings said the
most recent declaration wins. A second equal variadic signature bound to
a different function now raises `DuplicateSignature` at its line, as an
equal concrete signature always did; the same function bound again
changes nothing. Different variadic signatures that overlap, such as
`ARGS[int]` and `(int, ARGS[int])`, remain no conflict, and the most
recent declaration of the nearest class takes a call both accept. A
subclass may still redeclare a variadic signature it inherits.

### A BaseObject subclass without an initializer refuses constructor arguments

`Object.__init__` records whatever arguments it receives, which a
descriptor needs for its deferred default, so a `BaseObject` subclass
that defined no `__init__` of its own accepted any arguments and dropped
them: `Point(3, 4)` built a point at its defaults without a word.
`BaseObject.__init__` now raises the `TypeError` Python raises for a
plain class without an initializer, `Point() takes no arguments`, when
the class defines neither `__init__` nor `__new__` below `BaseObject`.
A subclass whose `__init__` hands its arguments on to `super().__init__`
still has them recorded, an overloaded initializer receives its
arguments as before, and `Object` and the descriptors built on it are
unchanged.

### An overloaded method carries the docstring of its function

The compiled dispatch a class exposes for an overloaded name carries the
docstring of the first registered function, else of the first variadic
one, else of the fallback, and the module of its owner, so `help` and
the documentation tools see what the author wrote; it used to carry only
its name and qualified name. A flexible declaration, `@overload.flex`,
registers a `PermuterMethod` around the function, and the dispatch read
the docstring of that wrapper's class whenever the flexible declaration
came first; it now reads the function the wrapper holds.

### A sentinel other than THIS is refused in an overload signature

`TypeSig.validateTypes` refused `OWNER` by name and accepted every other
sentinel class, so `@overload(DESC)` registered a signature nothing
could ever match, a sentinel class having no instances. `THIS` is now
handled first and passes, alone or inside a trailing `ARGS`, since
placement swaps it for the class; every other `Sentinel` subclass,
`OWNER`, `DESC`, `DELETED`, `METACALL` and `Sentinel` itself, is refused
with `TypeError` naming its position and the sentinel, at the decorator.

### Every exception shares a common base, WorkToyException

Every exception of `worktoy.waitaminute`, the control-flow signals
aside, subclasses `WorkToyException` ahead of the builtin it is based
on, so `except WorkToyException` catches every exception of the library
at once while `except TypeError`, `except AttributeError` and the other
builtin clauses keep working as before. The base adds nothing else: it
declares empty slots so that it stands beside `SyntaxError`, whose
layout is wider than that of `Exception`, and it carries no pickling or
copy support.

### A deleted plain name may be overloaded, through a deletion phase for the hooks

`LoadSpaceHook` records every plain binding of the class body so that
one body does not give a name both a plain definition and overloads,
and it kept that record past a deletion: `f = 1`, `del f`,
`@overload(int) def f` raised `OverloadConflict` although no plain
binding survived. The namespace hooks gained a deletion phase,
`delItemPhase(key, value)`, run by `AbstractNamespace.__delitem__` with
the name and the value being removed before the namespace removes it; a
hook returning `True` claims the deletion and the name stays. In that
phase `LoadSpaceHook` forgets the plain name, so the sequence above
builds and dispatches. A deleted overloaded name is still refused with
`ClaimedName` as the class is created.

### A Dispatcher wired by hand refuses what the overload decorator refuses

The `overload` decorator refuses a `staticmethod` or `classmethod`
object, and anything that cannot be called, with `TypeException` at the
decorator; the decorators of a `Dispatcher` wired by hand, `overload`,
`flex`, `fallback` and `finalize`, registered them and failed at the
first call. The one refusal now sits where every decorator of a
dispatcher passes, so both routes refuse alike and a refused
registration leaves the dispatcher as it was.

### A routed class hook is a classmethod and nothing else

`NamespaceHook` used to refuse a plain function or a `staticmethod` at
a routed `__class_*__` hook name with `UnboundClassHook`, and let
anything else through. An `@overload` there passed, became a
`Dispatcher` at compile time, and broke the operation at the first
call: `len(Y)` on a class whose body overloaded `__class_len__` raised
a `TypeError` about a missing instance. The rule is now the one the
documentation stated: a hook is a classmethod, and anything else at a
hook name, in the class body or supplied by a plain base, is refused
at the class-body line. The `METACALL` sentinel, which means the
metaclass's own implementation, passes, and so does a classmethod bound
again under a second hook name.

### A boxed value answers for its context through the box that made it

An `AttriBox` tags every object it creates with `__field_box__`,
`__field_name__` and `__field_owner__`, naming the box. An `Object` uses
the latter two names for its own placement record, and
`Object.getContextInstance` told "a value no class holds" from "a placed
descriptor read outside a frame" by `__field_name__` alone, so a boxed
value that is an `Object`, a `BaseObject`, a
`SymbolicName`, any descriptor, was taken for a placed descriptor:
`hasattr(value, 'instance')` raised `WithoutException` instead of
answering, and so did `inspect.getmembers` and anything else that walks
attributes.

A boxed value now answers `instance` and `owner` through the box that
made it. While that box has a frame, during the read that built or
fetched the value, `value.instance` is the instance read from and
`value.owner` the owner class, which an `onGet` callback can use.
Outside any frame the value is an ordinary object holding no context:
it raises `AttributeError`, `hasattr` answers `False`, and `inspect`
walks it. A placed descriptor read outside a frame still raises
`WithoutException`, and a value no box made is as it was.

### A subclass expands on an inherited descriptor through THIS

A class body may add notifiers to a descriptor it inherits by decorating
it through `THIS`, naming the base that holds the descriptor:

    class Child(Parent):

      @THIS[Parent].x.onGet
      def _onGetX(self, value) -> None:
        ...

`THIS[Parent].x` refers to the descriptor `x` that `Parent` holds, as the
class being built will hold it. Reading it takes a clone of `Parent.x`,
which derives the same storage name and so shares the field with the
parent's descriptor as a redeclared field does. The role decorators of
the reference, `preGet`, `onGet`, `preSet`, `onSet`, `preDelete`,
`onDelete` and `setName`, apply to that clone and hand the function back
as the descriptor's own decorators do, so the roles stack. `Parent`
receives an `__init_subclass__` that places the clone on the subclass as
it is created and names it there; `Parent.x` is never touched. Every
parent named takes a hook of its own, beside one a base of it holds, and
a hook hands over to the next along the resolution order as it runs, so
the parents may be named in any order across class bodies.
`THIS[GrandParent].x` is `THIS[Parent].x` for an `x` that `Parent`
inherits from `GrandParent`: one reference with one clone, named once.
Naming the
base is also what lets a static checker resolve the reference to
`Parent.x`, so a misspelled name is flagged and the roles complete. A
name `Parent` does not hold is refused at the line with `DanglingAlias`.
`BaseDescriptor` gained the `clone` that makes the copy, carrying the
captured arguments, the field type of a box and every registered
callback name, and no owner.

Decorating `Parent.x` directly from a subclass body still registers on
the parent's descriptor, which is what that line says.

A decorator may hold a subscript only from Python 3.9 on (PEP 614). On
3.7 and 3.8 the same decoration is written as a call after the method:

    class Child(Parent):

      def _onGetX(self, value) -> None:
        ...

      _onGetX = THIS[Parent].x.onGet(_onGetX)

Like the decorator, the call is written only inside the body of a
subclass of `Parent`. No other subclass of `Parent` may be created
before that body ends: the clone goes to the next subclass of `Parent`
created, so a subclass of `Parent` nested in the body would
take it and leave the enclosing class without the decoration. `worktoy`
is designed around custom metaclasses rather than nested classes; a
nested class may work, but edge cases such as this one are not
supported, as the package docstring now says.

`AttriBox.__get__` declares, as `BaseDescriptor` already did, that class
access gives the box itself, which the static resolution rests on.

### Alias forwards every access and keeps nothing

An `Alias` is a second name for a descriptor of its class or of a base:
`width = AttriBox[int](240)` beside `w = Alias('width')`. Through an
instance the alias now forwards each read, write and deletion to the
descriptor the real name holds on the class of that instance, found
afresh at every access as the first class dict along the resolution
order holds it, with no `__get__` run on it; the alias then runs that
protocol once itself. So `g.w` is the very object `g.width` gives, and
a subclass that redeclares the field is served by its own box whichever
name is read first. Read from the class, the alias is itself.

The alias used to replace itself on the class with the target object as
the class was created, whenever the target already resolved, and forward
only otherwise. A subclass redeclaring the field then kept reaching the
parent's box through the alias, and since both boxes store under the one
name the field derives, the first name read on a fresh subclass instance
decided what both names held afterwards. That swap is gone, and with it
the hand-written scan of the class dicts, the fallback to a name only
the metaclass supplies, and the three rules for a target holding a plain
value. A real name holding something that is not a descriptor is refused
with the new `NotADescriptor`, a `TypeError` naming the alias and the
value, since there is no protocol to forward to; a plain value takes a
second name by assignment. A value counts as a descriptor when its type
defines `__get__`, as for Python itself, so a proxy that answers
`__get__` only through `__getattr__` is refused too. As the class is
created the alias is held to
what it stands for, with three new refusals: a name no class along the
resolution order holds raises `DanglingAlias`, a name holding a plain
value raises `NotADescriptor`, and a `staticmethod` or `classmethod`,
which the class does not read as itself, raises `NotAliasable`, naming
the real name and both kinds, since through the class the two names
would not agree. The first two refusals come again from an access should
the name be removed or replaced on the class afterwards. A plain
function is read as itself and may be aliased. Two things change for a
user: read from the class, an alias is no longer the box it stands for,
and an alias follows the name it stands for in the class body or in a
base, since an alias of a name a subclass supplies later is refused.

#### Rationale

A second name should mean what the first name means, found the way the
first name is found, every time. The copy taken at class creation was a
shortcut that broke under redeclaration, and the rules kept around it
served cases an alias is not for.

### Keyword arguments pass through overload dispatch

An overloaded call is dispatched on the types of its positional
arguments alone. Its keyword arguments play no part in choosing the
overload and pass through unchanged to the function the positional
types select. A call with no positional arguments selects the empty
signature, `@overload()`, so a class that takes keywords declares that
overload and handles them there, forwarding from its other overloads
with `if kwargs: self.__init__(**kwargs)`, as the samplers of
`work_test` have always done. A keyword the selected function does not
take is refused by that function with Python's own `TypeError`, which
names it. A call no signature accepts still goes to the fallback, else
`DispatchException`, which still lists the keywords received.

The dispatcher used to bind keywords to the parameter names of every
registration, so that `Point(x=69, y=420)` reached `@overload(int, int)`
declared on `(self, x, y)` without an empty signature. That binding
needed rules of its own: which keyword fills which name, how a keyword
beyond the signature is absorbed by a later parameter or `**kwargs`,
how a `flex` registration binds its canonical names, why a variadic one
binds none, and a second set of three matching tiers over the bound
values. The list it bound against held one entry per function, so a
function stacked under several signatures was reachable by keyword
through its first signature only. All of it is gone. What a project
loses is the keyword form of a positional overload without a handler
for it: `Point(x=69, y=420)` now needs `@overload()` on `Point`, or is
refused, and `Point(69, y=420)` dispatches on `(int,)`, not on
`(int, int)`.

#### Rationale

One lenient acceptance, that a keyword call should still find a
positional overload, had grown a binder with its own rule set, each
rule with an edge, and the first bug found in it needed one more
condition. The plain rule needs none, and the forwarding pattern it
rests on was already how the library's own constructors took keywords.

### AttriBox declarations are settled when the class is created

Several ways of writing an `AttriBox` declaration used to be accepted in
silence and then misbehave later, or never behave at all. Each is now
settled at the declaration itself, which is where the offending line
actually sits.

A subscript naming something other than a plain type, such as
`AttriBox[list[int]]` or `AttriBox[T]`, is handed to the generic
machinery and comes back as a type alias rather than a box. An alias
carries none of the descriptor protocol, so the attribute quietly
answered with the alias object on every read. Such a declaration now
raises `PhantomBoxError` while the class is being built. The subscript
on its own remains legal, because `class Sub(AttriBox[T])` asks for
exactly that alias and a base-class entry is not a namespace value. What
is refused is the alias landing in a class body as an attribute.

A box that never captured a field type, written `AttriBox()` or produced
by calling one of the aliases above, has nothing to build from and no
later chance to learn a field type, since the subscript is the only
place one is ever assigned. It now raises `MissingVariable` as the class
is created, rather than at the first read of the attribute.

A subscript written without its trailing call, `bar = AttriBox[int]`, is
now completed instead of left half-built. The subscript already fixed
the field type, so the only thing the missing parentheses withheld is
the deferred argument list, and an absent list is read as an empty one.
Such a declaration now behaves exactly as `bar = AttriBox[int]()`.

A box installed on a finished class through `setattr` never reaches
`__set_name__`, so both refusals above are repeated on read for that
route.

#### Rationale

A malformed declaration used to surface as a puzzling value or an
exception raised several frames inside the descriptor machinery, at
whatever unrelated line happened to read the attribute first. The class
body that caused it could be in another file entirely. Refusing at class
creation names the attribute, the owning class and the subscript as
written, and does so before any instance exists.

The three spellings are not treated alike, because only one of them
leaves anything to work with. A missing pair of parentheses withholds an
argument list that has an obvious default, so it is completed. A
subscript the box declines to claim, or no subscript at all, leaves no
field type and therefore nothing to construct, so it is refused.

### New exception: PhantomBoxError

`PhantomBoxError` is added to `worktoy.waitaminute.desc` and raised when
a class-body subscript produced a type alias in place of a box. Its
message reports the attribute name, the owning class, and the subscript
as it was written, along with the completed form the declaration wanted.

It subclasses `DescriptorException` and deliberately does not subclass
`AttributeError`. A declaration error that presented as an
`AttributeError` would be swallowed by `hasattr` and by `getattr` with a
default, turning a broken class body into a silently absent attribute.

`AccessError`, `ProtectedError`, `ReadOnlyError` and `PhantomBoxError`
now share the `DescriptorException` base, so a single
`except DescriptorException` still catches all of them.

### Object reports inconsistent state instead of failing obscurely

`Object` now checks the invariants its accessors depend on and reports
the missing piece by name. `getContextInstance` and `getContextOwner`
refuse an absent context stack, which a subclass can produce by
overriding the public `hasContext` in a way that disagrees with the
stack it summarises. `getPrivateName` reports a missing field name
rather than building an attribute name out of `None`, which is reachable
whenever a descriptor is used without having gone through a class body.
The deleted-value guard likewise reports a missing field name rather
than naming the deleted attribute `None`.

### Box storage names are the field name as written

A box stores the value of a field on each instance under a name derived
from the field name. That name used to be the snake-cased private name
of the field, so `fooBar` and `foo_bar`, or `X` and `x`, derived one
storage name and shared one slot; such a pair was refused with
`StorageCollision` as the class was created, and a subclass redeclaring a
field its parent exposed under a second name through `Alias` was refused
by the same guard, wrongly, since the guard met the parent's box under the
alias name and compared it with itself.

The storage name now takes the field name as written, wrapped in double
underscores and followed by the lower-case name of the box class and
`_field_object__`: an `AttriBox` named `fooBar` stores at
`__fooBar__attribox_field_object__`. Two different field names can never
derive one storage name, so two near names are two fields with two slots,
as plain Python has them, the guard is gone, and `StorageCollision` with
it. An instance pickled by an earlier release holds its values under the
old storage names; loaded under this one, those fields rebuild their
defaults on the first read.

### The testing support no longer depends on lorem_ipsum

`worktoy.work_test` drew its random text from `worktoy.lorem_ipsum`: the
word and symbolic-name samplers from `StochasticWord`, the lorem sampler
from a `Sentence` of its own, and `BaseTest` exposed both generators as
`stochWord` and `loremSentence`. The samplers now draw from a small
vocabulary of their own, `LOREM_WORDS` in `worktoy.work_test.samplers`,
through `randomWord` and `loremSentence`, which builds a sentence of
exactly the requested number of characters. `LoremSampler.charCount` is a
plain per-sampler setting, forty by default, refusing a count below one;
the `sentence` attribute is gone, and so are `BaseTest.stochWord` and
`BaseTest.loremSentence`. `work_test` therefore depends on the central
packages alone, which a test pins by reading the import statements of
every module in the package.

## [1.0.0] - 2026 May 29

First stable release. The public API is frozen for the 1.0 series.

### Relicensed from AGPL-3.0 to Apache-2.0

worktoy is now distributed under the Apache License 2.0, replacing the
AGPL-3.0 license used throughout the pre-1.0 development series.

#### Rationale

AGPL-3.0 was originally chosen for one reason: to stop a large company
from folding worktoy into a closed-source product. The clearest version
of that worry is training data, and AGPL was meant to make such use a
copyleft violation rather than a free lunch.

In practice it changed nothing about that threat. Long-removed, renamed
internals of worktoy (for example the abandoned `monoSpace` feature)
already surface in the pre-knowledge of commercial language models,
which means the source was ingested into training weights regardless of
the license. If copying source into training data and model weights is
not treated as derivation, then the one outcome AGPL was chosen to
prevent is simply not prevented.

So the restrictive license bought nothing against the actor it was aimed
at, while it did deter the honest ones: many organizations refuse AGPL
dependencies outright as a matter of policy. A lock that only stops the
law-abiding and waves the scrapers through is not worth keeping.

Apache-2.0 keeps worktoy freely usable, adds an explicit patent grant,
and has clearer terms than a bare permissive license such as MIT.

#### Scope

The `LICENSE` file now holds the canonical Apache-2.0 text. The per-file
license headers, the `pyproject.toml` classifier, the README badge and
license section, and the Code of Conduct were all updated to match.
Copyright remains with Asger Jon Vistisen; only the license terms
changed.

The relicense first shipped in 1.0.0-rc7. Earlier candidates, up to and
including 1.0.0-rc6, remain available under AGPL-3.0; every release from
1.0.0-rc7 onward is Apache-2.0.

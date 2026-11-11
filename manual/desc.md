# worktoy manual: desc

`worktoy.desc` gives a class typed attributes, declared in the class
body, with defaults built for each instance and assignments held to the
type. It is the part of worktoy most projects use first.

Everything shown here is promised. The examples are checked against
every release, so they keep working in every update. Anything this
chapter does not show may change.

Contents:

1. Which one to use
2. `AttriBox`: a typed attribute with a default
3. Reacting to reads and writes
4. `FixBox`: set once
5. `FastBox`: strict and fast
6. `Field`: an attribute made of methods
7. `Alias`: a second name
8. `SymbolicName`: one name in every convention
9. A subclass watching an inherited attribute: `THIS[Parent].name`


## 1. Which one to use

- `AttriBox` for an ordinary typed attribute: a default built for each
  instance, assignments converted to the type or refused. Start here.
- `FixBox` for one that is set once and never changes.
- `FastBox` for one read in a hot loop, where every conversion and
  callback costs too much.
- `Field` for one computed or guarded by methods, as a `property` is.
- `Alias` for a second name of an attribute.

The boxes work in any class, a plain one included, and generate
nothing: no `__init__`, `__repr__` or `__eq__`. The `ezdata` chapter
describes the dataclass that does. Where a box keeps a value is not
promised; read it through the attribute.

The seven callbacks of section 3 are for the author of a class
reacting to its attributes. Writing a descriptor of your own is the
core chapter's `Object`, or `BaseDescriptor`, which is an `Object` that
takes the seven callbacks as well.


## 2. `AttriBox`: a typed attribute with a default

```
>>> from worktoy.mcls import BaseObject
>>> from worktoy.desc import AttriBox
>>> class Point(BaseObject):
...   x = AttriBox[float](0.0)
...   y = AttriBox[float](0.0)
>>> point = Point()
>>> point.x
0.0
>>> point.x = 3
>>> point.x
3.0

```

The subscript gives the type and the parentheses the arguments of the
default. The default is built at the first read, for each instance
apart, by calling the type with those arguments, and kept for every
later read:

```
>>> class Gear(BaseObject):
...   def __init__(self, teeth):
...     self.teeth = teeth
>>> class Machine(BaseObject):
...   gear = AttriBox[Gear](12)
>>> machine = Machine()
>>> machine.gear.teeth
12
>>> machine.gear is Machine().gear
False

```

Things to know about defaults:

- The default is built by the constructor of the type, so
  `AttriBox[int]('3')` holds `3`. An assignment converts only as
  `typeCast` does, so assigning `'3'` later is refused. The declaration
  line may parse; an assignment never does.
- A lone argument already of the type is deep-copied for each instance,
  so no two instances ever share a mutable default. One that cannot be
  copied, as a lock, raises `TypeError` at the first read; give the
  type no arguments instead, `AttriBox[threading.Event]()`, to build a
  new one for each instance.
- Among the arguments, `THIS` becomes the instance and `OWNER` its
  class, so a part can know what holds it. Only an argument that is the
  placeholder itself is replaced, not one inside a list.
- `AttriBox[THIS]` types the attribute with the class declaring it, as
  for the parent of a node in a tree.
- A box always holds a value of its type. There is no `Optional`: an
  attribute that may be absent is better deleted, or modelled with a
  sentinel of the core chapter.

```
>>> from worktoy.core.sentinels import THIS
>>> class Part(BaseObject):
...   def __init__(self, holder):
...     self.holder = holder
>>> class Engine(BaseObject):
...   part = AttriBox[Part](THIS)
>>> engine = Engine()
>>> engine.part.holder is engine
True

```

An assigned value of the type is kept as it is, so a `bool` assigned
to an `AttriBox[int]` stays a `bool`. Any other value converts as
`typeCast` converts it, or is refused with `TypeException` naming the
field:

```
>>> from worktoy.waitaminute import TypeException
>>> try:
...   point.x = 'three'
... except TypeException as refusal:
...   print(refusal.varName, refusal.actualObject)
x three

```

After a deletion, a read raises `MissingVariable`, an `AttributeError`,
until a value is assigned again; the default is not built a second
time. A copy of an instance copies its values, and an instance of a
class defined at the top of a file pickles with them.

As the class is created, a box declared without parentheses is
refused with `TypeError`, and so is a box in a class whose instances
have no `__dict__`, as a class declaring `__slots__`, with
`MissingInstanceDict`. One box object cannot serve two classes, which
raises `SharedDescriptor`; to reuse a declaration, write a small
function returning a new box. And mind this one:

```
>>> class Pair(BaseObject):
...   left = AttriBox[int](1)
...   right = left
>>> pair = Pair()
>>> pair.left = 5
>>> pair.right
1

```

A box bound to a second name in the same body gives a second, separate
attribute. For a second name of the same attribute, use `Alias`.


## 3. Reacting to reads and writes

Every box, and `Field`, takes seven decorators, each registering a
method of the class:

- `preGet(self)` before a read, `onGet(self, value)` after it;
- `preSet(self, value)` before a write, `onSet(self, value)` after it;
- `preDelete(self)` and `onDelete(self)` around a deletion;
- `setName(cls, desc)`, a classmethod, as the class is created.

```
>>> class Account(BaseObject):
...   balance = AttriBox[float](0.0)
...   @balance.preSet
...   def _checkBalance(self, value):
...     if value < 0:
...       raise ValueError('a balance cannot be negative')
...   @balance.onSet
...   def _audit(self, value):
...     print('balance is now', value)
>>> account = Account()
>>> account.balance = 5
balance is now 5.0
>>> try:
...   account.balance = -1
... except ValueError as error:
...   print(error)
a balance cannot be negative
>>> account.balance
5.0

```

- `preSet` sees the value as assigned, `5`, before any conversion; it
  refuses by raising, or skips the write silently by raising `SkipSet`
  of the core chapter. `onSet` sees the value as stored, `5.0`.
- Building the default at the first read is no write: no `preSet` or
  `onSet` runs for it.
- Several `onSet`s on one box run in the order written, and one method
  may serve two boxes by stacking `@width.onSet` and `@height.onSet`.
- A method may declare fewer parameters than it is passed, as `_read(self)`
  for an `onGet`. A `staticmethod` receives the value alone.
- The method is found by its name on the class of the instance at each
  access, so a subclass defining `_audit` replaces it. To keep the
  base's as well, call it from the subclass: `Account._audit(self,
  value)`.
- The method must be a method of the class, `__audit` style names
  included. A lambda has no name to find and raises `NamelessCallback`.


## 4. `FixBox`: set once

A `FixBox` is an `AttriBox` whose first stored value is final:

```
>>> from worktoy.desc import FixBox
>>> from worktoy.waitaminute.desc import WriteOnceError
>>> class Config(BaseObject):
...   port = FixBox[int](8080)
>>> config = Config()
>>> config.port = 9000
>>> try:
...   config.port = 9001
... except WriteOnceError as refusal:
...   print('fixed at', refusal.oldValue)
fixed at 9000

```

A second assignment raises `WriteOnceError`, a `TypeError`, even of the
same value, and a deletion raises `ProtectedError`. Mind that a read
stores the default it builds: anything reading the attribute first, a
log line or a debugger included, fixes it at the default. Assign a value
meant for run time before anything reads it.


## 5. `FastBox`: strict and fast

A `FastBox` gives up everything that costs time: no conversion on
assignment, no callbacks, no placeholders. A read is one dictionary
lookup.

```
>>> from worktoy.desc import FastBox
>>> class Particle(BaseObject):
...   mass = FastBox[float](1)
>>> particle = Particle()
>>> particle.mass
1.0
>>> try:
...   particle.mass = 2
... except TypeException:
...   print('2 is no float')
2 is no float

```

The declared value is converted once, on the declaration line, and
shared by every instance until one assigns its own, so it must be
hashable. Empty parentheses give each instance a new `fieldType()`
instead. An assignment must be an instance of the type already, a `bool`
passing for an `int`. A deletion makes the next read start over from the
declared value, where an `AttriBox` raises `MissingVariable`. A
`FastBox` declared without parentheses, given an unhashable value, or
called on the class again raises `TypeError`.


## 6. `Field`: an attribute made of methods

A `Field` is an attribute computed or guarded by methods, as a
`property` is. `GET`, `SET` and `DELETE`, in capitals, define what the
attribute is; the seven callbacks of section 3 only react to it.

```
>>> from worktoy.desc import Field
>>> class Circle(BaseObject):
...   __radius__ = 1.0
...   radius = Field()
...   @radius.GET
...   def _getRadius(self):
...     return self.__radius__
...   @radius.SET
...   def _setRadius(self, value):
...     self.__radius__ = value
>>> class BigCircle(Circle):
...   def _getRadius(self):
...     return 10 * self.__radius__
>>> BigCircle().radius
10.0

```

What `Field` adds over a `property`: the methods are found by name at
each access, so a subclass overriding `_getRadius` changes the
attribute without declaring it again. A second `GET` replaces the
first; several `SET`s and `DELETE`s run in the order written. A read
without a getter raises `AccessError`, a write without a setter
`ReadOnlyError`, a deletion without a deleter `ProtectedError`, all
`AttributeError`s.


## 7. `Alias`: a second name

```
>>> from worktoy.desc import Alias
>>> class Geometry(BaseObject):
...   width = AttriBox[int](240)
...   w = Alias('width')
>>> geometry = Geometry()
>>> geometry.w = 300
>>> geometry.width
300

```

Both names read, write and delete the one value, with the same
callbacks. The name may belong to a base, and the alias follows a
subclass that declares the attribute again. A method may be aliased
too, and a write through such an alias raises `ReadOnlyError`. The name
is a string, so a rename by your editor may miss it; but a name no class
holds raises `DanglingAlias` as the class is created, and one holding a
plain value, as `x = 3`, raises `NotADescriptor`.


## 8. `SymbolicName`: one name in every convention

```
>>> from worktoy.desc import SymbolicName
>>> name = SymbolicName('font', 'size')
>>> name.snake, name.camel, name.pascal, name.screamingSnake
('font_size', 'fontSize', 'FontSize', 'FONT_SIZE')

```

`kebab` and `screamingKebab` give `font-size` and `FONT-SIZE`. The
words are kept as given and never split, so build one from words, not
from `'fontSize'`. Every word is capitalized as `str.capitalize` does,
so `HTTPServer` becomes `Httpserver`; give an acronym as a word of its
own. Two names of the same words are equal whatever their case, but a
name is never equal to a string.


## 9. A subclass watching an inherited attribute: `THIS[Parent].name`

A subclass sometimes needs a callback on an attribute it inherits,
without changing the base's attribute, which other subclasses share.
`THIS[Speaker].volume` stands for the attribute as the subclass will
hold it:

```
>>> class Speaker(BaseObject):
...   volume = AttriBox[int](5)
>>> class LoudSpeaker(Speaker):
...   def _report(self, value):
...     print('volume', value)
...   _report = THIS[Speaker].volume.onSet(_report)
>>> LoudSpeaker().volume = 7
volume 7
>>> Speaker().volume = 3

```

From Python 3.9 the same is written as a decorator:

```python
class LoudSpeaker(Speaker):
  @THIS[Speaker].volume.onSet
  def _report(self, value):
    print('volume', value)
```

The subclass gets an attribute of its own, and the base keeps its own
as it was; the parent named may be any class above the one holding the
attribute, and a `Field` takes it as a box does. On 3.7 and 3.8 the
call form above goes after the method, in the same class body.

Mind the trap: writing `Speaker.volume.onSet` in the subclass body,
without `THIS`, registers on the base's own attribute, as that line
says, so every `Speaker` then looks for the method too. A body
declaring `volume` itself decorates that one directly, and doing both
raises `ReferenceConflict`; a name no class holds raises
`DanglingAlias`.

`THIS` is the same marker throughout worktoy: it stands for the class
being defined, or for something of it the class body cannot name yet.
Where a value is built, as in the arguments of a box, it is the
instance; in an overload signature, the class; and here, the attribute
as the subclass will hold it.

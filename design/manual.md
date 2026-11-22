[![wakatime](https://wakatime.com/badge/github/AsgerJon/WorkToy.svg)](https://wakatime.com/badge/github/AsgerJon/WorkToy)
[![Tokens](https://img.shields.io/badge/Tokens-24.9B-D97757)](https://claude.com/claude-code)
[![codecov](https://codecov.io/gh/AsgerJon/WorkToy/graph/badge.svg?token=FC0KFZJ7JK)](https://codecov.io/gh/AsgerJon/WorkToy)
[![PyPI version](https://img.shields.io/pypi/v/worktoy)](https://pypi.org/project/worktoy/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

# worktoy v1.2.3-dev0 (development build)

**worktoy** provides utilities for Python development focused on
reducing boilerplate while improving type safety and readability. Each
release is tested thoroughly on each supported Python version from 3.7*
to 3.15.

*Maybe it is time to consider updating if you are still using Python 3.7.

# Table of Contents

- [Installation](#installation)
- [Python Is Easy. Too Easy!](#python-is-easy-too-easy)
    - ['Trust-Me-Bro'-Typing](#trust-me-bro-typing)
    - [The Python Parsing Situation Is Crazy](#the-python-parsing-situation-is-crazy)
    - ["Show Don't Tell" Is for Stories, not for Code!](#show-dont-tell-is-for-stories-not-for-code)
    - [Static Discipline](#static-discipline)
- [Contributing](#contributing)
- [License](#license)

# Installation

Install with pip:

```bash
pip install worktoy
```

# Python Is Easy. Too Easy!

What enables effortless prototyping does not guarantee the scalable
structure serious applications demand.

Introducing worktoy.

A structural layer for Python that adds deliberate constraints without
sacrificing ergonomics. It brings the architectural discipline of
statically typed languages to dynamic Python.

Build the GUI. Build the logic. Build the architecture.
All in Python.

## 'Trust-Me-Bro'-Typing

```python
class Point:
  def __init__(self, x: float = 0.0, y: float = 0.0) -> None:
    self.x = x
    self.y = y
```

The above code is perfectly valid Python, it even includes types. Or does
it? Those `float` annotations are not there at runtime. Basically, it is
'trust-me-bro'-typing. `Point('breh', None)` will happily create a `Point`
object.

Instead:

```python
from worktoy.desc import AttriBox


class Point:
  x = AttriBox[float](0.0)
  y = AttriBox[float](0.0)

  def __init__(self, x: float = 0.0, y: float = 0.0) -> None:
    self.x = x
    self.y = y
```

When `AttriBox` says `float` it enforces `float` at runtime.
Attributes are declared explicitly at the class level. Despite this,
flexibility remains, for example:

```python
point = Point(69, 420)  # int, int
point.x == 69.0
point.y == 420.0
```

When types do not match, `AttriBox` converts what converts without loss,
as an `int` to a `float`, and refuses the rest: `Point(69, '420')` raises
`TypeException`, since no string is ever parsed. Same ergonomics. Stronger
guarantees.

Note that `Point` above is a plain class: both `AttriBox` and `Field`
are ordinary descriptors and work on any class. The `BaseObject` base
shown in the examples below is required only for the `@overload`
machinery, not for declarative attributes.

## The Python Parsing Situation Is Crazy

Python is not always easy though. Consider the `Point` implementation
under discussion. Suppose we wanted a flexible constructor. One that
supports instantiation on:

- a pair of `float` objects
- a complex number
- another `Point` object

That is possible in Python, for example:

```python

class Point:

  def __init__(self, *args, ) -> None:
    if len(args) == 2:
      self.x = float(args[0])
      self.y = float(args[1])
    elif len(args) == 1:
      if isinstance(args[0], complex):
        self.x = args[0].real
        self.y = args[0].imag
      elif isinstance(args[0], type(self)):
        self.x = args[0].x
        self.y = args[0].y
    else:
      raise TypeError('Invalid arguments')
```

Possible? Sure, but look at that syntactic broccoli! Conditional branches.
Growing complexity. Manual parsing. Long gone are those happy days of
effortless coding.

But it does not have to be like this. Introducing `@overload`:

```python
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.mcls import BaseObject
from worktoy.core.sentinels import THIS
from worktoy.dispatch import overload
from worktoy.desc import AttriBox

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Self


class Point(BaseObject):
  x = AttriBox[float](0.0)
  y = AttriBox[float](0.0)

  @overload(float, float)
  def __init__(self, x: float, y: float) -> None:
    self.x = x
    self.y = y

  @overload(complex)
  def __init__(self, z: complex) -> None:
    self.x = z.real
    self.y = z.imag

  @overload(THIS)  # THIS = the enclosing class (matches an instance of it)
  def __init__(self, other: Self) -> None:
    self.x = other.x
    self.y = other.y

  @overload()
  def __init__(self, ) -> None:
    pass

```

Each new signature requires one new overloaded function. No more painful
parsing of `*args`. All of this just works. Actually.

## "Show Don't Tell" Is for Stories, not for Code!

When reading code, you look for declarations.
For where symbols are defined. For where meaning begins.

Narrative storytelling is different. The method by which information is
conveyed is itself part of the artistic expression. The way
information is revealed is frequently as important as the information
itself. In *Clair Obscur: Expedition 33*, the horror of the *Gommage*
unfolds gradually until Sophie disappears from Gustave's arms. The
imperative subtlety grants the story its emotional impact.

In code, the declaration **is** the point! In matters of code, I want
declarations. I don't want foreshadowing. I don't want subtlety. I don't
want subversion of expectations. I want declarations.

Anyway, what were we talking about?
Right, figure out what `point.r` is from the code below:

```python
class Point:
  def __init__(self, *args, ) -> None:
    if len(args) == 2:
      self.x = float(args[0])
      self.y = float(args[1])
    elif len(args) == 1:
      if isinstance(args[0], complex):
        self.x = args[0].real
        self.y = args[0].imag
      elif isinstance(args[0], type(self)):
        self.x = args[0].x
        self.y = args[0].y
    else:
      raise TypeError('Invalid arguments')

  @property
  def r(self) -> float:
    return (self.x ** 2 + self.y ** 2) ** 0.5
```

Great, you found it. Well, you found what it does, and you inferred it.
This is *imperative* declaration. In Python, this is fine. It is much
worse in other languages. Anyway, here is the alternative provided by
**worktoy**: `Field`.

```python
from worktoy.desc import Field


class Point(BaseObject):
  x = AttriBox[float](0.0)
  y = AttriBox[float](0.0)

  r: Field[float] = Field()  # Straight up declaration!

  @overload(float, float)
  def __init__(self, x: float = 0.0, y: float = 0.0) -> None:
    self.x = x
    self.y = y

  @overload(complex)
  def __init__(self, z: complex) -> None:
    self.x = z.real
    self.y = z.imag

  @overload(THIS)  # THIS = the enclosing class (matches an instance of it)
  def __init__(self, other: Self) -> None:
    self.x = other.x
    self.y = other.y

  @overload()
  def __init__(self, ) -> None:
    pass

  @r.GET  # Straight up declaration of something called 'GET'.
  def _getR(self) -> float:
    return (self.x ** 2 + self.y ** 2) ** 0.5
```

The `r` attribute is declared first. Next, the `@r.GET` declares that the
method implementing the get operation comes next. The structure is
visible separately from the behaviour.

## Static Discipline

In plain Python, attributes assigned in `__init__` are closer to
dictionary entries than declared structure.

```python
class Point:
  def __init__(self, x: float = 0.0, y: float = 0.0) -> None:
    self.x = x
    self.y = y
```

Inspecting the class reveals nothing about `x` or `y`. They do not exist
at the class level. They are created at runtime on the instance. Two
common remedies are `__slots__` and annotations:

```python
class Point:
  __slots__ = ('x', 'y')

  def __init__(self, *args) -> None: ...
```

or

```python
class Point:
  x: float
  y: float

  def __init__(self, *args, ) -> None: ...  # Implementation as before
```

Both improve clarity, but neither makes `x` and `y` part of the class.
With annotations alone, `Point.x` raises `AttributeError`; with
`__slots__`, `Point.x` is a bare slot that knows nothing of the type.
Either way the values appear only once `__init__` sets them, as attributes
of the instance, and setting them there makes no difference compared to
setting them anywhere else. Structure remains implicit.

With **worktoy** attributes are an essential part of the class structure
on par with methods.

```python
class Point(BaseObject):
  x = AttriBox[float](0.0)
  y = AttriBox[float](0.0)

  #  Implementation as before
```

Now `x` and `y` are declared at the class level, making them visible,
inspectable and enforced. They are more than just keys in an instance
dictionary. They are structural elements of the class. In plain Python,
instances define structure. Here, the class does.

# Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for
the style rules and development setup.

# License

worktoy is released under the Apache License 2.0 (Apache-2.0). See
[LICENSE](LICENSE) for the full text.

# The Manual

The README above ends with a class whose structure is declared instead
of inferred: `Point`, with two typed attributes, a constructor for each
kind of argument, and an attribute computed from the other two. This is
that class, whole:

```
>>> from worktoy.mcls import BaseObject
>>> from worktoy.core.sentinels import THIS
>>> from worktoy.dispatch import overload
>>> from worktoy.desc import AttriBox, Field
>>> class Point(BaseObject):
...   x = AttriBox[float](0.0)
...   y = AttriBox[float](0.0)
...   r = Field()
...   @overload(float, float)
...   def __init__(self, x, y):
...     self.x = x
...     self.y = y
...   @overload(complex)
...   def __init__(self, z):
...     self.x = z.real
...     self.y = z.imag
...   @overload(THIS)
...   def __init__(self, other):
...     self.x = other.x
...     self.y = other.y
...   @overload()
...   def __init__(self):
...     pass
...   @r.GET
...   def _getR(self):
...     return (self.x ** 2 + self.y ** 2) ** 0.5

```

And this is what the README said it does, run:

```
>>> Point(69, 420).y
420.0
>>> Point(3 + 4j).r
5.0
>>> Point(Point(3.0, 4.0)).x
3.0
>>> Point().r
0.0
>>> point = Point()
>>> try:
...   point.x = '420'
... except TypeError:
...   print('refused: no string is ever parsed')
refused: no string is ever parsed

```

From here the document goes into ever more detail. It begins with the
three things `Point` is made of, the typed attribute, the overload and
the field, and then takes the rest of the library one package at a
time. Each part answers one question:

- How do I give a class typed attributes with defaults? `worktoy.desc`
- How do I let one method take several kinds of arguments?
  `worktoy.dispatch`
- How do I make the class itself iterable, callable or checked as it is
  written? `worktoy.mcls`
- How do I declare an enumeration or a set of flags? `worktoy.keenum`
- How do I declare a small class that only holds data? `worktoy.ezdata`
- How do I write a descriptor of my own? `worktoy.core`
- Which small helpers come along? `worktoy.utilities`
- Something raised: what does the exception tell me?
  `worktoy.waitaminute`
- How do I get placeholder text? `worktoy.lorem_ipsum`
- What helps me test my own classes? `worktoy.work_test`
- What can I rely on from one release to the next? The last part.

Every example in this document is run against every release.

## `worktoy.desc`

`worktoy.desc` gives a class typed attributes, declared in the class
body, with defaults built for each instance and assignments held to the
type. It is the part of worktoy most projects use first.

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


### 1. Which one to use

- `AttriBox` for an ordinary typed attribute: a default built for each
  instance, assignments converted to the type or refused. Start here.
- `FixBox` for one that is set once and never changes.
- `FastBox` for one read in a hot loop, where every conversion and
  callback costs too much.
- `Field` for one computed or guarded by methods, as a `property` is.
- `Alias` for a second name of an attribute.

The boxes work in any class, a plain one included, and generate
nothing: no `__init__`, `__repr__` or `__eq__`. The `ezdata` part
describes the dataclass that does. Where a box keeps a value is not
promised; read it through the attribute.

The seven callbacks of section 3 are for the author of a class
reacting to its attributes. Writing a descriptor of your own is the
core part's `Object`, or `BaseDescriptor`, which is an `Object` that
takes the seven callbacks as well.


### 2. `AttriBox`: a typed attribute with a default

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
  copied, as a lock, is refused with `TypeError` at the first read; give
  the type no arguments instead, `AttriBox[threading.Event]()`, to build
  a new one for each instance.
- Among the arguments, `THIS` becomes the instance and `OWNER` its
  class, so a part can know what holds it. Only an argument that is the
  placeholder itself is replaced, not one inside a list.
- `AttriBox[THIS]` types the attribute with the class declaring it, as
  for the parent of a node in a tree.
- A box always holds a value of its type. There is no `Optional`: an
  attribute that may be absent is better deleted, or modelled with a
  sentinel of the core part.

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

After a deletion, a read is refused with `MissingVariable`, an
`AttributeError`, until a value is assigned again; the default is not
built a second time. A copy of an instance copies its values, and an
instance of a class defined at the top of a file pickles with them.

As the class is created, a box declared without parentheses is refused
with `TypeError`, and so is a box in a class whose instances have no
`__dict__`, as a class declaring `__slots__`, with
`MissingInstanceDict`. One box object cannot serve two classes, which is
refused with `SharedDescriptor`; to reuse a declaration, write a small
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


### 3. Reacting to reads and writes

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
  of the core part. `onSet` sees the value as stored, `5.0`.
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
  included. A lambda has no name to find and is refused with
  `NamelessCallback`.


### 4. `FixBox`: set once

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

A second assignment is refused with `WriteOnceError`, a `TypeError`,
even of the same value, and a deletion is refused with `ProtectedError`.
Mind that a read stores the default it builds: anything reading the
attribute first, a log line or a debugger included, fixes it at the
default. Assign a value meant for run time before anything reads it.


### 5. `FastBox`: strict and fast

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
declared value, where an `AttriBox` refuses the read with
`MissingVariable`. A `FastBox` declared without parentheses, given an
unhashable value, or called on the class again is refused with
`TypeError`.


### 6. `Field`: an attribute made of methods

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
each access, so a subclass overriding `_getRadius` changes the attribute
without declaring it again. A second `GET` replaces the first; several
`SET`s and `DELETE`s run in the order written. A read without a getter
is refused with `AccessError`, a write without a setter `ReadOnlyError`,
a deletion without a deleter `ProtectedError`, all `AttributeError`s.


### 7. `Alias`: a second name

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
subclass that declares the attribute again. A method may be aliased too,
and a write through such an alias is refused with `ReadOnlyError`. The
name is a string, so a rename by your editor may miss it; but a name no
class holds is refused with `DanglingAlias` as the class is created, and
one holding a plain value, as `x = 3`, is refused with `NotADescriptor`.


### 8. `SymbolicName`: one name in every convention

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


### 9. A subclass watching an inherited attribute: `THIS[Parent].name`

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
says, so every `Speaker` then looks for the method too. A body declaring
`volume` itself decorates that one directly, and doing both is refused
with `ReferenceConflict`; a name no class holds is refused with
`DanglingAlias`.

`THIS` is the same marker throughout worktoy: it stands for the class
being defined, or for something of it the class body cannot name yet.
Where a value is built, as in the arguments of a box, it is the
instance; in an overload signature, the class; and here, the attribute
as the subclass will hold it.

## `worktoy.dispatch`

Python keeps only the last function bound to a name in a class body,
so a method cannot be written once per signature. `worktoy.dispatch`
makes that possible: declare the method once per signature with
`@overload`, and each call goes to the declaration its arguments match.

Contents:

1. Where overloading works
2. Declaring a method per signature
3. How a call finds its declaration
4. Several signatures, any order, a tail, a fallback
5. Classmethods, staticmethods and subclasses
6. Mistakes caught at the declaration
7. The building blocks


### 1. Where overloading works

`@overload` works in the body of a class built by `BaseMeta`, the
metaclass behind `BaseObject`, which the metaclass part describes.
The decorator only records a signature; the class turns the records of
each name into one dispatcher as it is created. So there is no
overloading of a module-level function, and an `@overload` left in a
plain class is refused as that class is created, as section 6 shows.

The classes go in the decorator. The annotations of the function are
not read, so write them as you like, or leave them out. And the name
`overload` is not `typing.overload`, which serves type checkers only;
if a file needs both, import one of them under another name.


### 2. Declaring a method per signature

```
>>> from worktoy.mcls import BaseObject
>>> from worktoy.desc import AttriBox
>>> from worktoy.dispatch import overload
>>> class Money(BaseObject):
...   amount = AttriBox[float](0.0)
...   currency = AttriBox[str]('EUR')
...   @overload(float, str)
...   def __init__(self, amount, currency):
...     self.amount, self.currency = amount, currency
...   @overload(float)
...   def __init__(self, amount):
...     self.amount = amount
...   @overload()
...   def __init__(self):
...     pass
>>> usd = Money(2.5, 'USD')
>>> usd.amount, usd.currency
(2.5, 'USD')
>>> Money(4.0).currency
'EUR'
>>> Money().amount
0.0

```

The classes listed are those of the positional arguments after
`self`. Any method may be overloaded this way, `__init__` and the
operators included.


### 3. How a call finds its declaration

Only the positional arguments of a call are matched. Keywords play no
part in the choice and pass to the declaration chosen. Two things
follow that are easy to trip over:

```
>>> try:
...   Money(amount=2.5)
... except TypeError:
...   print('no positional arguments: the empty declaration took it')
no positional arguments: the empty declaration took it
>>> class Greeter(BaseObject):
...   @overload(str)
...   def greet(self, name, loud=False):
...     return name.upper() if loud else name
>>> Greeter().greet('ada', loud=True)
'ADA'
>>> from worktoy.waitaminute.dispatch import DispatchException
>>> try:
...   Greeter().greet('ada', True)
... except DispatchException:
...   print('(str, bool) is not declared')
(str, bool) is not declared

```

A call by keyword alone is matched as a call with no positional
arguments, and a defaulted parameter given by position is one more
positional argument to match. Pass optional parameters by keyword.

The positional arguments are matched in steps, and the first step that
finds a declaration decides:

1. Their exact classes.
2. As instances, so a subclass instance matches its base. The class's
   own declarations come before inherited ones, and within one class
   the first declaration written that accepts the arguments wins.
3. A conversion that loses nothing, as `typeCast` of the utilities
   part allows: an `int` for a `float`, `2.0` for an `int`, and a
   class with a `__cast_as__` hook converts there too.
4. The fallback of section 4, if there is one.
5. Otherwise `DispatchException`, a `TypeError`, holding the dispatcher
   as `dispatch`, and the arguments as `posArgs` and `keyArgs`.

Step 2 does not look for the most specific declaration. It takes the
first one written, so write the specific ones first:

```
>>> class Kind(BaseObject):
...   @overload(object)
...   def kind(self, value):
...     return 'object'
...   @overload(int)
...   def kind(self, value):
...     return 'int'
>>> Kind().kind(1)
'int'
>>> Kind().kind(True)
'object'

```

`1` is an `int` exactly and step 1 finds it. `True` is a `bool`, which
no declaration names, so step 2 asks each declaration in order, and
`object` comes first. Reordering the declarations changes the answer,
so their order is part of what the class means.

An argument accepted in step 2 arrives as it was passed, so `True`
reaches an `int` declaration as `True`. One converted in step 3 arrives
converted:

```
>>> class Scale(BaseObject):
...   @overload(float)
...   def ratio(self, value):
...     return value
>>> Scale().ratio(3)
3.0

```


### 4. Several signatures, any order, a tail, a fallback

Decorators stack, so one function may serve several signatures:

```
>>> class Halver(BaseObject):
...   @overload(int)
...   @overload(float)
...   def half(self, value):
...     return value / 2
>>> Halver().half(4), Halver().half(3.0)
(2.0, 1.5)

```

`overload.flex` takes its classes in any order, and the function
receives them in the order declared:

```
>>> class Label(BaseObject):
...   @overload.flex(str, int)
...   def __init__(self, text, size):
...     self.text, self.size = text, size
>>> Label(12, 'Title').text
'Title'

```

`THIS` in a signature stands for the class being declared, which does
not exist yet while its body runs; it is how an operator takes another
instance of its own class:

```
>>> from worktoy.core.sentinels import THIS
>>> class Vector(BaseObject):
...   @overload(float, float)
...   def __init__(self, x, y):
...     self.x, self.y = x, y
...   @overload(THIS)
...   def __add__(self, other):
...     return Vector(self.x + other.x, self.y + other.y)
>>> total = Vector(1.0, 2.0) + Vector(3.0, 4.0)
>>> total.x, total.y
(4.0, 6.0)

```

It is the same marker the core part fills in with the instance
during an access. Where a value is built, it means the instance; in a
signature, where a class is listed, it means the class.

`ARGS[int]`, last in a signature, takes any number of further
integers, none included, converting them as a single entry would. A
signature that matches exactly wins over a tail:

```
>>> from worktoy.core.sentinels import ARGS
>>> class Summary(BaseObject):
...   @overload(str, ARGS[int])
...   def total(self, label, *numbers):
...     return label, sum(numbers)
...   @overload(str)
...   def total(self, label):
...     return label, 'nothing to add'
>>> Summary().total('apples', 1, 2, 3)
('apples', 6)
>>> Summary().total('pears')
('pears', 'nothing to add')

```

A bare `ARGS`, or `*ARGS`, takes any number of anything. Mind that it
takes a mistaken call as well: a declaration of `ARGS` alone catches
every call nothing else accepts, typos included.

`@overload.fallback` declares the function for every call no
declaration accepts, and `@overload.finalize` one that runs after every
call, whichever declaration took it and whether or not it raised. Both
receive the positional arguments and the keywords of the call, and a
subclass inherits both:

```
>>> class Job(BaseObject):
...   @overload(int)
...   def run(self, n):
...     return n * 2
...   @overload.fallback
...   def run(self, *args, **kwargs):
...     return 'cannot run %r' % (args,)
...   @overload.finalize
...   def run(self, *args, **kwargs):
...     print('done')
>>> Job().run(21)
done
42
>>> Job().run('x')
done
"cannot run ('x',)"

```


### 5. Classmethods, staticmethods and subclasses

An overloaded name may be a classmethod, as an alternative constructor
taking several kinds of argument, or a staticmethod. Write
`@classmethod` or `@staticmethod` above `@overload` or below it:

```
>>> class Color(BaseObject):
...   @classmethod
...   @overload(int)
...   def make(cls, code):
...     return 'code %d' % code
...   @overload(str)
...   @classmethod
...   def make(cls, name):
...     return 'named ' + name
>>> Color.make(1), Color.make('red')
('code 1', 'named red')

```

From the update after 1.2.2, one name may hold bound methods,
classmethods and staticmethods together. Through the class the
classmethods and the staticmethods are tried. Through an instance the
bound methods and the classmethods are tried. The overload that matches
receives the instance if it is bound, the class if it is a classmethod,
and neither if it is static:

```
>>> class File(BaseObject):
...   @overload()
...   def exists(self):
...     return 'this file'
...   @staticmethod
...   @overload(str)
...   def exists(name):
...     return 'the file ' + name
>>> File().exists(), File.exists('notes')
('this file', 'the file notes')

```

A staticmethod is not considered through an instance where the name has
a bound method, nor a bound method through the class, so a bound method
and a staticmethod at one name may have the same signature:

```
>>> try:
...   File().exists('notes')
... except DispatchException:
...   print('refused')
refused
>>> class Foo(BaseObject):
...   @staticmethod
...   @overload(int)
...   def bar(value):
...     return 'static'
...   @overload(int)
...   def bar(self, value):
...     return 'bound'
>>> Foo.bar(69), Foo().bar(420)
('static', 'bound')

```

A subclass overloading a name it inherits keeps the inherited
declarations and adds its own, and a declaration of an equal signature
replaces the inherited one:

```
>>> class Shape(BaseObject):
...   @overload(int)
...   def describe(self, n):
...     return 'shape int'
...   @overload(str)
...   def describe(self, s):
...     return 'shape str'
>>> class Square(Shape):
...   @overload(int)
...   def describe(self, n):
...     return 'square int'
>>> Square().describe(1), Square().describe('a')
('square int', 'shape str')

```

A subclass defining the name as a plain method instead hides every
inherited declaration, as a plain definition does.


### 6. Mistakes caught at the declaration

A mistaken declaration fails at its line or as the class is created,
never at the first call:

- `@overload` without parentheses is refused with `BareOverload`.
- An entry that is no class is refused with `TypeException`; `None` is
  refused with a `TypeError`, since a call passing `None` is declared
  with `type(None)`.
- A class `isinstance` cannot check, such as a `Protocol` not marked
  `@runtime_checkable`, is refused with `UncheckableType`.
- One body declaring the same signature twice for a name is refused with
  `DuplicateSignature`.
- An `@overload` in a class not built by `BaseMeta` is refused with a
  `TypeError` as the class is created, which Python wraps in a
  `RuntimeError` before 3.12. Calling what `@overload` returns is
  refused with a `TypeError` too, since it only records a signature.

```
>>> from worktoy.waitaminute.dispatch import DuplicateSignature
>>> try:
...   class Twice(BaseObject):
...     @overload(int)
...     def f(self, x):
...       return 1
...     @overload(int)
...     def f(self, x):
...       return 2
... except DuplicateSignature:
...   print('(int) is declared twice')
(int) is declared twice

```


### 7. The building blocks

The parts of the machinery are public too, for a project building its
own:

- `flexCall(func)` wraps a plain function so it drops surplus positional
  arguments, still refusing a missing one with `TypeError`; it suits a
  callback that some caller hands more arguments than it needs. Keywords
  pass unchanged. `isFlex` tells a wrapper from a plain function.
- `TypeSig` is the classes of a call, in order, equal and hashing alike
  for the same classes; `TypeSig.fromArgs(1, 'a')` is `TypeSig(int,
  str)`. It is not equal to a plain tuple.
- `CallMeMaybe` holds a function and calls it, never binding it as a
  method; `Permuter` calls a function with its arguments put back in the
  order an `Arrangement` restores, which is what `overload.flex` needs.
- `Dispatcher` is what the class holds at an overloaded name:
  `vars(Money)['__init__']` is one, while `Money.__init__` reads as a
  callable.

```
>>> from worktoy.dispatch import flexCall
>>> def onClick(position):
...   return 'clicked at %s' % (position,)
>>> flexCall(onClick)((3, 4), 'left button', 2)
'clicked at (3, 4)'

```

## `worktoy.mcls`

`worktoy.mcls` holds `BaseObject`, the base of a worktoy class, and the
metaclass machinery behind it. Most projects need `BaseObject` and
nothing else from here; the later sections are for giving a class
behaviour of its own and for writing namespace rules of your own.

Contents:

1. `BaseObject`
2. A class that behaves as an object: the class hooks
3. `__class_init__` and `__subclasshook__`
4. Mistakes caught in the class body
5. Combining with another library's metaclass
6. Namespace hooks of your own


### 1. `BaseObject`

Base a class on `BaseObject` and it gets the overloads of the dispatch
part, the checks of section 4 and the class hooks of section 2 at
once. The layers underneath are for those building metaclasses:
`BaseMeta` is the metaclass of `BaseObject` and the one to base a
metaclass of your own on; `AbstractMetaclass` and `AbstractNamespace`
are its plainer parts, and `MetaType` of the core part is the
bottom.

A class with no initializer refuses constructor arguments, as a plain
class does:

```
>>> from worktoy.mcls import BaseObject
>>> class Point(BaseObject):
...   pass
>>> try:
...   Point(1)
... except TypeError:
...   print('Point takes no arguments')
Point takes no arguments

```

A plain base listed after `BaseObject`, as `threading.Thread`, is
initialized as in a plain class, without arguments; a base whose
`__init__` requires arguments goes before `BaseObject`.


### 2. A class that behaves as an object: the class hooks

In plain Python, making a class itself iterable, or giving it a length,
takes a metaclass of its own. A worktoy class defines it in its own
body, with classmethods named after the operation:

```
>>> class Planets(BaseObject):
...   __names__ = ('Mercury', 'Venus', 'Earth')
...   @classmethod
...   def __class_iter__(cls):
...     return iter(cls.__names__)
...   @classmethod
...   def __class_len__(cls):
...     return len(cls.__names__)
>>> list(Planets)
['Mercury', 'Venus', 'Earth']
>>> len(Planets), 'Venus' in Planets
(3, True)

```

The hooks are `__class_call__`, `__class_init__`,
`__class_instancecheck__`, `__class_subclasscheck__`, `__class_str__`,
`__class_repr__`, `__class_iter__`, `__class_next__`, `__class_bool__`,
`__class_contains__`, `__class_len__`, `__class_hash__`,
`__class_setitem__`, `__class_delitem__`, `__class_getattr__` for a
missing attribute, `__class_setattr__` and `__class_delattr__`. A
subscript of a class still goes to Python's own `__class_getitem__`.

- Each hook must be a classmethod; anything else is refused with
  `UnboundClassHook` as the class is created.
- An operation without a hook behaves as for a plain class: `len` and
  `iter` are refused with `TypeError`, `bool` answers from
  `__class_len__` or else `True`, and `in` searches what
  `__class_iter__` yields, one item at a time.
- A hook decides alone. `__class_instancecheck__` answering for `int`
  makes `isinstance(3, Whole)` True and leaves instances of `Whole`
  itself to whatever the hook says; `__class_call__` replaces making an
  instance.
- Hooks are inherited. A subclass sets one to `METACALL`, from the core
  part, to hand the operation back:

```
>>> from worktoy.core.sentinels import METACALL
>>> class Whole(BaseObject):
...   @classmethod
...   def __class_instancecheck__(cls, obj):
...     return isinstance(obj, int)
>>> class Ordinary(Whole):
...   __class_instancecheck__ = METACALL
>>> isinstance(3, Whole), isinstance(3, Ordinary)
(True, False)

```

`METACALL` at `__class_call__` likewise brings back ordinary
construction in a subclass.


### 3. `__class_init__` and `__subclasshook__`

`__class_init__` runs once a class exists, for the class declaring it
and for every subclass, with the name, the bases, the namespace and
the class keywords. A plugin registry is the usual use:

```
>>> registry = []
>>> class Plugin(BaseObject):
...   @classmethod
...   def __class_init__(cls, name, bases, space, **kwargs):
...     registry.append((name, kwargs))
>>> class Exporter(Plugin, format='csv'):
...   pass
>>> registry
[('Plugin', {}), ('Exporter', {'format': 'csv'})]

```

It runs for `Plugin` itself, so a registry wanting subclasses only
skips the base by hand. A class keyword reaches `__class_init__` and the
`__init_subclass__` of a plain base alike.

A base's `__subclasshook__` receives each new subclass as it is
created, and refuses it by raising whatever fits. Each direct base is
asked, its own hook or one it inherits, so a grandchild passes through
its parent's.

Mind the name. `abc` asks the same method inside `issubclass` and
expects `True`, `False` or `NotImplemented`. Under a metaclass combined
with `ABCMeta`, as in section 5, a hook that refuses by raising must
therefore return `NotImplemented` when it lets a class through.


### 4. Mistakes caught in the class body

Python lets some mistakes in a class body pass without a word. In a
worktoy class each fails at its line, with a `SyntaxError`:

- A known misspelling of a dunder, as `__setname__` for `__set_name__`,
  is refused with `QuestionableSyntax`, naming both. It checks a list of
  known misspellings, not every possible one.
- `__del__`, most often written where `__delete__` was meant, is refused
  with `DelException` unless the class statement says `trustMeBro=True`.
  Each class defining `__del__` says so itself.
- `__slots__` is refused with `SlotsRefused`: a worktoy instance always
  keeps a `__dict__`, where its boxes keep their values.
- Rebinding a name Python reserves for the class, as `__qualname__`, is
  refused with `ReservedName`.

```
>>> from worktoy.waitaminute.meta import QuestionableSyntax
>>> try:
...   class Placed(BaseObject):
...     def __setname__(self, owner, name):
...       pass
... except QuestionableSyntax as mistake:
...   print(mistake.derpName, 'should be', mistake.realName)
__setname__ should be __set_name__
>>> class Handle(BaseObject, trustMeBro=True):
...   def __del__(self):
...     pass

```


### 5. Combining with another library's metaclass

A class may have one metaclass, so a base built by another library's
metaclass, such as `abc.ABC`, cannot sit beside `BaseObject`: Python
raises its metaclass conflict. A metaclass based on both builds the
class with the features of both:

```
>>> import abc
>>> from worktoy.mcls import BaseMeta
>>> from worktoy.dispatch import overload
>>> class ABCBaseMeta(BaseMeta, abc.ABCMeta):
...   pass
>>> class Shape(BaseObject, metaclass=ABCBaseMeta):
...   @abc.abstractmethod
...   def area(self):
...     pass
...   @overload(int)
...   def scale(self, factor):
...     return factor
>>> class Square(Shape):
...   def area(self):
...     return 1.0
>>> Square().area(), Square().scale(2)
(1.0, 2)
>>> try:
...   Shape()
... except TypeError:
...   print('Shape is abstract')
Shape is abstract

```

The same pattern serves other libraries' metaclasses.


### 6. Namespace hooks of your own

A team rule for class bodies, such as "no single-underscore names",
can fail at the line breaking it. It takes three small classes: a hook,
a namespace holding it, and a metaclass returning that namespace.

```
>>> from worktoy.mcls import BaseSpace
>>> from worktoy.mcls.space_hooks import AbstractSpaceHook
>>> class NoSingleUnderscore(AbstractSpaceHook):
...   def setItemPhase(self, key, value, old=None):
...     if key.startswith('_') and not key.startswith('__'):
...       raise NameError('%s.%s' % (self.space.getClassName(), key))
...     return False
>>> class TeamSpace(BaseSpace):
...   noSingleUnderscore = NoSingleUnderscore()
>>> class TeamMeta(BaseMeta):
...   @classmethod
...   def __prepare__(mcls, name, bases, **kwargs):
...     return TeamSpace(mcls, name, bases, **kwargs)
>>> class TeamObject(BaseObject, metaclass=TeamMeta):
...   pass
>>> try:
...   class Report(TeamObject):
...     _cache = None
... except NameError as error:
...   print('refused', error)
refused Report._cache

```

`setItemPhase(key, value, old)` runs before each binding of a class
body. Raising refuses the binding at its line; returning `True` claims
it, and the class does not receive the name; returning `False` leaves it
alone. Inside a phase `self.space` is the namespace of the class
statement in progress. The other phases are `preparePhase`,
`getItemPhase`, `delItemPhase`, `preCompilePhase`, `postCompilePhase`
and `newClassPhase`.

The hook screens the class declaring the metaclass as well as its
subclasses, and worktoy's own checks of section 4 keep running beside
it. One hook object serves every class statement of its namespace, so
it keeps what it learns on `self.space`, never on itself.

## `worktoy.keenum`

`worktoy.keenum` holds worktoy's enumerations: `KeeNum`, a set of named
members with typed values, and `KeeFlags`, a set of flags with every
combination as a member. Both work with the boxes of the desc part,
which turn a name or a value assigned to a field into the member.

Three things are deprecated since 1.2.0: `index` on a member, `KeeBox`
and `KeeFlag`. Each works as it did through the 1.x releases, gives a
deprecation notice where it is used, and is no longer promised from the
next major update. Section 8 lists them with the promises 1.2.0 took
back.

Contents:

1. Declaring an enumeration
2. Finding a member
3. The enumeration and its members
4. Extending an enumeration
5. Enumerations in boxes, and `KeeBox`
6. Flags: `KeeFlags`
7. A metaclass of your own
8. Deprecated and taken back in 1.2.0


### 1. Declaring an enumeration

```
>>> from worktoy.keenum import KeeNum, Kee
>>> class WeekDay(KeeNum):
...   MONDAY = Kee[str]('Mandag')
...   TUESDAY = Kee[str]('Tirsdag')
...   SATURDAY = Kee[str]('Lordag')
...   def isWeekend(self):
...     return self is WeekDay.SATURDAY
>>> WeekDay.MONDAY.value, WeekDay.MONDAY.index
('Mandag', 0)
>>> WeekDay.SATURDAY.isWeekend()
True

```

- `Kee[str]('Mandag')` builds the value by calling the type, so
  `Kee[int]()` holds `0` and `Kee[int]('3')` holds `3`.
- Every value has the type of the first member; a second type is refused
  with `KeeTypeException`.
- Member names are upper case; another name is refused with
  `KeeCaseException`, unless the class statement says
  `strictCase=False`, shown below.
- Values need not be unique. Anything in the body that is no `Kee`,
  a method or a plain value, stays an ordinary class attribute, and a
  method is a method of every member.
- A name declared twice is refused with `KeeDuplicate`, and a plain
  value at a member's name `KeeMemberNameError`.

From 1.2.2, a class whose members are named in another case says so on
its class statement, with the class keyword `strictCase=False`:

```
>>> class Header(KeeNum, strictCase=False):
...   Accept = Kee[str]('Accept')
...   contentType = Kee[str]('Content-Type')
>>> [header.name for header in Header]
['Accept', 'contentType']
>>> Header.contentType.value
'Content-Type'

```

`strictCase` takes a `bool`, and `strictCase=True` is the rule as it
stands without the keyword. Any other value is refused with
`TypeException`, whether or not the body declares a member:

```
>>> from worktoy.waitaminute import TypeException
>>> try:
...   class Vague(KeeNum, strictCase='no'):
...     pass
... except TypeException as refusal:
...   print(refusal.varName)
strictCase

```

Whatever their case, two members may not differ by the case of their
names alone, since a lookup by name ignores case and could not tell them
apart. The second is refused with `KeeDuplicate`, as a name declared
twice does:

```
>>> from worktoy.waitaminute.keenum import KeeDuplicate
>>> try:
...   class Power(KeeNum, strictCase=False):
...     mW = Kee[float](0.001)
...     MW = Kee[float](1000000.0)
... except KeeDuplicate as duplicate:
...   print(duplicate.clsName, duplicate.name)
Power MW

```

The upper-case rule is also what keeps a member apart from the other
names of its class. A class that gives the rule up may therefore not
name a member as something a base or the metaclass holds already, as
`members`, `valueType` or a method of a base. Such a member is refused
with `ReservedName`:

```
>>> from worktoy.waitaminute.meta import ReservedName
>>> try:
...   class Role(KeeNum, strictCase=False):
...     guests = Kee[int](1)
...     members = Kee[int](2)
... except ReservedName as reserved:
...   print(reserved.resName)
members

```

A subclass takes the choice of its base, and says `strictCase=True` to
take the upper-case rule back for the members it adds:

```
>>> class Metric(KeeNum, strictCase=False):
...   mm = Kee[float](0.001)
>>> class Imperial(Metric):
...   inch = Kee[float](0.0254)
>>> [unit.name for unit in Imperial]
['mm', 'inch']

```

Coming from Python's `enum`, mind the differences: a lookup by call
takes names as well as values, a subscript takes positions, a miss is
refused with `KeeResolveError`, which is no `ValueError`, and an
enumeration may be extended by a subclass.


### 2. Finding a member

`WeekDay(x)` and `WeekDay[x]` look for a member in this order:

1. `x` is already a member;
2. a name, in any case;
3. the answer of `__class_resolve__`, a classmethod of your own;
4. for `WeekDay[x]` only, a position, as list indexing, `WeekDay[-1]`
   the last;
5. a value, the first member holding it.

```
>>> class Rank(KeeNum):
...   LOW = Kee[int](2)
...   MID = Kee[int](5)
...   HIGH = Kee[int](9)
>>> Rank('mid').name, Rank(9).name
('MID', 'HIGH')
>>> Rank(2).name, Rank[2].name
('LOW', 'HIGH')

```

`Rank(2)` is a value and `Rank[2]` a position, so for an enumeration of
integers the two disagree, and `Rank[5]` is a value only while there are
fewer than six members. Use the call for values and the subscript for
positions, and give an integer enumeration a `__class_resolve__` to
settle what its integers mean:

```
>>> class Level(KeeNum):
...   LOW = Kee[int](1)
...   HIGH = Kee[int](10)
...   @classmethod
...   def __class_resolve__(cls, identifier):
...     if identifier == 'max':
...       return cls.HIGH
...     return NotImplemented
>>> Level('max').name, Level('low').name
('HIGH', 'LOW')

```

A name wins over a value, and a value shared by two members gives the
first. A `bool` is no position and no value of an integer enumeration. A
miss is refused with `KeeResolveError`, with the enumeration as `keeNum`
and the identifier as `identifier`:

```
>>> from worktoy.waitaminute.keenum import KeeResolveError
>>> try:
...   Rank('top')
... except KeeResolveError as miss:
...   print(miss.identifier)
top

```

A call takes exactly one argument. `Rank.fromValue(9)` looks up a value
and nothing else, refusing a value of another type with `TypeException`.
And `Rank.low` is `Rank.LOW`: attribute access takes a name in any case.


### 3. The enumeration and its members

An enumeration iterates its members in order, counts them with `len`,
and holds them in `members`. A member has `name`, `value` and
`valueType`, and is an instance of its enumeration. It has `index` too,
which is deprecated:

```
>>> [day.name for day in WeekDay]
['MONDAY', 'TUESDAY', 'SATURDAY']
>>> type(WeekDay.MONDAY) is WeekDay, isinstance(WeekDay.MONDAY, WeekDay)
(True, True)
>>> WeekDay.MONDAY in WeekDay, 'MONDAY' in WeekDay
(True, False)

```

- A member equals itself alone, not its name or value.
- It hashes when its value hashes, so a member with a list value is no
  dict key.
- A copy, a deep copy and a pickle give the member itself. A pickle
  holds the member's name, so renaming a member breaks old pickles.
- Members are frozen. Setting or deleting an attribute of one, or
  rebinding a member's name on the class, is refused with
  `KeeWriteOnceError`.
- There is no ordering of members.
- How a member reads as text is not promised: use `name` or `value`.


### 4. Extending an enumeration

A subclass holds the members of its base, the same objects, and adds
its own after them:

```
>>> class LongWeek(WeekDay):
...   SUNDAY = Kee[str]('Sondag')
>>> [day.name for day in LongWeek]
['MONDAY', 'TUESDAY', 'SATURDAY', 'SUNDAY']
>>> LongWeek.MONDAY is WeekDay.MONDAY
True
>>> LongWeek.SUNDAY in WeekDay, isinstance(LongWeek.SUNDAY, WeekDay)
(True, True)

```

So `in` and `isinstance` admit the members of subclasses too, while
iterating `WeekDay` gives its own. Code that must know every member it
can receive iterates the enumeration it was written for.


### 5. Enumerations in boxes, and `KeeBox`

An `AttriBox` over an enumeration takes whatever a call takes, so a
name or a value assigned to the field becomes the member:

```
>>> from worktoy.mcls import BaseObject
>>> from worktoy.desc import AttriBox
>>> class Calendar(BaseObject):
...   day = AttriBox[WeekDay](WeekDay.MONDAY)
>>> calendar = Calendar()
>>> calendar.day = 'tuesday'
>>> calendar.day is WeekDay.TUESDAY
True
>>> calendar.day = 'Lordag'
>>> calendar.day is WeekDay.SATURDAY
True

```

Anything the enumeration cannot resolve is refused with
`TypeException`. `typeCast` converts the same way, which is why a name
becomes a member while `typeCast` never parses a number: resolving a
name is the enumeration's own rule.

`KeeBox` is deprecated since 1.2.0; an `AttriBox` over the enumeration,
as above, declares the same field. A `KeeBox` is a box whose
parentheses take more: the member, a name, a
position, a value, or the arguments the value is built from. Over flags
it takes several names. The one place they part ways is a lone
integer:

```
>>> from worktoy.keenum import KeeBox
>>> class Board(BaseObject):
...   boxed = KeeBox[Rank](2)
...   plain = AttriBox[Rank](2)
>>> board = Board()
>>> board.boxed.name, board.plain.name
('HIGH', 'LOW')

```

The parentheses of a `KeeBox` read `2` as a position; those of an
`AttriBox` call `Rank(2)`, a value. Assignment to either converts as the
enumeration does. A `KeeBox` default no member matches is refused with
`KeeBoxValueError` at the first read.


### 6. Flags: `KeeFlags`

```
>>> from worktoy.keenum import KeeFlags, KeeFlag
>>> class FileAccess(KeeFlags):
...   READ = KeeFlag()
...   WRITE = KeeFlag()
...   EXECUTE = KeeFlag()
>>> len(FileAccess)
8
>>> (FileAccess.READ | FileAccess.WRITE) is FileAccess.READ_WRITE
True
>>> FileAccess('execute_read').names == {'READ', 'EXECUTE'}
True

```

`KeeFlag` is deprecated since 1.2.0. It is still how this part
declares a flag, since what is written in its place is not promised
yet.

A flags class holds every combination of its flags as a member, built
as the class is created: 2 ** N members for N flags, `NULL` the one with
none. That costs memory and time at the class statement: the
`KeeFlags` docstring measured 16 flags at about
a third of a second on one machine, and the cost quadruples for every
two flags added.

- A member's `index` is its bit mask, which is also its position among
  the members. Flag `i` is bit `i` in the order declared; bits cannot be
  chosen. `index` is deprecated.
- A member's `name` joins its flag names by `_` in declaration order, so
  a flag name may not contain `_` itself, nor be `NULL`; either is
  refused with `KeeFlagNameError`. A body name a member takes is refused
  with `KeeMemberNameError`, so there are no aliases such as `ALL`.
- `names` is a frozenset of the flag names, `highs` and `lows` the flags
  on and off, and iterating a member gives its flags on.
- A call or subscript takes a member, a name in any case and flag order,
  several names or a tuple of them, an index or a value; `FileAccess()`
  is `NULL`.
- `|`, `&`, `^` and `~` give members; `NULL` is false, every other
  member true.
- A subclass overrides `_getValue` to give members values of its own.
  What `value` is without that is not promised.
- `~` of `NULL` is not promised.

A subclass adds flags. Members of the two with the same flags are equal
and hash alike, and combining them gives the member of the class that
holds every flag:

```
>>> class Extended(FileAccess):
...   APPEND = KeeFlag()
>>> Extended.READ == FileAccess.READ
True
>>> (FileAccess.READ | Extended.APPEND) is Extended.READ_APPEND
True

```


### 7. A metaclass of your own

`KeeNum` is built by `KeeMeta`. A project extending the metaclass bases
its enumerations on the root its own metaclass builds, `keeNum`, so the
customizations reach them:

```
>>> from worktoy.keenum import KeeMeta
>>> class FontMeta(KeeMeta):
...   pass
>>> class FontFamily(FontMeta.keeNum):
...   ARIAL = Kee[int](1)
...   TIMES = Kee[int](2)
>>> isinstance(FontFamily, FontMeta)
True

```

Basing `FontFamily` on `KeeNum` instead would build it with plain
`KeeMeta`, silently without the customizations.

`AccessNum`, last, is a small enumeration worktoy uses itself, of the
descriptor methods: `GET`, `SET` and `DELETE`, holding `'__get__'`,
`'__set__'` and `'__delete__'`.


### 8. Deprecated and taken back in 1.2.0

Deprecated: each works as it did through 1.x, gives a deprecation
notice, a `FutureWarning`, at the line that uses it, and is no longer
promised from the next major update.

- `index` on a member, of `KeeNum` and of `KeeFlags`. An index is a
  position in a class, and a member is one object shared by its
  enumeration and every subclass of it, so it can carry one index where
  two classes may hold it at two positions. The class still answers a
  position: `WeekDay[0]`.
- `KeeBox`. An `AttriBox` over the enumeration declares the same field,
  and reads a lone number in its parentheses the way assignment reads
  it.
- `KeeFlag`. What is written in its place is not promised yet.

Taken back: promised in 1.1.0, found to contradict another promise, and
no longer true in 1.2.0. Nothing is promised in their place.

- The default `value` of a flags member is its bit mask. Equal members
  of related flags classes held different values.
- A flags subclass holds members of its own for the flags of its base.
  The members are still equal and hash alike.
- `~` of `NULL` gives the member with every flag. `NULL` stands for no
  flag in every flags class alike, so it cannot say whose flags it
  lacks.
- An enumeration iterates in index order. The order of a class cannot
  be read off a number each member carries.

## `worktoy.ezdata`

`worktoy.ezdata` holds `EZData`, worktoy's dataclass. Declare the fields
in the class body and the class receives its constructor, equality,
iteration and the rest. Unlike a standard dataclass, every value is
held to its type, as the constructor runs and at every assignment
after.

Contents:

1. Declaring a dataclass
2. What counts as a field
3. Making an instance
4. Using an instance
5. Frozen, ordered, keyword-only
6. Inheritance
7. Mistakes caught as the class is created


### 1. Declaring a dataclass

```
>>> from worktoy.ezdata import EZData, EZField, fields
>>> class Point(EZData):
...   x = 0.0
...   y = 0.0
>>> point = Point(1, 2)
>>> point.x, point.y
(1.0, 2.0)
>>> point.x = 5
>>> point.x
5.0

```

A field is a value the body binds: a plain value, whose type becomes
the field's type, or `EZField[T](...)`, which names the type and the
arguments of the default. The fields come in the order written, and
`fields(Point)` lists them.

Mind the first difference from `dataclasses`, `attrs` and `pydantic`:
an annotation alone, `label: str`, declares nothing. The fields are
what the body binds, so write `label = ''`, or `label =
EZField[str]()`.


### 2. What counts as a field

- Methods, properties and classmethods are not fields; they stay what
  they are.
- Every plain value is a field, a constant included. Keep a constant on
  a plain base class instead:

```
>>> class Limits:
...   MAX = 100
>>> class Box(EZData, Limits):
...   size = 1
>>> [f.fieldName for f in fields(Box)], Box.MAX
(['size'], 100)

```

- A field takes the type of its value exactly: `x = 0` declares an
  `int` field, which then refuses `0.5`. Write `x = 0.0` for a float.
- A bare `None` has no type, and is refused with
  `IncompleteFieldException`. There is no optional field: every field
  holds a value of its type.
- `EZField[THIS]`, a field of the class's own type, is refused with
  `TypeError`, since no value of the class exists while its body runs.

A default is built anew for each instance, so no two instances share a
mutable default. A lone value that already is of the field's type is
copied. A lone value of another type converts as `typeCast` converts
when the field's type is a number or a text, a subclass of one, or a
class with a `__cast_as__` hook, so `EZField[int]('7')` is refused. In
every other case the type is called with the arguments, so
`EZField[list]('abc')` holds `['a', 'b', 'c']`.


### 3. Making an instance

The constructor takes the fields by position, in order, or by keyword,
each left out taking its default. Each value converts as `typeCast`
converts it, or is refused with `TypeException`:

```
>>> Point(y=3).asTuple()
(0.0, 3.0)
>>> from worktoy.waitaminute import TypeException
>>> try:
...   Point('1.5')
... except TypeException:
...   print('a string is no number')
a string is no number

```

Too many positional arguments are refused with
`ExtraPositionalException`, an unknown keyword `ExtraKeywordException`,
and a field given both ways `RepeatedFieldException`, all `TypeError`s.

A body may define `__post_init__(self)`, which runs after the fields
are set, for checks and derived values:

```
>>> class Account(EZData):
...   balance = 0.0
...   def __post_init__(self):
...     if self.balance < 0:
...       raise ValueError('a balance cannot be negative')
>>> try:
...   Account(-5)
... except ValueError as error:
...   print(error)
a balance cannot be negative

```


### 4. Using an instance

```
>>> point = Point(1, 2)
>>> x, y = point
>>> len(point), point.asDict()
(2, {'x': 1.0, 'y': 2.0})
>>> point.replace(y=5).asTuple()
(1.0, 5.0)
>>> point == Point(1, 2), point == (1.0, 2.0)
(True, False)

```

- An instance iterates and unpacks as its values, and `len` counts its
  fields, so an instance without fields is false.
- `asDict` and `asTuple` give the values. They are shallow: a nested
  `EZData` stays an instance.
- `replace` gives a new instance with some values changed, running
  `__post_init__` again.
- `__match_args__` lists the fields, and is empty for a keyword-only
  class, so `match` works on Python 3.10 and later.
- Two instances are equal when their values are and they are of one
  lineage, holding the same fields in the same order: a class and its
  subclasses, a frozen subclass included. An instance of a sibling
  class, or a tuple, is never equal.
- An instance is not hashable unless its class is frozen.
- Assigning a field converts as the constructor does. Deleting a field
  is refused with `AttributeError`.
- Any other attribute may be set and deleted freely, and stays out of
  the values and equality. So a typo, `point.xx = 5`, creates an
  attribute rather than failing.

The class writes `__repr__` and `__str__` for you, but their text is not
promised; a body may write its own, as it may `asDict`, `asTuple` and
`replace`.


### 5. Frozen, ordered, keyword-only

Three class keywords change a dataclass, each under several names:

- `frozen=True`, or `immutable` or `hashable`: every assignment and
  deletion is refused with `AttributeError`, and instances hash, equal
  ones alike. `__post_init__` cannot assign to a frozen instance either.
- `ordered=True`, or `order`, `sortable` or `comparable`: instances
  compare field by field, in order.
- `kwOnly=True`, or `keywordOnly` or `kw_only`: the constructor takes
  keywords only, and refuses a positional argument with
  `KwargsOnlyException`.

```
>>> class Version(EZData, ordered=True):
...   major = 0
...   minor = 0
>>> Version(1, 9) < Version(2, 0)
True
>>> class Port(EZData, frozen=True):
...   number = 80
>>> try:
...   Port(8080).number = 1
... except AttributeError:
...   print('frozen')
frozen

```

The class answers `isFrozen`, `isOrdered` and `kwOnly`. A subclass of an
ordered class is ordered. A subclass of a frozen class must say
`frozen=True` itself, or the class statement is refused with
`TypeError`. And a misspelled keyword, as `frozn=True`, is dropped
without a word, as every class keyword no class takes is in worktoy.


### 6. Inheritance

A subclass adds its fields after those it inherits, and may give an
inherited field a new default:

```
>>> class Point3D(Point):
...   x = 1.0
...   z = 0.0
>>> [f.fieldName for f in fields(Point3D)], Point3D().asTuple()
(['x', 'y', 'z'], (1.0, 0.0, 0.0))

```

Several `EZData` classes may be combined as bases, and the result holds
the fields of all of them.


### 7. Mistakes caught as the class is created

- `EZField(1)` without a type, and `EZField[int]` without parentheses,
  are refused with `IncompleteFieldException`.
- A field bound twice is refused with `DuplicateError`.
- A field at a name kept for a method, as `replace`, `asDict` or
  `__post_init__`, is refused with `ReservedFieldError`.
- A body defining a method `EZData` writes itself, as `__init__`,
  `__eq__` or `__setattr__`, is refused with `ReservedMethodError`, and
  one binding an attribute it sets itself, as `__kw_only__`,
  `ReservedAttributeError`.

All of these are `SyntaxError`s, as the exceptions part explains.
`EZMeta`, `EZSpace`, `EZHook` and `EZStore` are the machinery behind
the class, public for a project building a dataclass base of its own.

## `worktoy.core`

`worktoy.core` is the layer the rest of worktoy stands on. Most
projects never import from it: they subclass `BaseObject` and declare
their attributes with `AttriBox`, which later parts describe. You
reach into `core` when you build something of your own, of the kinds
worktoy itself is built from:

- a descriptor, on `Object`;
- a marker no real value can be mistaken for, on `Sentinel`;
- a signal that steers a protocol, on `ControlFlow`;
- a metaclass, on `MetaType`.

Contents:

1. Writing a descriptor on `Object`
2. Hooks around every access
3. Arguments and placeholders: `THIS`, `OWNER`, `DESC`
4. The access in progress
5. An `Object` as a class value
6. Options under several names: `parseKwargs`
7. Sentinels
8. Control-flow signals
9. Metaclasses: `MetaType`


### 1. Writing a descriptor on `Object`

A descriptor is an object in a class body that decides what reading,
writing and deleting an attribute does on the instances; `property` is
the best known one. In plain Python a descriptor defines `__get__`,
`__set__` and `__delete__`. On `Object` you define three methods of
your own instead, and leave those three to `Object`, which uses them to
keep track of the access, run the hooks of the next section and handle
deletion:

```
>>> from worktoy.core import Object
>>> from worktoy.core.sentinels import DELETED
>>> class Counted(Object):
...   def __instance_get__(self, instance, owner, **kwargs):
...     return instance.__dict__.get('_count', 0)
...   def __instance_set__(self, instance, value, **kwargs):
...     instance.__dict__['_count'] = value
...   def __instance_delete__(self, instance, old=None, **kwargs):
...     instance.__dict__['_count'] = DELETED
>>> class Visit:
...   count = Counted()
>>> visit = Visit()
>>> visit.count
0
>>> visit.count = 3
>>> visit.count
3
>>> del visit.count
>>> hasattr(visit, 'count')
False

```

A few things to know before you write your own:

- Any class can hold one. `Visit` is a plain class; neither `MetaType`
  nor `BaseObject` is needed.
- Where the values live is yours to decide. `Counted` keeps them in the
  instance dictionary. The boxes of a later part, `AttriBox` first,
  do that bookkeeping for you.
- Deleting is yours too. `__instance_delete__` stores `DELETED` where
  the getter reads, and when the getter returns `DELETED`, `Object`
  turns the read into `MissingVariable`, an `AttributeError`. So
  `hasattr` answers False, and a second `del` raises as well.
- Always accept `**kwargs`. worktoy hands keywords to these methods,
  `_deleting` among them, as section 2 shows.
- `instance` arrives as an argument, and is also `self.instance` while
  the access runs, so a helper method you call from inside can ask for
  it instead of being handed it. `self.owner` is the class; during a
  write or a deletion that is the class of the instance. Both work
  through `ContextInstance` and `ContextOwner`, which you never need
  yourself.
- Read through the class, the attribute is the descriptor itself:
  `Visit.count` is the `Counted` object.
- A method you leave out keeps the default of `Object`: a read gives the
  descriptor itself, a write is refused with `ReadOnlyError` and a
  deletion is refused with `ProtectedError`. Section 5 shows why that is
  useful.


### 2. Hooks around every access

Around each access, `Object` calls hooks you may define:

- `hookPreGet(instance)` before a read, and `hookOnGet(instance,
  value)` after it, with the value about to be returned;
- `hookPreSet(instance, value)` before a write, with the value
  assigned, and `hookOnSet(instance, value)` after it;
- `hookPreDelete(instance)` and `hookOnDelete(instance)` around a
  deletion;
- `hookSetName(owner, name)` when the descriptor is placed in a class
  body.

A thermostat that refuses frost, skips a setting it already has, and
reports every change:

```
>>> from worktoy.core.control_flow import SkipSet
>>> class Setting(Object):
...   def __instance_get__(self, instance, owner, **kwargs):
...     return instance.__dict__.get('_target', 20)
...   def __instance_set__(self, instance, value, **kwargs):
...     instance.__dict__['_target'] = value
...   def hookPreSet(self, instance, value, **kwargs):
...     if value < 5:
...       raise ValueError('too cold')
...     if value == instance.__dict__.get('_target', 20):
...       raise SkipSet
...   def hookOnSet(self, instance, value, **kwargs):
...     print('target set to', value)
>>> class Thermostat:
...   target = Setting()
>>> room = Thermostat()
>>> room.target = 22
target set to 22
>>> room.target = 22
>>> try:
...   room.target = 2
... except ValueError as error:
...   print(error)
too cold
>>> room.target
22

```

- `hookPreSet` refuses a write by raising, and skips one silently by
  raising `SkipSet`: nothing is stored and `hookOnSet` is not called.
  `SkipSet` works there and nowhere else; any other exception, a
  signal of your own included, reaches the line that assigned. To store
  something other than what was assigned, convert it in
  `__instance_set__` and return what you stored.
- `hookOnSet` receives what `__instance_set__` returned, or the value
  assigned when it returned `None`. It runs after the value is stored,
  so raising there refuses nothing.
- A deletion first reads the old value through your getter, with
  `_deleting=True` among the keywords and without the read hooks, so
  side effects of your getter happen on `del` too, and a getter that
  builds defaults can see that it should not. Then come
  `hookPreDelete`, `__instance_delete__`, which receives the old value,
  and `hookOnDelete`.
- `hookSetName` runs when Python places the descriptor, in a class
  body. Python does not place an attribute set on a class afterwards.
- Each hook is one method of your class. For several callbacks on one
  field, the boxes of a later part take them as decorators.

The reads are guarded against loops, as section 4 shows; the writes
are not, so a `hookOnSet` assigning its own field runs again and again.


### 3. Arguments and placeholders: `THIS`, `OWNER`, `DESC`

An `Object` keeps the arguments it was created with, and
`getPosArgs()` and `getKeyArgs()` give them back. An argument is
written in the class body, where no instance exists yet, so three
placeholders stand in: during an access, an argument that is `THIS`
becomes the instance, `OWNER` the class, and `DESC` the descriptor
itself.

```
>>> from worktoy.core.sentinels import THIS
>>> class Greeting(Object):
...   def __instance_get__(self, instance, owner, **kwargs):
...     word, person = self.getPosArgs()
...     return '%s, %s' % (word, person.name)
>>> class Person:
...   greeting = Greeting('Hello', THIS)
...   def __init__(self, name):
...     self.name = name
>>> Person('Ada').greeting
'Hello, Ada'

```

This is what lets `AttriBox[...](THIS)` build a value from the instance
it belongs to.

- Only an argument that is the placeholder itself is replaced, not one
  inside a list or a dict. Build the container in `__instance_get__`
  from the filled-in arguments.
- Outside an access there is no instance, so `THIS` and `OWNER` stay
  themselves. `DESC` always becomes the descriptor, which always
  exists. Read the arguments during an access.
- `Object` takes any arguments and checks none of them: what they mean
  is up to your class. `hasSentinelArgs()` tells whether any is a
  placeholder.

`getPrivateName()` suggests a private name to store a field under:
`'__foo_bar__'` for a field named `fooBar`. The mapping is not one to
one: `foo_bar` gives `'__foo_bar__'` as well, and a field named `dict`
gives the `'__dict__'` Python uses itself. A descriptor no class holds
has no field name, and `getPrivateName()` is refused with
`MissingVariable`.


### 4. The access in progress

`self.instance` and `self.owner` answer during an access, and only then.
Asked outside one, a descriptor placed in a class is refused with
`WithoutException`, short for "without an access in progress", a
`RuntimeError` and deliberately no `AttributeError`, since asking is a
mistake in the code; so `hasattr` raises it too. An `Object` no class
holds simply has no such attribute.

Code driving a descriptor by hand opens an access with
`createContext(instance, owner)` and closes it with `exitContext()`.
Accesses nest, and closing one brings back the one opened before:

```
>>> class Plain(Object):
...   pass
>>> class Holder:
...   thing = Plain()
>>> desc, holder = vars(Holder)['thing'], Holder()
>>> _ = desc.createContext(holder, Holder)
>>> try:
...   print(desc.instance is holder)
... finally:
...   _ = desc.exitContext()
True

```

Pair them in `try` and `finally` as shown. Closing with nothing open is
refused with `WithoutException`.

Each thread sees only its own accesses, so two threads reading through
one descriptor at the same moment each get their own instance. An
access lasts exactly one call, so asyncio tasks do not see each
other's either.

A read hook that reads its own field for the same instance would run
itself again forever. It is refused at that line with `RecursiveRead`,
a `RecursionError` that names the hook in `phase`, `'preGet'` or
`'onGet'`:

```
>>> from worktoy.waitaminute.desc import RecursiveRead
>>> class Gauge(Object):
...   def __instance_get__(self, instance, owner, **kwargs):
...     return instance._level
...   def hookOnGet(self, instance, value, **kwargs):
...     if instance.level != value:
...       print('changed')
>>> class Tank:
...   level = Gauge()
...   def __init__(self, level):
...     self._level = level
>>> try:
...   Tank(3).level
... except RecursiveRead as error:
...   print('refused during', error.phase)
refused during onGet

```

Reading the same field of another instance is allowed. Only the hooks
are guarded: a getter reading its own field ends in Python's own
`RecursionError`.


### 5. An `Object` as a class value

An `Object` that defines none of the three access methods is a value in
the class body, shared by every instance. Reading it through an
instance gives the object itself, and an instance may not replace or
delete it: worktoy holds its own objects in a class body to that rule.

```
>>> class Theme(Object):
...   pass
>>> class Config:
...   theme = Theme('dark')
>>> config = Config()
>>> config.theme is Config.theme
True
>>> config.theme.getPosArgs()
('dark',)
>>> from worktoy.waitaminute.desc import ReadOnlyError
>>> try:
...   config.theme = 'light'
... except ReadOnlyError as error:
...   print(error.newVal, 'refused')
light refused

```

`Object` is also the base of the ordinary objects of worktoy,
`BaseObject` among them. A base listed after an `Object` class still
has its `__init__` run, as `threading.Thread` needs, but without
arguments, so a base that requires some refuses with its own
`TypeError`; list such a base first.

An `Object` already uses these names, so a subclass should not take
them for something else: `instance`, `owner`, `directory`,
`getPosArgs`, `getKeyArgs`, `hasSentinelArgs`, `getFieldOwner`,
`getFieldName`, `getPrivateName`, `createContext`, `exitContext`,
`hasContext`, `getContextInstance`, `getContextOwner`,
`getContextualSentinels`, `filterSentinels`, `parseKwargs`, and the
hooks of section 2. `directory` is the folder of the file that defines
the class, as `Directory` in the utilities part gives it.


### 6. Options under several names: `parseKwargs`

An option sometimes goes by several names, as `readOnly` or `frozen`.
`Object.parseKwargs` reads it once: give it the names and the accepted
types, in any order, and the keywords:

```
>>> def connect(**options):
...   return Object.parseKwargs('readOnly', 'frozen', bool, **options)
>>> connect(frozen=True, timeout=5)
(True, {'timeout': 5})
>>> connect(timeout=5)
(None, {'timeout': 5})

```

It is a classmethod, so any function may use it. The first name present
wins, in the order you gave the names, and a second synonym stays among
the other keywords. A `float` accepts an `int`, a `complex` accepts
both, and a `bool` passes as an `int`; the value comes back as given,
not converted. A value of no accepted type is refused with
`TypeException`.


### 7. Sentinels

A sentinel is a marker no real value can be mistaken for: "not given
yet", "deleted", "the class being defined". A project declares one with
a class statement, and the class itself is the marker. It reads well in
a traceback, it is equal to itself alone, and it cannot be
instantiated:

```
>>> from worktoy.core.sentinels import Sentinel, SentinelMeta
>>> class PENDING(Sentinel):
...   """The result has not arrived yet."""
>>> results = {'job1': PENDING}
>>> results['job1'] is PENDING
True
>>> from worktoy.waitaminute.meta import IllegalInstantiation
>>> try:
...   PENDING()
... except IllegalInstantiation:
...   print('a sentinel is never instantiated')
a sentinel is never instantiated

```

A name stands for one sentinel in the whole process, so a second class
statement at a name already taken is refused with `DuplicateSentinel`:

```
>>> from worktoy.waitaminute.meta import DuplicateSentinel
>>> try:
...   class PENDING(Sentinel):
...     pass
... except DuplicateSentinel as error:
...   print(error.sentinelName, 'is taken')
PENDING is taken

```

That holds wherever the second statement is: in another module, in
another library, in a Jupyter cell run again, or in a module reloaded.
Declare each sentinel once, in one module the rest import, and give it
a distinctive name.

To give sentinels behaviour, base a metaclass of your own on
`SentinelMeta`. Its sentinels share the one registry of names:

```
>>> class LightMeta(SentinelMeta):
...   def describe(cls):
...     return 'the light is %s' % cls.__name__.split('_')[-1].lower()
>>> class LIGHT_ON(metaclass=LightMeta):
...   pass
>>> LIGHT_ON.describe()
'the light is on'
>>> isinstance(LIGHT_ON, SentinelMeta)
True

```

`isinstance(x, SentinelMeta)` is the test that works for every
sentinel, those of a family included.

worktoy declares a few of its own. `DELETED` marks a deleted value, as
in section 1, and `THIS`, `OWNER` and `DESC` are the placeholders of
section 3. `METACALL` belongs to the metaclass part. `ARGS` belongs
to the overload part: unlike the others it is subscripted,
`ARGS[int]`, to an instance carrying its inner type, and instances of
one inner type are equal and hash alike.


### 8. Control-flow signals

Some exceptions steer a protocol instead of reporting a failure, as
`StopIteration` tells a loop to stop. worktoy calls them control-flow
signals. Each is a subclass of `ControlFlow`, so `except ControlFlow`
catches them all, and none is a worktoy error. `SkipSet`, from section
2, is the one worktoy raises, and worktoy catches it only around
`hookPreSet`.

A project declares a signal of its own with a class statement. A
signal is used by its type alone and carries nothing, so its body may
hold a docstring and, if you like, `__str__` and `__repr__`, and
nothing else:

```
>>> from worktoy.core.control_flow import ControlFlow
>>> class Retry(ControlFlow):
...   """The step should run again."""
>>> try:
...   raise Retry
... except ControlFlow as signal:
...   print('caught', type(signal).__name__)
caught Retry
>>> from worktoy.waitaminute.meta import ControlClassError
>>> try:
...   class Wait(ControlFlow):
...     seconds = 3
... except ControlClassError as error:
...   print('refused:', error.badKey)
refused: seconds

```

When the reason matters, raise a real exception instead. Mind that a
signal is an `Exception`, so an `except Exception` between the raise
and the place meant to catch it catches the signal as well.

The signals lived in `worktoy.waitaminute.control_flow` before. They
import from there as the same objects throughout the 1.x releases. That
path is deprecated since 1.2.0: each name read from it gives a
deprecation notice, a `FutureWarning`.
`MetaFlow` and `ControlSpace`, the metaclass and namespace behind the
signals, are public, but a project declaring signals never needs them.


### 9. Metaclasses: `MetaType`

Every worktoy class and metaclass is built on `MetaType`. A metaclass
of your own based on it gets two things plain `type` does not give.

A class statement may carry keywords, and a base whose
`__init_subclass__` takes one receives it:

```
>>> from worktoy.core import MetaType
>>> class Plugin:
...   registry = []
...   def __init_subclass__(cls, tag=None, **kwargs):
...     Plugin.registry.append(tag)
...     super().__init_subclass__(**kwargs)
>>> class Reader(Plugin, metaclass=MetaType, tag='reader', tagg='typo'):
...   pass
>>> Plugin.registry
['reader']

```

Mind the second keyword. Plain Python would end the class statement
with "takes no keyword arguments" for any keyword left over; worktoy
absorbs what no class takes, so a misspelled keyword is dropped
without a word.

And a metaclass of another library combines with a worktoy one in
either order. Python runs only the first `__init__` of a combined
metaclass, and each hands on to the next; `MetaType` hands on, so the
other one runs too, as long as it hands on in turn:

```
>>> class Registry(type):
...   classes = []
...   def __init__(cls, name, bases, space, **kwargs):
...     Registry.classes.append(name)
...     super().__init__(name, bases, space, **kwargs)
>>> class PluginMeta(MetaType, Registry):
...   pass
>>> class Exporter(metaclass=PluginMeta):
...   pass
>>> Registry.classes
['Exporter']

```

`Object` is itself built by `MetaType`, so a class mixing an `Object`
class with one of another metaclass, such as `ABCMeta`, needs a
metaclass combining the two, as Python always requires.

A class `MetaType` builds keeps the namespace its body ran in as
`__namespace__`, which is where a worktoy metaclass keeps what it
learned from the body:

```
>>> class Settings(metaclass=MetaType):
...   width = 80
>>> Settings.__namespace__['width']
80

```

A metaclass of your own may give the body a namespace of its own from
`__prepare__`, a `dict` or a subclass of it. The entries worktoy adds
itself, `__namespace__` and `__annotations__`, never pass through its
`__setitem__`, so it sees the names of the class body alone. And the
`__annotations__` of a class are always its own: for an ordinary class
that is what Python gives anyway, and it matters when a metaclass
annotates its own body, where Python may report the annotations of the
metaclass instead.

## `worktoy.utilities`

`worktoy.utilities` is the toolbox the rest of worktoy is built with: a
converter, a few text helpers, and some odd jobs. They are yours to use
as well. This part shows what each one is for and how it behaves.

Three things hold throughout:

- Every helper imports from `worktoy.utilities`, and the three
  combinatorial ones from `worktoy.utilities.combinatorics`.
- The names are camelCase. That is worktoy's house style everywhere,
  not a slip.
- The exceptions come from `worktoy.waitaminute`, worktoy's package of
  exceptions, and each one is also the builtin you would expect: a
  `TypeCastException` or a `TypeException` is a `TypeError`, an
  `UnpackException` is a `ValueError`, and `MissingVariable`,
  `ReadOnlyError` and `ProtectedError` are `AttributeError`s. Your
  existing `except` clauses keep catching them. Each carries the facts
  of the refusal as attributes, so there is never a message to parse,
  and the wording of the messages may change in any release.

Contents:

1. Converting values: `typeCast` and `__cast_as__`
2. Will `typeCast` decide? `hasCastRule`
3. Writing messages: `textFmt`, `joinWords`, `wordWrap`
4. Splitting and replacing text: `stringList`, `replaceFlex`
5. Fallbacks and loose arguments: `maybe`, `unpack`
6. Read-only attributes: `QuickDesc`, `Directory`
7. Recording what a block raised: `ExceptionInfo`
8. Slices: `sliceLen`, `ValidSlice`
9. Classes and functions: `resolveMRO`, `argsCount`
10. Combinatorics: `bipartiteMatching`, `indexPermutations`,
    `Arrangement`, `Arrangements`


### 1. Converting values: `typeCast` and `__cast_as__`

`typeCast(target, value)` gives you `value` as a `target`, or refuses.
It is the conversion every part of worktoy uses, and its rules are
narrow on purpose: it never guesses, it never parses, and it never
loses information.

A value that already is a `target` comes back untouched:

```
>>> from worktoy.utilities import typeCast
>>> typeCast(int, 7)
7
>>> typeCast(int, True)
True

```

`True` comes back as `True` because in Python a `bool` is an `int`.

Numbers convert among `bool`, `int`, `float` and `complex` when nothing
is lost:

```
>>> typeCast(int, 3.0)
3
>>> typeCast(float, 3)
3.0
>>> typeCast(complex, 1.5)
(1.5+0j)
>>> typeCast(bool, 1)
True

```

And they are refused when something would be:

```
>>> from worktoy.waitaminute.dispatch import TypeCastException
>>> for target, value in [(int, 3.5), (bool, 2), (float, 2 ** 53 + 1)]:
...   try:
...     typeCast(target, value)
...   except TypeCastException as refusal:
...     print(refusal.type_.__name__, 'refused', refusal.arg)
int refused 3.5
bool refused 2
float refused 9007199254740993

```

`3.5` is no whole number. Only `0` and `1` are booleans, so `2` is
refused: `typeCast` is not a truth test. And a `float` holds every
whole number exactly only up to `2 ** 53`, so `2 ** 53 + 1` would come
back as a different number. That last refusal depends on the value,
not the type: the same cast that works for `2 ** 53` refuses
`2 ** 53 + 1`.

Text converts among `str`, `bytes` and `bytearray`, always as UTF-8:

```
>>> typeCast(str, b'hello')
'hello'
>>> typeCast(bytes, 'hi')
b'hi'

```

Bytes in another encoding are for you to decode first.

Three things `typeCast` never does:

```
>>> from decimal import Decimal
>>> for target, value in [(int, '3'), (str, 5), (int, Decimal(3))]:
...   try:
...     typeCast(target, value)
...   except TypeCastException:
...     print('refused:', repr(value))
refused: '3'
refused: 5
refused: Decimal('3')

```

- It never parses a string. Reading `'3'` as a number is a decision
  about format (is `'3,5'` three and a half? is `'0x3'` hex?) that
  belongs to your code. When you mean it, call `int('3')` yourself.
- It never turns anything into text. `str(x)` works on every object
  there is, so a cast to text through it would accept everything.
- It converts no number outside the four builtins: `Decimal` and
  `Fraction` belong to neither family.

#### Teaching your own class to convert

A class of your own converts through a classmethod named
`__cast_as__`. Read the name as "cast this value as me": it receives
the value and returns an instance of the class, or `NotImplemented` to
refuse.

```
>>> class Count(int):
...   @classmethod
...   def __cast_as__(cls, value):
...     return cls(typeCast(int, value))
>>> count = typeCast(Count, 3.0)
>>> count, type(count).__name__
(3, 'Count')
>>> class Even(int):
...   @classmethod
...   def __cast_as__(cls, value):
...     if isinstance(value, int) and not value % 2:
...       return cls(value)
...     return NotImplemented
>>> typeCast(Even, 4)
4
>>> try:
...   typeCast(Even, 5)
... except TypeCastException:
...   print('refused 5')
refused 5

```

The hook must be a classmethod, since `typeCast` calls it on the class
to make an instance, and a subclass looking it up then builds itself. A
`__cast_as__` without `@classmethod` is refused with `UnboundCastHook`
at the first cast. Whatever the hook returns must be an instance of the
class; anything else is refused.

A subclass of a builtin converts nothing until it has a hook. That is
deliberate: `typeCast` cannot know what your constructor does, so it
will not call `Meters(3.0)` behind your back.

```
>>> class Meters(float):
...   pass
>>> try:
...   typeCast(Meters, 3.0)
... except TypeCastException:
...   print('Meters needs a __cast_as__')
Meters needs a __cast_as__

```

One more rule, for class families: when the target has a hook and the
value is an instance of a subclass of the target, the hook is asked
anyway, so the target gets an instance of its own class back.

```
>>> class Celsius(float):
...   @classmethod
...   def __cast_as__(cls, value):
...     return cls(typeCast(float, value))
>>> class Precise(Celsius):
...   pass
>>> type(typeCast(Celsius, Precise(20.0))).__name__
'Celsius'

```

There is no registry for types you do not own, such as `datetime` or
`Path`: a class without a hook converts only its own instances. The
boxes and the overloads of worktoy convert through `typeCast`; their
parts say how.


### 2. Will `typeCast` decide? `hasCastRule`

`hasCastRule(target)` tells your code whether `typeCast` owns the
conversion to `target`. It is True for the number and text builtins,
for every subclass of one, and for every class with a `__cast_as__`:

```
>>> from worktoy.utilities import hasCastRule
>>> hasCastRule(float), hasCastRule(Meters), hasCastRule(Count)
(True, True, True)
>>> hasCastRule(list)
False

```

True does not mean the cast will succeed. It means `typeCast` has the
final say, so your code should ask it and not call the class itself.
False means `typeCast` merely passes the class's own instances through,
and your code is free to convert by calling the class, as `list((1, 2))`
does. `Meters` answers True precisely so that nothing builds a `Meters`
by calling it. A `__cast_as__` without `@classmethod` is refused with
`UnboundCastHook` here too, rather than answer False, since the class is
broken, not ruleless.


### 3. Writing messages: `textFmt`, `joinWords`, `wordWrap`

#### `textFmt`

A long message reads best in the source as an indented triple-quoted
string, and badly when printed that way. `textFmt` turns it into one
clean line:

```
>>> from worktoy.utilities import textFmt
>>> message = """Expected a positive width,
...     but received a negative one."""
>>> textFmt(message)
'Expected a positive width, but received a negative one.'

```

Every run of whitespace becomes one space. Where you want a line break,
write `<br>`, and for an indent, `<tab>`, which is two spaces:

```
>>> print(textFmt('Problems found:<br><tab>width is negative'))
Problems found:
  width is negative

```

`textFmt` fills in no placeholders. Format first, then tidy, or pass
several arguments, which are joined by spaces:

```
>>> textFmt('Received', 3, 'items')
'Received 3 items'

```

A line break is `os.linesep`, so `\r\n` on Windows. Pass
`newLineSymbol='\n'` to always get `\n`. If your text really contains
`<br>`, as HTML does, choose another token with `newLineToken`, and
likewise `tabToken` and `indentSymbol` for the indent.

#### `joinWords`

`joinWords` writes a list the way a person does:

```
>>> from worktoy.utilities import joinWords
>>> joinWords('red', 'green', 'blue')
'red, green and blue'
>>> joinWords('tea', 'coffee', sep='or')
'tea or coffee'
>>> joinWords('Tom', ['Dick', 'Harry'])
'Tom, Dick and Harry'

```

`sep` is the word before the last one, not the separator between all
of them. Lists and tuples among the words are flattened, a string is
always one word, and no words at all give `''`. It writes no comma
before the last word.

#### `wordWrap`

`wordWrap(width, *text)` reflows text into lines of at most `width`
characters. The width comes first. It returns one string with the
lines joined by `os.linesep`; split it if you want a list:

```
>>> from worktoy.utilities import wordWrap
>>> print(wordWrap(12, 'lorem ipsum dolor sit amet'))
lorem ipsum
dolor sit
amet
>>> print(wordWrap(20, 'first half <br> second half'))
first half
second half

```

A `<br>` in any case forces a break, or pass another token as `newLine`.
The line breaks already in the text are whitespace like any other and
get reflowed. A word longer than the width gets a line of its own,
unbroken. A width that is no `int`, or a piece of text that is no `str`,
is refused with `TypeException`, and a width below one is refused with
`ValueError`.


### 4. Splitting and replacing text: `stringList`, `replaceFlex`

#### `stringList`

`stringList` splits strings into a clean list: every piece stripped,
the empty ones dropped.

```
>>> from worktoy.utilities import stringList
>>> stringList('a, b, c')
['a', 'b', 'c']
>>> stringList('a;b,c', separator=[',', ';'])
['a', 'b', 'c']

```

Watch the default separator: it is `', '`, a comma and a space, so
text without the space does not split at all. Say `separator=','`
when that is what you have:

```
>>> stringList('a,b')
['a,b']
>>> stringList('a,b', separator=',')
['a', 'b']

```

A list or tuple of separators splits by each in turn. A separator of any
other type is refused with `TypeException`.

#### `replaceFlex`

`replaceFlex(text, old, new, n)` replaces only the `n`-th occurrence,
counted from one; without `n`, the first:

```
>>> from worktoy.utilities import replaceFlex
>>> replaceFlex('foo bar foo baz foo', 'foo', 'X', 2)
'foo bar X baz foo'
>>> replaceFlex('aaa', 'aa', 'X', 2)
'aX'

```

Occurrences may overlap, unlike in `str.count`: `'aaa'` holds `'aa'`
twice, from the first letter and from the second. With fewer than `n`
occurrences the text comes back unchanged, so compare the result with
the text when you need to know. An `n` below one is refused with
`ValueError`, so there is no counting from the end.


### 5. Fallbacks and loose arguments: `maybe`, `unpack`

#### `maybe`

`maybe` gives the first of its arguments that is not `None`, like
`COALESCE` in SQL. Unlike `or`, it keeps the falsy values `0` and `''`:

```
>>> from worktoy.utilities import maybe
>>> maybe(None, 'fallback')
'fallback'
>>> maybe(0, 'fallback')
0
>>> maybe(None, None) is None
True

```

Its natural home is a keyword left at `None`:
`width = maybe(width, 80)`. Python works out every argument before
the call, so a fallback that is expensive to build belongs in an `if`.

#### `unpack`

`unpack` flattens the iterables among its arguments into one tuple, all
the way down:

```
>>> from worktoy.utilities import unpack
>>> unpack([1, 2], (3, [4, 5]))
(1, 2, 3, 4, 5)
>>> unpack([1, [2, 3]], shallow=True)
(1, [2, 3])
>>> unpack('abc', [1, 2])
('abc', 1, 2)

```

Text is never split into characters. Its everyday use is a function
that takes its values loose or in one list alike:

```
>>> def total(*numbers):
...   return sum(unpack(*numbers, strict=False))
>>> total(1, 2, 3), total([1, 2, 3])
(6, 6)

```

`strict=False` matters there. By default `unpack` insists on receiving
at least one iterable, and refuses the call with `UnpackException`
otherwise, with the arguments it got as `posArgs`:

```
>>> from worktoy.waitaminute import UnpackException
>>> try:
...   unpack(1, 2)
... except UnpackException as refusal:
...   print(refusal.posArgs)
(1, 2)

```

A worktoy class is kept whole, although Python sees it as iterable,
since its metaclass offers iteration to classes that ask for it:

```
>>> from worktoy.mcls import BaseObject
>>> class Plain(BaseObject):
...   pass
>>> unpack(Plain, [1])[0] is Plain
True

```

Lists, tuples, generators and any mix of them are promised. What
`unpack` does with a dict, a set or an endless iterator is not.


### 6. Read-only attributes: `QuickDesc`, `Directory`

#### `QuickDesc`

On a worktoy class, an attribute belongs in an `AttriBox` or a `Field`.
On a plain class, `QuickDesc(key)` gives a read-only view of the
attribute named `key`:

```
>>> from worktoy.utilities import QuickDesc
>>> class Box:
...   __value__ = 42
...   value = QuickDesc('__value__')
>>> box = Box()
>>> box.value
42

```

worktoy spells its private names `__value__` by house style; the key may
be any attribute name. Writing is refused with `ReadOnlyError` and
deleting is refused with `ProtectedError`, both `AttributeError`s, with
the instance and the attribute on them:

```
>>> from worktoy.waitaminute.desc import ReadOnlyError
>>> try:
...   box.value = 7
... except ReadOnlyError as refusal:
...   print(refusal.instance is box, refusal.newVal)
True 7

```

A `ProtectedError` has `oldVal` too, which may be `None` when the value
is not known.

#### `Directory`

`Directory()` gives a class the folder its source file lives in, as an
absolute path in a `str`, so it can find files kept beside it:

```python
# resources.py
from worktoy.utilities import Directory


class Resource:
  home = Directory()


Resource().home  # the absolute path of the folder holding resources.py
```

Read it through an instance. A class defined where no file stands behind
it, as under `exec`, is refused with `MissingVariable` naming the
attribute, and writing or deleting is refused with `ReadOnlyError` or
`ProtectedError`. (This example is the one in this part that cannot
run as written here, since it depends on a file; the promise in
`design/promises/utilities/promise_directory.py` runs it.)


### 7. Recording what a block raised: `ExceptionInfo`

`ExceptionInfo` is a recorder, not a judge. Give it the exception you
expect, run the block inside it, and read afterwards what happened:

```
>>> from worktoy.utilities import ExceptionInfo
>>> with ExceptionInfo(ValueError) as info:
...   int('three')
>>> info.actualExcType is ValueError
True
>>> info.actualName
'ValueError'

```

With an expected type, any exception from the block is recorded and
swallowed, even one of another type. Nothing is decided for you:
compare the two types yourself.

```
>>> with ExceptionInfo(ValueError) as info:
...   {}['missing']
>>> info.actualExcType is info.expectedExcType
False
>>> info.actualName
'KeyError'

```

That is the opposite of `assertRaises` and `pytest.raises`, which fail
on a wrong type. Without an expected type, nothing is swallowed and
`report` stays empty:

```
>>> info = ExceptionInfo()
>>> try:
...   with info:
...     {}['missing']
... except KeyError:
...   print('propagated')
propagated
>>> info.report
''

```

A `KeyboardInterrupt` or any other `BaseException` that is no
`Exception` always gets through. When nothing was raised, `actualName`
is `'No Exception'` and `actualException` and `actualExcType` are
`None`. `report` is a summary for a person to read, not for code to
parse.


### 8. Slices: `sliceLen`, `ValidSlice`

`sliceLen(s, length)` tells how many elements the slice `s` selects
from a sequence of `length` elements, without needing the sequence:

```
>>> from worktoy.utilities import sliceLen
>>> sliceLen(slice(0, 10, 2), 10)
5
>>> sliceLen(slice(5, 100), 10)
5

```

A step of zero is refused with `ValueError`, as slicing does.

`ValidSlice` is a check, not a thing to build. Python accepts anything
in a slice and complains only when it is used; `isinstance(s,
ValidSlice)` tells you at once whether start, stop and step are each
`None`, an `int` or something with an `__index__`:

```
>>> from worktoy.utilities import ValidSlice
>>> isinstance(slice(1, 10), ValidSlice)
True
>>> isinstance(slice(0, 10, 'step'), ValidSlice)
False

```

It checks the shape, not the values: `__index__` is never called, so one
that would fail still passes. Calling `ValidSlice()` is refused with
`TypeError`.


### 9. Classes and functions: `resolveMRO`, `argsCount`

`resolveMRO(*bases)` gives the resolution order a class with these
bases would have, the class itself left out, before any such class
exists. A metaclass needs that while it builds one:

```
>>> from worktoy.utilities import resolveMRO
>>> class A:
...   pass
>>> class B(A):
...   pass
>>> class C(A):
...   pass
>>> [base.__name__ for base in resolveMRO(B, C)]
['B', 'C', 'A', 'object']
>>> class Foo(B, C):
...   pass
>>> resolveMRO(B, C) == Foo.mro()[1:]
True

```

Bases Python would refuse in a class statement are refused with
`TypeError`.

`argsCount(func)` counts the positional parameters of a function,
leaving out `*args`, `**kwargs` and keyword-only parameters:

```
>>> from worktoy.utilities import argsCount
>>> argsCount(lambda a, b, *args, c=0: None)
2
>>> class Greeter:
...   def greet(self, name):
...     return name
>>> argsCount(Greeter().greet)
2

```

Mind the bound method: `argsCount` counts the parameters of the
function behind it, `self` included, not the arguments you pass. You
call `greet` with one argument; subtract one when that is what you
want to know.


### 10. Combinatorics

#### `bipartiteMatching`

`bipartiteMatching(slots)` gives every slot an index of its own, chosen
from that slot's candidates, no two alike. Seating three guests: Ada
may take chair 0 or 1, Bob only chair 0, Cy chair 1 or 2:

```
>>> from worktoy.utilities import bipartiteMatching
>>> bipartiteMatching([(0, 1), (0,), (1, 2)])
[1, 0, 2]

```

When several answers fit, which one you get is not promised. When none
fits, the call is refused with `ValueError`.

#### `indexPermutations`

`indexPermutations(n)` gives every ordering of `0` to `n - 1`, `n!` of
them, in lexicographic order:

```
>>> from worktoy.utilities.combinatorics import indexPermutations
>>> list(indexPermutations(3))
[(0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0)]

```

That is what `itertools.permutations(range(n))` gives too; this one
refuses a negative `n` with `ValueError` at the call, before you draw
anything from it.

#### `Arrangement`

An `Arrangement` is one ordering of some items, with the bookkeeping to
go both ways. `forward` says, for each slot, which item fills it;
`inverse` says, for each item, which slot it went to:

```
>>> from worktoy.utilities.combinatorics import Arrangement
>>> arrangement = Arrangement(('north', 'east', 'south'), (2, 0, 1))
>>> arrangement.values
('south', 'north', 'east')
>>> arrangement.inverse
(1, 2, 0)

```

`applyTo` puts values given in the order of the items into the order of
the arrangement, and `restoreFrom` puts them back. With the headings of
the three directions:

```
>>> arrangement.applyTo(0, 90, 180)
(180, 0, 90)
>>> arrangement.restoreFrom(180, 0, 90)
(0, 90, 180)

```

Either is refused with `ValueError` when given the wrong number of
values.

#### `Arrangements`

`Arrangements(*items)` holds every distinct ordering of the items, each
an `Arrangement`. Repeated items collapse, so three letters with one
repeated give three orderings, not six:

```
>>> from worktoy.utilities.combinatorics import Arrangements
>>> [a.values for a in Arrangements('A', 'A', 'B')]
[('A', 'A', 'B'), ('A', 'B', 'A'), ('B', 'A', 'A')]
>>> len(Arrangements('red', 'green', 'blue'))
6

```

Mind the size: `n` items have `n!` orderings, 3,628,800 for ten. Note
the two names, one letter apart: `Arrangement` takes the items as one
tuple and a recipe, `Arrangements` takes the items loose.

## `worktoy.waitaminute`

`worktoy.waitaminute` holds the exceptions of worktoy, about seventy of
them. The name is a joke on what an exception says, and it is the only
name: there is no `worktoy.exceptions`. The other parts say when
each exception is raised; this one says how to catch them, how to read
them, and how to raise them yourself.

Contents:

1. Catching worktoy's exceptions
2. Reading an exception: attributes, not messages
3. Where each exception lives
4. Raising them yourself
5. Exceptions of your own


### 1. Catching worktoy's exceptions

Every exception worktoy defines is two things at once: a
`WorkToyException`, and the builtin that best matches its meaning. So
you can catch it either way:

```
>>> from worktoy.utilities import typeCast
>>> from worktoy.waitaminute import WorkToyException
>>> try:
...   typeCast(int, '3')
... except TypeError:
...   print('caught as the builtin')
caught as the builtin
>>> try:
...   typeCast(int, '3')
... except WorkToyException:
...   print('caught as worktoy')
caught as worktoy

```

Code you already have, catching `TypeError` or `AttributeError`, keeps
working when worktoy raises one of its own.

`except WorkToyException` catches every exception worktoy defines, but
not everything worktoy raises. A few small helpers raise a plain
builtin, as `sliceLen` raises Python's own `ValueError` for a step of
zero, and the parts say where. The control-flow signals of the core
part are no `WorkToyException` either, on purpose: they are not
errors.

A few bases are worth knowing before they surprise you:

- `RecursiveRead` is a `RecursionError`, so a handler you wrote for deep
  recursion catches it too.
- `KeeResolveError`, raised when an enumeration has no member for a
  name or a value, is a plain `Exception`, not a `ValueError` as with
  Python's `Enum`.
- `KeeTypeException` is a `TypeError` but no `TypeException`; catch
  `TypeError` to get both.
- `VariableNotNone`, raised when a value meant to be set once is set
  again, is a plain `Exception`.


### 2. Reading an exception: attributes, not messages

Each worktoy exception keeps the facts it was raised with as
attributes. The message is written for a person and may be reworded in
any release; the attributes are promised.

```
>>> from worktoy.waitaminute.dispatch import TypeCastException
>>> try:
...   typeCast(int, 3.5)
... except TypeCastException as refusal:
...   print(refusal.type_.__name__, refusal.arg)
int 3.5

```

Each part names the attributes of the exceptions it raises.


### 3. Where each exception lives

The exceptions are grouped by the part of worktoy that raises them, and
each imports from its group:

- `worktoy.waitaminute`, the cross-cutting ones: `TypeException`,
  `UncheckableType`, `SubclassException` (`TypeError`);
  `UnpackException` (`ValueError`); `MissingVariable`
  (`AttributeError`); `VariableNotNone` (`Exception`); and the root,
  `WorkToyException`.
- `worktoy.waitaminute.desc`, the descriptors: `AccessError`,
  `ReadOnlyError`, `ProtectedError` (`AttributeError`, and all three
  `DescriptorException`s); `WriteOnceError`, `MissingInstanceDict`,
  `NotADescriptor` (`TypeError`); `WithoutException` (`RuntimeError`);
  `RecursiveRead` (`RecursionError`); `NamelessCallback`,
  `DanglingAlias`, `SharedDescriptor`, `ReferenceConflict`,
  `OverloadReference` (`SyntaxError`); `PhantomBoxError` and
  `DescriptorException` (`Exception`).
- `worktoy.waitaminute.meta`, the metaclasses: `IllegalInstantiation`,
  `DuplicateSentinel`, `ControlClassError` (`TypeError`);
  `DelException`, `QuestionableSyntax`, `ReservedName`,
  `UnboundClassHook`, `OverloadConflict`, `ReboundOverload`,
  `MixedMethodKind`, `ClaimedName`, `ShadowedClassHook`, `SlotsRefused`
  (`SyntaxError`); `DuplicateHook`, `HookException` (`Exception`).
- `worktoy.waitaminute.dispatch`, the overloads and conversion:
  `BareOverload`, `DispatchException`, `DuplicateSignature`,
  `TypeCastException` (`TypeError`); `UnboundCastHook` (`SyntaxError`).
- `worktoy.waitaminute.keenum`, the enumerations: `KeeBoxTypeError`,
  `KeeTypeException` (`TypeError`); `KeeBoxValueError`,
  `KeeNameConflict`, `KeeCaseException`, `KeeFlagNameError`
  (`ValueError`); `KeeWriteOnceError` (`AttributeError`);
  `KeeMemberNameError` (`SyntaxError`); `KeeBoxException`,
  `KeeDuplicate`, `KeeFlagDuplicate`, `KeeResolveError` (`Exception`).
- `worktoy.waitaminute.ezdata`, the dataclasses: `ExtraPositionalException`,
  `KwargsOnlyException`, `ExtraKeywordException`,
  `RepeatedFieldException` (`TypeError`); `DuplicateError`,
  `IncompleteFieldException`, `ReservedFieldError`, `ClassFieldError`,
  `ReservedMethodError`, `ReservedAttributeError` (`SyntaxError`).

So the place to import from follows the part of worktoy you were
using when it was raised: `TypeCastException` sits with the overloads,
which convert through `typeCast` on every call.

Many of them are `SyntaxError`s. That marks a mistake in a declaration:
the code is valid Python, but what it declares is refused, most often
as the class is created, at the line of the class body that made the
mistake. A refusal of a value passed at run time is a `TypeError`,
`ValueError` or `AttributeError` instead.


### 4. Raising them yourself

The cross-cutting exceptions at the top of `worktoy.waitaminute` are
offered for your own checks as well:

- `TypeException(name, value, *types)` for a value of the wrong type;
- `MissingVariable(instance, name, *types)` for a value still `None`;
- `VariableNotNone(name, value)` for a value meant to be set once, set
  again, `value` being the one already there;
- `UnpackException(*args)` for arguments with nothing to unpack;
- `SubclassException(subClass, baseClass)` for a class that is no
  subclass of the one required.

```
>>> from worktoy.waitaminute import TypeException
>>> def setWidth(width):
...   if not isinstance(width, (int, float)):
...     raise TypeException('width', width, int, float)
...   return width
>>> try:
...   setWidth('wide')
... except TypeError as refusal:
...   print(refusal.varName, refusal.actualType.__name__)
width str

```

Each records what you give it and checks nothing: deciding that the
value is wrong is your code's job. Mind the order of the arguments:
`TypeException` takes the name first, `MissingVariable` the instance
first. The other exceptions of worktoy are raised by worktoy, and their
constructors are not promised for raising by hand.


### 5. Exceptions of your own

A project may base its own exceptions on `WorkToyException`, with the
builtin it means beside it. Such an exception takes its message as any
Python exception does:

```
>>> class BudgetExceeded(WorkToyException, ValueError):
...   pass
>>> try:
...   raise BudgetExceeded('over by 5')
... except ValueError as error:
...   print(error)
over by 5

```

Do that when your code extends worktoy and should be caught with it.
An `except WorkToyException` then catches your exceptions too, which is
the point; for exceptions that have nothing to do with worktoy, a base
of your own is the better choice.

## `worktoy.lorem_ipsum`

`worktoy.lorem_ipsum` makes placeholder text of an exact number of
characters, for mock-ups, fixed-width fields and layout tests. It is
also a small worked example of worktoy itself: the generators are
`BaseObject` classes with boxes and overloads.

Contents:

1. Text of an exact length
2. Clause, sentence, paragraph
3. Repeatable text
4. Words of your own
5. The distributions underneath


### 1. Text of an exact length

Every generator takes a character count and gives text of exactly that
many characters:

```
>>> from worktoy.lorem_ipsum import Clause, Sentence, Paragraph
>>> paragraph = Paragraph(200)
>>> len(str(paragraph)), len(paragraph)
(200, 200)
>>> str(paragraph).startswith('Lorem ipsum')
True

```

A draw of `str(Sentence(60))` might read `Ingenium ordo sensus numerus
aura mare lorem pontus fortuna.`: Latin-looking words from the three
lists the package exports, `COMMON_WORDS`, `UNCOMMON_WORDS` and
`RARE_WORDS`, drawn mostly from the first.

The count is given by position, as `charCount`, or not at all for 40. A
negative count is refused with `ValueError` at once, and any other
keyword is refused with `TypeError`. The text is made at the first read
and kept, so two reads give the same text, and `reset()` makes a new one
of the same count:

```
>>> clause = Clause(40)
>>> str(clause) == str(clause)
True
>>> clause.reset()
>>> len(str(clause))
40

```

Assigning `charCount` makes a text of the new count, and so does
assigning `isFirst` of the next section. A generator given another of
its kind copies it, the text it has realized included.


### 2. Clause, sentence, paragraph

- A `Clause` is words joined by single spaces, without punctuation.
  Iterating it gives its words, and `len` gives its characters.
- A `Sentence` is clauses joined by `', '`, its first letter capital and
  its last character a period.
- A `Paragraph` is sentences joined by single spaces.

A paragraph, the usual block of a mock-up, opens with `Lorem ipsum`. A
clause or a sentence, which usually sits mid-text, opens with it only
when made by `first`:

```
>>> str(Clause.first(40)).startswith('Lorem ipsum')
True
>>> str(Clause.first(15))
'Lorem ipsum....'

```

The lead-in is set by `isFirst`: `first` sets it on a clause or a
sentence, and a paragraph starts with it set. Set `paragraph.isFirst =
False` for a paragraph without it; the next read makes the new text.
A first clause too short for the lead-in and one word, as fifteen
characters, comes out as the lead-in cut short and filled with dots, so
the count still holds.

The smallest count differs: a clause that is not first needs room for
its shortest word, and below that `str()` is refused with `ValueError`;
a sentence or paragraph too short for its usual parts comes out as a
placeholder of the same count.


### 3. Repeatable text

The words and lengths are drawn from Python's `random`, so seeding it
repeats a text:

```
>>> import random
>>> random.seed(7)
>>> first = str(Paragraph(200))
>>> random.seed(7)
>>> str(Paragraph(200)) == first
True

```

That is the global generator your own code may use too, so seeding it
for a snapshot test seeds both.


### 4. Words of your own

A themed mock-up wants words of its own. A subclass of `StochasticWord`
lists them in `__category_weights__`, as pairs of a tuple of words and
the weight of each word in it; a clause takes them when its `stochWord`
box is declared over that subclass:

```
>>> from worktoy.desc import AttriBox
>>> from worktoy.lorem_ipsum import StochasticWord
>>> class Fruit(StochasticWord):
...   __category_weights__ = ((('fig', 'kiwi', 'apple', 'banana'), 1.0),)
>>> class FruitClause(Clause):
...   stochWord = AttriBox[Fruit]()
>>> text = str(FruitClause(20))
>>> len(text)
20
>>> set(text.split()) <= {'fig', 'kiwi', 'apple', 'banana'}
True

```

- The weight belongs to each word, so a longer list weighs more in
  total.
- The lengths must leave no gap between the shortest and the longest
  word, since any length in that range may be drawn; a gap is refused
  with `ValueError` at the class statement.
- `Fruit()[4]` and `Fruit().realizeLength(4)` give a word of length
  four, and `realize()` a word of any length.
- A subclass of `Clause` rebinding `__lead_in__`, as `('Hello',
  'world')`, opens its first clauses with words of its own.

Words of your own reach a clause. A sentence and a paragraph build their
clauses from `Clause` itself.


### 5. The distributions underneath

The lengths of clauses and sentences come from a `GaussianLengths`,
four numbers: a mean, a variance, and two bounds, both included. A
draw is a rounded Gaussian, clamped into the bounds:

```
>>> from worktoy.lorem_ipsum import GaussianLengths
>>> lengths = GaussianLengths(40, 15, 12, 70)
>>> 12 <= lengths.sampleInteger() <= 70
True
>>> parts = lengths.partition(300)
>>> sum(parts)
300
>>> all(12 <= part <= 70 for part in parts)
True

```

`partition(total)` cuts a total into values within the bounds;
`partitionSpaced(total, spacing)` cuts it so the values plus `spacing`
for each add up to it, which is how a clause pays for the spaces after
its words: it asks for its count plus one, since the last word has no
space after it. A total no number of values can reach is refused with
`ValueError`. A mean outside the bounds, or a negative variance, is
refused with `ValueError` too. `var` is the variance, not the standard
deviation.

Each sentence holds its own `clauseDist`, and each paragraph its own
`sentenceDist`, so a project may retune the one it holds.

## `worktoy.work_test`

`worktoy.work_test` is the testing support worktoy's own suite runs on,
offered to projects as well: a `unittest.TestCase` base with a
sub-test that checks every case, seeded random data, and a pattern for
running one bank of tests against several implementations.

Contents:

1. `BaseTest` and its `subTest`
2. Random data: the samplers
3. One bank of tests, many implementations


### 1. `BaseTest` and its `subTest`

Base a test class on `BaseTest` as on `unittest.TestCase`. Its
`subTest` runs every block of a loop, even after one fails, and the test
then fails once, with every failed block named:

```
>>> import unittest
>>> from worktoy.work_test import BaseTest
>>> class TestSquares(BaseTest):
...   def test_squares(self):
...     for value in (1, 2, 3, 4):
...       with self.subTest(value=value):
...         self.assertNotIn(value, (2, 3))
>>> result = unittest.TestResult()
>>> _ = unittest.TestLoader().loadTestsFromTestCase(TestSquares).run(result)
>>> result.testsRun, len(result.failures)
(1, 1)
>>> report = result.failures[0][1]
>>> 'value=2' in report, 'value=3' in report
(True, True)

```

What it adds over the `subTest` of `unittest`: that one reports each
failed block to the runner on its own, which some runners show poorly.
This one collects every block and fails the test once, at its end, with
the label and the traceback of each block that failed, so any runner
shows them all. A block raising an error, not only a failed assertion,
is recorded the same way and the loop goes on. Nested blocks join their
labels, as `outer=1 -> inner=2`.

A `setUp` of your own needs no call of the base's. `BaseTest` also has
`assertIsNotInstance` and `assertIsNotSubclass`, the negative
assertions under worktoy's names, on every Python worktoy supports.
`unittest` spells the first `assertNotIsInstance`, and gained its own
subclass pair only in Python 3.14.


### 2. Random data: the samplers

Each test has samplers of its own: `randomInteger`, `randomFloat`,
`randomGaussian`, `randomSymbolicName`, `randomWord` and `randomLorem`.
`seedSamplers(seed)` seeds them all, so the test repeats its data;
seed in `setUp` to make every run alike.

A sampler draws one value with `item`, a row with `row` and a table
with `table`, each anew at every read:

```
>>> from worktoy.work_test.samplers import IntSampler
>>> dice = IntSampler(1, 6, width=4, height=3, seed=7)
>>> len(dice.row), [len(row) for row in dice.table]
(4, [4, 4, 4])
>>> dice.item in range(1, 7)
True
>>> IntSampler(1, 6, seed=7).row == IntSampler(1, 6, seed=7).row
True

```

- The bounds are both included, and a swapped pair is put right:
  `IntSampler(6, 1)` draws from 1 to 6.
- A row is `width` or `size` values long, a table `height` or `count`
  rows; a size below one is refused with `ValueError`, and a keyword
  naming no setting is refused with `TypeError`.
- Each sampler draws from a generator of its own, `random`, which
  `seed=` seeds, so other code drawing in between changes nothing.

A sampler of your own subclasses `BaseSampler` with two methods, the
type of its values and a recipe for one:

```
>>> from worktoy.desc import AttriBox
>>> from worktoy.work_test.samplers import BaseSampler
>>> class DieSampler(BaseSampler):
...   sides = AttriBox[int](6)
...   def _getValueType(self, **kwargs):
...     return int
...   def _getItem(self, *args, **kwargs):
...     return self.random.randint(1, self.sides)
>>> die = DieSampler(seed=3)
>>> die.sides = 20
>>> die.item in range(1, 21)
True

```

Its settings are boxes, set after construction. A sampler leaving out
either method cannot be instantiated, and is refused with `TypeError`.

For text, `loremSentence(n)` gives a sentence of exactly `n`
characters, capitalized and closed by a period, and `randomWord()` a
word of `LOREM_WORDS`. These two draw from Python's own `random`, so
`random.seed` repeats them.


### 3. One bank of tests, many implementations

Several classes implementing one interface should pass one set of
tests, written once. `ComplexTest` shows the pattern: a bank of tests
for complex-number arithmetic, run against every class a test lists in
`targets`. `ComplexMixin` is the implementation it comes with, a class
getting the whole arithmetic of `complex` from two parts, `REAL` and
`IMAG`:

```
>>> from worktoy.work_test import ComplexMixin, ComplexTest
>>> class Simple(ComplexMixin):
...   pass
>>> z = Simple(1, 2)
>>> complex(z + Simple(3, 4)), z == 1 + 2j, abs(Simple(3, 4))
((4+6j), True, 5.0)
>>> class TestSimple(ComplexTest, BaseTest):
...   targets = (Simple,)
>>> result = unittest.TestResult()
>>> _ = unittest.TestLoader().loadTestsFromTestCase(TestSimple).run(result)
>>> result.wasSuccessful(), result.testsRun > 0
(True, True)

```

- The bank goes first among the bases and a test case after it,
  `BaseTest` or any other. A class listing the bank without a test case
  is refused with `TypeError`, so its tests cannot vanish from a run
  unnoticed.
- The bank has no base of its own, so it is never collected and run by
  itself. A test class without `targets` skips every test.
- A `ComplexMixin` is built from nothing, one number, a `complex`, a
  string `complex` parses, or two parts. It equals and hashes as
  `complex` does, and iterates its two parts.

A bank of your own follows the same shape: a class with no base,
holding test methods that loop over `self.targets` in blocks of
`subTest`, listed first beside a test case.

## What can I rely on?

The parts above describe what worktoy does. This last part answers what
a project built on it will want to know before an update: what stays,
what may change, and how it would be told.

### 1. Will this still work after an update?

The design of a behaviour is one thing: what works, and what is refused
on the way. A box of `float` keeps a number assigned to it as a `float`,
and refuses a text:

```
>>> from worktoy.desc import AttriBox
>>> from worktoy.mcls import BaseObject
>>> class Point(BaseObject):
...   x = AttriBox[float](0.0)
>>> point = Point()
>>> point.x = 3
>>> point.x
3.0
>>> try:
...   point.x = 'three'
... except Exception as refusal:
...   print(type(refusal).__name__)
TypeException

```

The parts above describe both in one breath, as here, since both are the
intended behaviour. They differ in what a project may build on.

What works is a promise. A promise is kept for every release of a major
version: what is promised in one release of 1.x works in every later
release of 1.x. That an `int` assigned to a box of `float` is kept as a
`float` is a promise.

What is refused is a refusal: a certain mistake raises an exception
where it is made, instead of passing in silence. A refusal names the
exception it raises as of a stated version: the exceptions this document
names are the ones raised as of 1.2.3. As of that version, a text
assigned to the box above is refused with `TypeException`. A refusal is
no promise, in two ways.

- Which exception is raised is not promised. It is the one raised as of
  the version stated, and may be another in any later release. Each
  refusal among the tests states its own version. When the exception of
  a refusal changes, the version stated for it changes with it. - A
  refusal may be relaxed. A later release may accept what an earlier one
  refused, as a class keyword lifting a rule does, or a rule that turned
  out stricter than it had to be. Relaxing a refusal is not a
  deprecation: it gives no notice and waits for no major update, since
  nothing that worked stops working when a mistake is no longer refused.

So do not build on a refusal. Code that makes the mistake on purpose and
catches the exception in order to go on leans on something that may
change in any release.

An exception of your own is another matter. When a callback, a hook or a
fallback you wrote raises, your exception reaches the caller as you
raised it, and that is a promise.

A behaviour the design does not cover may change in any release. That
holds for everything this document does not show, the wording of a
message and the text `str` and `repr` give among it.

### 2. What does an exception tell me?

What a worktoy exception is and carries, once it is raised, is promised
by the exception itself. The builtin exception it is based on stays,
so an `except TypeError` or an `except AttributeError` that catches one
keeps catching it. And each keeps the facts it was raised with as
attributes, as `TypeException` keeps the name, the object of the wrong
type and the types that would have been accepted. The part on
`waitaminute` goes through them. The message of an exception is for
people, and its wording is not promised.

### 3. What does deprecated mean here?

A deprecation is a promise that ends at the next major update. Until
then the feature works as it did, in every release of the major version
that deprecated it, and gives a deprecation notice where it is used, a
`FutureWarning`. A deprecation takes a notice and a major update because
something that works is going to stop working. That is what sets it
apart from a refusal being relaxed, where nothing stops working.

### 4. Has worktoy ever taken a promise back?

A confession is a promise worktoy made and could not keep, because it
contradicted another promise or itself. Such a promise is taken back in
a minor update, in the open: the confession says what was promised, when
it was taken back and why, and promises nothing in its place.

### 5. Where is all of this written, and how is it checked?

The design lies in the folder `design` of the repository, beside the
source:

- `design/promises/<package>` holds the promises of each package, as
  tests, and `design/promises/deprecations` those that end at the next
  major update. - `design/refusals/<package>` holds its refusals, each
  with the version its exceptions are stated for. -
  `design/promises/waitaminute` holds what the exceptions themselves
  promise. - `design/confessions` holds the confessions. -
  `design/manual.md`, this document, describes the design of each
  package, what works and what is refused together, with checked
  examples.

Both are checked from the root of the repository:

```terminaloutput python -m unittest discover -s design -t . -p
"promise_*.py" python -m doctest design/manual.md ```

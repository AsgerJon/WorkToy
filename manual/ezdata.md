# worktoy manual: ezdata

`worktoy.ezdata` holds `EZData`, worktoy's dataclass. Declare the fields
in the class body and the class receives its constructor, equality,
iteration and the rest. Unlike a standard dataclass, every value is
held to its type, as the constructor runs and at every assignment
after.

Everything shown here is promised. The examples are checked against
every release, so they keep working in every update. Anything this
chapter does not show may change.

Contents:

1. Declaring a dataclass
2. What counts as a field
3. Making an instance
4. Using an instance
5. Frozen, ordered, keyword-only
6. Inheritance
7. Mistakes caught as the class is created


## 1. Declaring a dataclass

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


## 2. What counts as a field

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
- A bare `None` has no type, and raises `IncompleteFieldException`.
  There is no optional field: every field holds a value of its type, and
  every field has a default.
- `EZField[THIS]`, a field of the class's own type, raises `TypeError`,
  since no value of the class exists while its body runs.

A default is built anew for each instance, so no two instances share a
mutable default. For a number or a text field the default converts as
`typeCast` converts, so `EZField[int]('7')` is refused; for any other
type the type is called with the arguments, so
`EZField[list]('abc')` holds `['a', 'b', 'c']`.


## 3. Making an instance

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

Too many positional arguments raise `ExtraPositionalException`, an
unknown keyword `ExtraKeywordException`, and a field given both ways
`RepeatedFieldException`, all `TypeError`s.

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


## 4. Using an instance

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
- `__match_args__` lists the fields, so `match` works on Python 3.10
  and later.
- Two instances are equal when their values are and they are of one
  lineage: a class and its subclasses, a frozen subclass included. An
  instance of a sibling class, or a tuple, is never equal.
- An instance is not hashable unless its class is frozen.
- Assigning a field converts as the constructor does. Deleting a field
  raises `AttributeError`.
- Any other attribute may be set and deleted freely, and stays out of
  the values and equality. So a typo, `point.xx = 5`, creates an
  attribute rather than failing.

The class writes `__repr__` and `__str__` for you, but their text is not
promised; a body may write its own, as it may `asDict`, `asTuple` and
`replace`.


## 5. Frozen, ordered, keyword-only

Three class keywords change a dataclass, each under several names:

- `frozen=True`, or `immutable` or `hashable`: every assignment and
  deletion raises `AttributeError`, and instances hash, equal ones
  alike. `__post_init__` cannot assign to a frozen instance either.
- `ordered=True`, or `order`, `sortable` or `comparable`: instances
  compare field by field, in order.
- `kwOnly=True`, or `keywordOnly` or `kw_only`: the constructor takes
  keywords only, and raises `KwargsOnlyException` for a positional
  argument.

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

The class answers `isFrozen`, `isOrdered` and `kwOnly`. A subclass of
an ordered class is ordered. A subclass of a frozen class must say
`frozen=True` itself, or the class statement raises `TypeError`. And a
misspelled keyword, as `frozn=True`, is dropped without a word, as every
class keyword no class takes is in worktoy.


## 6. Inheritance

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


## 7. Mistakes caught as the class is created

- `EZField(1)` without a type, and `EZField[int]` without parentheses,
  raise `IncompleteFieldException`.
- A field bound twice raises `DuplicateError`.
- A field named after a generated method, as `replace`, `asDict` or
  `__post_init__`, raises `ReservedFieldError`.
- A body defining a method `EZData` writes itself, as `__init__`,
  `__eq__` or `__setattr__`, raises `ReservedMethodError`, and one
  binding an attribute it sets itself, as `__kw_only__`,
  `ReservedAttributeError`.

All of these are `SyntaxError`s, as the exceptions chapter explains.
`EZMeta`, `EZSpace`, `EZHook` and `EZStore` are the machinery behind
the class, public for a project building a dataclass base of its own.

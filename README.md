[![wakatime](https://wakatime.com/badge/github/AsgerJon/WorkToy.svg)](https://wakatime.com/badge/github/AsgerJon/WorkToy) [![codecov](https://codecov.io/gh/AsgerJon/WorkToy/graph/badge.svg?token=FC0KFZJ7JK)](https://codecov.io/gh/AsgerJon/WorkToy)
[![PyPI version](https://badge.fury.io/py/worktoy.svg)](https://pypi.org/project/worktoy/)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPLv3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

# worktoy v0.99.xx

The **worktoy** provides utilities for Python development focused on
reducing boilerplate code, type-safety and readability. Each release is
tested thoroughly on each supported Python version from 3.7* to 3.14.

*Maybe it is time to consider updating if you are still using Python 3.7.

# Table of Contents

- [Installation](#installation)
- [Introduction](#introduction)
- [Features](#features)
- [Usage](#usage)
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
'trust-me-bro'-typing. Point('breh', None) will happily create a `Point`
object.

Instead:

```python
class Point:
  x = AttriBox[float](0.0)
  y = AttriBox[float](0.0)

  def __init__(self, x: float = 0.0, y: float = 0.0) -> None:
    self.x = x
    self.y = y
```

When ```AttriBox``` says `float` it enforces `float` at runtime.
Attributes are declared explicitly at the class level. Despite this,
flexibility remains, for example:

```python
point = Point(69, '420')  # int, str
point.x == 69.0
point.y == 420.0
```

When types do not match, `AttriBox` attempts casting before raising an
error. Same ergonomics. Stronger guarantees.

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

Conditional branches. Growing complexity. Manuel parsing. Long gone are
those happy days of effortless coding.

But it does not have to be like this. Introducing `@overload`:

```python
from __future__ import annotations

from typing import Self

from worktoy.mcls import BaseObject
from worktoy.core.sentinels import THIS
from worktoy.dispatch import overload
from worktoy.desc import AttriBox


class Point(BaseObject):
  x = AttriBox[float](0.0)
  y = AttriBox[float](0.0)

  @overload(float, float)
  def __init__(self, x: float = 0.0, y: float = 0.0) -> None:
    self.x = x
    self.y = y

  @overload(complex)
  def __init__(self, z: complex) -> None:
    self.x = z.real
    self.y = z.imag

  @overload(THIS)  # THIS is a special token type-hinting to the class itself
  def __init__(self, other: Self) -> None:
    self.x = other.x
    self.y = other.y
```

Each new signature requires one new overloaded function. No more painful
parsing of `*args`. All of this just works. Actually.

## "Show Don't Tell" Is for Stories, not for Code!

When reading code, you look for declarations.
For where symbols are defined. For where meaning begins.

In storytelling, subtle declaration is art. In *Clair Obscur: Expedition 33*,
the horror of the *Gomache* unfolds gradually until Sophie disappears in
Gustave's arms. The imperative subtlety grants the story its emotional
impact.

In code, the declaration **is** the point! In matters of code, I want
declarations. I don’t want foreshadowing. I don’t want subtlety. I don’t
want subversion of expectations. I want declarations.

Anyway, what were we talking about?
Right — figure out what point.r is from the code below:

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
worse in other languages. Anyway, here is the alternative provided by *
*worktoy**: `Field`.

```python
class Point(BaseObject):
  x = AttriBox[float](0.0)
  y = AttriBox[float](0.0)

  r = Field()  # Straight up declaration! 

  @overload(float, float)
  def __init__(self, x: float = 0.0, y: float = 0.0) -> None:
    self.x = x
    self.y = y

  @overload(complex)
  def __init__(self, z: complex) -> None:
    self.x = z.real
    self.y = z.imag

  @overload(THIS)  # THIS is a special token type-hinting to the class itself
  def __init__(self, other: Self) -> None:
    self.x = other.x
    self.y = other.y

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

Inspecting the class reveals nothing about x or y. They do not exist at the
class level. They are created at runtime on the instance. Two common
remedies are `__slots__` and annotations:

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

Both improve clarity. But in both cases `Point.x` and `Point.y` will raise
`AttributeError`. The presence of `x` and `y` becomes visible only after
instantiation. At this point, they are just attributes of the instance, not
of the class. Setting during `__init__` makes no difference compared to
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

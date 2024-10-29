[![wakatime](https://wakatime.com/badge/github/AsgerJon/WorkToy.svg)](https://wakatime.com/badge/github/AsgerJon/WorkToy)

# worktoy v0.99.xx

This library leverages the most advanced Python features including the
descriptor protocol and support for customizable metaclasses. The
documentation below explains these features and how **worktoy** leverages
them to provide powerful and flexible tools for Python developers.

# Table of Contents

- [Installation](#installation)
- [Introduction](#introduction)
- [Usage](#usage)
  * [```worktoy.text```](#worktoytext)
    + [```worktoy.text.stringList```](#worktoytextstringlist)
    + [```worktoy.text.monoSpace```](#worktoytextmonospace)
    + [```worktoy.text.wordWrap```](#worktoytextwordwrap)
    + [```worktoy.text.typeMsg```](#worktoytexttypemsg)
    + [```worktoy.text.joinWords```](#worktoytextjoinwords)
  * [```worktoy.parse```](#worktoyparse)
    + [```worktoy.parse.maybe```](#worktoyparsemaybe)

  + [```worktoy.desc```](#worktoydesc)
    + [```worktoy.desc.Field```](#worktoydescfield)
    + [```worktoy.desc.AttriBox```](#worktoydescattribox)
    + [```worktoy.desc.THIS```](#worktoydescthis)

  + [```worktoy.base```](#worktoybase)
  + [```worktoy.keenum```](#worktoykeenum)

# Installation

The stable version of **worktoy** may be installed using the following
command:

```bash 
pip install worktoy
```

The development version, which is not for the faint of heart, may be
installed by passing the ``--pre`` flag:

```Bash
pip install worktoy --pre
```

# Introduction

The **usage** section aims to provide a concise explanation of how to use
the **worktoy** library. A much more in depth explanation of the contents
is under development.

# Usage

This section explains the packages included in the **worktoy** library in
the order they are imported.

## ```worktoy.text```

This package provides functions for manipulating text. The functions are
very simple but widely used across **worktoy**.

### ```worktoy.text.stringList```

This function saves you a lot of quotation marks:

```python
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.text import stringList

if __name__ == '__main__':
  foo = ['so', 'many', 'quotation', 'marks!']
  bar = stringList("""so, many, quotation, marks!""")
  print(foo == bar)  # True
```

Just write a string with comma, space separated words and the function
will return a list of the words, providing a much more convenient way of
defining a list of strings.

### ```worktoy.text.monoSpace```

Python provides a convenient way of defining long strings using triple
quotes. However, when including new lines in such a string it is likely
done for code readability, rather than requiring a linebreak at that
particular position. The ``monoSpace`` function modifies a string to have
only single spaces between words and no leading or trailing spaces. If a
linebreak is intended, include ```'<br>'``` in the string to force a
linebreak.

```python
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.text import monoSpace

if __name__ == '__main__':
  foo = """Welcome to the monoSpace documentation! <br> After that 
  convenient linebreak, we are done!"""
  bar = monoSpace(foo)
  print(bar)
```

The above outputs:

  ```terminal
  Welcome to the monoSpace documentation!
  After that convenient linebreak, we are done!
  ```

Inclusion of ```'<br>'``` explicitly forces a linebreak. Otherwise, the
function removes all linebreaks and multiple spaces between words.

### ```worktoy.text.wordWrap```

This function takes a string and splits it into lines not exceeding a
specified width and returns a list of the lines.

```python
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.text import wordWrap

if __name__ == '__main__':
  foo = """This is a long string that needs to be wrapped. It is 
  important that the wrapping is done correctly. Otherwise, the text 
  will not be readable. """
  lineWidth: int = 40  # The line must not exceed 40 characters
  bar: list[str] = wordWrap(lineWidth, foo)  # Returns a list
  for line in bar:
    print(line)
```

The above outputs:

```terminal
This is a long string that needs to be
wrapped. It is important that the
wrapping is done correctly. Otherwise,
the text will not be readable.
```

### ```worktoy.text.typeMsg```

When type-guarding a particular variable, an unsupported type should
result in a TypeError. The `typeMsg` function provides a convenient way
to raise a TypeError with a custom message if the type is not supported.

```python
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import sys

from worktoy.text import typeMsg, wordWrap


def foo(bar: int) -> None:
  if not isinstance(bar, int):
    e = typeMsg('bar', bar, int)
    raise TypeError(e)
  print(bar)


if __name__ == '__main__':
  susBar = 'sixty-nine'
  try:
    foo(susBar)  # That's not an int!
  except TypeError as typeError:
    errorMsg = str(typeError)  # Let's wrap this string at 50 characters
    wrapped = wordWrap(50, errorMsg)  # We apply 'str.join' to the list
    msg = '\n'.join(wrapped)
    print(msg)
    sys.exit(0)
```

The above outputs the following:

```terminal
Expected object 'bar' to be of type 'int', but
found 'sixty-nine' of type 'str'!
```

### ```worktoy.text.joinWords```

Recall the ```stringList``` function mentioned earlier. The
```joinwords``` function does nearly the opposite: It takes a list of
strings and joins them to one string with commas in between, except for
in between the last two words where an 'and' is used.

```python
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.text import joinWords

if __name__ == '__main__':
  foo = ['Tom', 'Dick', 'Harry']
  print(joinWords(foo[0]))  # 'Tom'
  print(joinWords(*foo[:2]))  # 'Tom and Dick'
  print(joinWords(*foo[:3]))  # 'Tom, Dick and Harry'
```

The above outputs the following:

```terminal
Tom
Tom and Dick
Tom, Dick and Harry
```

In summary, ```worktoy.text``` provides the following:

- ```stringList```
- ```monoSpace```
- ```wordWrap```
- ```typeMsg```
- ```joinWords```

## ```worktoy.parse```

This module provides the ```None```-aware ```maybe``` function.

### ```worktoy.parse.maybe```

*Simplify identity-checks with the ```maybe``` function.*

```Python
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any
from worktoy.parse import maybe

fallback = 69.


def verboseFunc(arg: float = None) -> Any:
  """Verbose identity check"""
  if arg is None:
    val = fallback
  else:
    val = arg


def syntacticSugarFunc(arg: float = None) -> Any:
  """Syntactic sugar alternative"""
  val = maybe(arg, fallback)
```

This function takes any number of arguments and returns the first that is
different from ```None```.

## ```worktoy.desc```

This module provides classes implementing the descriptor protocol

### ```worktoy.desc.Field```

Python allows significant customization of the attribute access mechanism
through the descriptor protocol. Use ```GET```, ```SET``` and ```DELETE```
to specify the accessor methods. For example:

```Python
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import sys
from typing import Never

from worktoy.desc import Field


class Point:
  """A point in 2D space"""

  _x = 0.0  # Private value
  _y = 0.0  # Private value

  x = Field()
  y = Field()

  @x.GET  # Specify the getter method
  def _getX(self) -> float:
    return self._x

  @x.SET  # Specify the setter method
  def _setX(self, value: float) -> None:
    self._x = float(value)  # cast to float

  @x.DELETE  # Specify the deleter method as appropriate
  def _delX(self, *_) -> Never:
    """Deleter methods are rarely used in practice. This is because 
    deviating from expected behaviour can lead to undefined behaviour 
    when other libraries expect the default behaviour. Particularly, when 
    a custom implementation fails to raise an expected error. Unless 
    specifically needed, it is advisable to omit the deleter method. The 
    safest option is to explicitly raise an error like done here. """
    e = """Tried deleting protected attribute!"""
    raise TypeError(e)

  #  Accessor methods for 'y' left as an exercise to the try-hard reader.


if __name__ == '__main__':
  point = Point()
  print(point.x)  # Getter function returns default value
  point.x = 69.  # Setter function changes the value
  print(point.x)  # Getter function returns new value
  try:
    del point.x  # Deleter function raises an error
  except TypeError as typeError:
    print('%s: %s' % (typeError.__class__.__name__, str(typeError)))
  sys.exit(0)
```

The above outputs the following:

```terminal
0.0
69.0
TypeError: Tried deleting protected attribute!
```

In summary, the ```Field``` class provides a descriptor implementation
that allows the owning class to entirely define how the attribute is
accessed.

### ```worktoy.desc.AttriBox```

Where the ```Field``` class required the accessor methods to be explicitly
implemented by the owning class, the ```AttriBox``` class provides a
highly general descriptor implementation requiring only one line in the
owning class body. It uses a powerful and novel syntax. The attribute can
point to any object of any type: ```attr = AttriBox[cls](*args, **kwargs)```
This creates a descriptor instance pointing to an instance of ```cls```.
The default value is created only when necessary by passing the given
arguments to the constructor of ```cls```.

```Python
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import sys

from worktoy.parse import maybe
from worktoy.desc import AttriBox


class Point:
  """A point in 2D space"""

  x = AttriBox[int](0)
  y = AttriBox[int](0)

  def __init__(self, x: int = None, y: int = None) -> None:
    self.x = maybe(x, 0)
    self.y = maybe(y, 0)
    print("""Created: %s""" % str(self))  # Logs creation of Point instance

  def __str__(self, ) -> str:
    return """Point: (%d, %d)""" % (self.x, self.y)


class Circle:
  """A circle in 2D space"""

  center = AttriBox[Point](69, 420)
  radius = AttriBox[float](1.337)

  def __init__(self, *args) -> None:
    """The constructor may optionally receive a Point object as the
    center of the circle. """
    for arg in args:
      if isinstance(arg, Point):
        self.center = arg
        break

  def __str__(self, ) -> str:
    return """Circle spanning .3f% from %s""" % (self.radius, self.center)


if __name__ == '__main__':
  circle = Circle()
  #  This creates the object 'circle' as an instance of 'Circle', however, 
  #  the 'circle.center' object does not actually exist yet. 
  print("""Created instance of 'Circle'""")
  P = circle.center
  print(P)
  #  The 'circle.center' object is created when accessed here. AttriBox 
  #  creates the object by passing the given arguments to the constructor 
  #  of the given class, in this case: 'Point(69, 420)'. This triggers the
  #  print statement in the '__init__' method of the 'Point' class.
  Q = circle.center
  #  Now that the object exists, the existing object is returned, so 
  #  there is no output from the '__init__' method of the 'Point' class.
  if P is not Q:
    raise ValueError
  newCenter = Point(1337, 80085)
  newCircle = Circle(newCenter)
  #  This creates a new circle with the center at the same point as the
  #  previous circle. The 'Point' object is passed to the constructor of
  #  the 'Circle' class, which assigns it to the 'center' attribute.
  #  Because the attribute is set to a specific object, before it is ever 
  #  otherwise accessed, 'AttriBox' never creates a new object. Instead, 
  #  it makes use of the object passed in the constructor.
  print(newCircle.center)
  print(newCircle)
  if newCircle.center is not newCenter:
    raise ValueError
  sys.exit(0)

```

The above outputs the following:

```terminal
Created instance of 'Circle'
Created: Point: (69, 420)
Point: (69, 420)
Created: Point: (1337, 80085)
Point: (1337, 80085)
Circle spanning 1.337 from Point: (1337, 80085)
```

The terminal output above shows the ordering of events: The ```Circle```
instance is created *before* the center ```Point``` is even created.
```AttriBox``` creates a ```Point``` instance when the center attribute
is accessed. It passes the arguments on to the constructor of the
```Point``` class. The created ```Point``` instance is then assigned to
the center attribute of the ```Circle``` instance. When setting ```Q``` to
```circle.center```, the object created previously is returned. Thus,
```P is Q``` is ```True```.

Next, the ```newCenter``` is created and is passed to the ```Circle```
constructor. When the print statement then accesses the ```center```
attribute on the new ```Circle``` instance, the existing ```Point```
instance is returned by ```AttriBox```.

### ```worktoy.desc.THIS```

The ```THIS``` object is a novel and powerful feature of the ```worktoy```
library.

In the previous example of ```AttriBox```, the ```Point``` class was
instantiated with the arguments ```69``` and ```420```, when creating the
```circle.center``` object. When ```AttriBox``` receives the ```THIS```
object as an argument, it passes the owning instance to the constructor.

```Python
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations
from worktoy.desc import AttriBox, THIS


class Owner:
  """A class that uses THIS to pass itself to the attribute"""

  name = AttriBox[str]('John Doe')

  def __init__(self, name: str = None) -> None:
    if isinstance(name, str):
      self.name = name

  def __str__(self) -> str:
    return """Owner named: %s""" % self.name


class Dependent:
  """A class that gets initialized with an instance of Owner"""

  owner = AttriBox[Owner]()

  def __init__(self, composition: object) -> None:
    owner = getattr(composition, 'owner', None)
    if owner is None:
      raise ValueError
    self.owner = owner

  def __str__(self) -> str:
    return """Dependent of: '%s'""" % self.owner


class Composition:
  """Composition class demonstrating use of THIS with AttriBox"""

  owner = AttriBox[Owner]('Jack Doe')
  dependent = AttriBox[Dependent](THIS)

  def __init__(self) -> None:
    pass


if __name__ == '__main__':
  comp = Composition()
  print(comp.owner)  # Instantiates Owner with 'Asger'
  print(comp.dependent)  # Instantiates Dependent with the Owner instance
```

The above outputs the following:

```terminal
Owner named: Jack Doe
Dependent of: 'Owner named: Jack Doe'
```

When a class is created in Python the code body is executed before the
class is created. Thus, the class body itself is not able to reference
the class itself directly. When instantiating ```AttriBox``` arguments to
be passed to the constructor of the field class can still include the
instance of the class being accessed. To achieve this, the ```THIS```
object should be passed as an argument to the ```AttriBox``` instance. In
the same style, ```TYPE``` would refer to the owner of the
instance, ```BOX``` would refer to the ```AttriBox``` instance, and
```ATTR``` to the ```AttriBox``` (or subclass hereof) class object.

## ```worktoy.base```

```worktoy``` provides two base classes for general use: ```BaseObject```
and ```FastObject```. Both support function overloading. The latter does
not allow dynamically created attributes and is faster due to the use of
```__slots__```. All attributes on a ```FastObject``` subclass must be
instances of ```AttriBox```.

The ```@overload``` decorator allows for function overloading in Python.
This allows a named function to support multiple argument signatures.
Like ```AttriBox```, the ```@overload``` decorator understands ```THIS```
to mean an instance of the class.

Below is an implementation of a complex number as a subclass of
```FastObject``` allowing multiple argument signatures in the constructor
by leveraging the ```@overload``` decorator.

```Python
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Self

from worktoy.base import FastObject, overload
from worktoy.desc import AttriBox, THIS
from worktoy.meta import DispatchException


class Complex(FastObject):
  """Complex number implementation using AttriBox"""

  RE = AttriBox[float](0.)
  IM = AttriBox[float](0.)

  @overload(float, float)
  def __init__(self, x: float, y: float) -> None:
    self.RE, self.IM = x, y

  @overload(complex)
  def __init__(self, z: complex) -> None:
    self.RE, self.IM = z.real, z.imag

  @overload(float)
  def __init__(self, x: float) -> None:
    self.__init__(x, 0.)

  @overload(tuple)
  def __init__(self, z: tuple) -> None:
    self.__init__(*z, )

  @overload(THIS)  # As explained in the previous section
  def __init__(self, other: Self) -> None:
    self.RE, self.IM = other.RE, other.IM

  def __str__(self) -> str:
    return """%.2f + %.2fJ""" % (self.RE, self.IM)

  def __add__(self, other: object) -> Self:
    if isinstance(other, Complex):
      return Complex(self.RE + other.RE, self.IM + other.IM)
    try:
      return self + Complex(other)
    except DispatchException:
      return NotImplemented

  #  Remaining arithmetic operations left as an exercise to the reader.


if __name__ == '__main__':
  z1 = Complex(69, 420)
  print(z1)
  z2 = Complex(z1)
  print(z2)
  z3 = Complex(69 + 420j)
  print(z3)
  z4 = Complex((69, 420))
  print(z4)
  w = Complex(1337, 80085)
  print(w)
  print(w + 69.)
  print(w + (69, 420))

```

The above outputs the following:

```terminal
69.00 + 420.00J
69.00 + 420.00J
69.00 + 420.00J
69.00 + 420.00J
1337.00 + 80085.00J
1406.00 + 80085.00J
1406.00 + 80505.00J
```

The complex number implementation supports multiple argument signatures.
The addition operator leverages the flexibility in the constructor to
support multiple other types.

In summary, ```BaseObject``` and ```FastObject``` provide base classes
for general use. They add function overloading to Python. The former
retains the familiar flexibility allowing dynamic attribute creation,
while the latter provides a significant increase in speed at the cost of
this flexibility.

## ```worktoy.keenum```

```KeeNum``` provides a flexible enumeration class. Instances are managed
by internal integer values, leaving available public values that are
never used or accessed by the internal logic. Subclasses provide
iteration over their enumerated instances in the order they appear in the
class body. If no value is passed to the ```auto``` function, then the
key is used as the public value.

In the following example, we will create a normal class that encapsulates
colors represented by red, green and blue values. We will then enumerate
a number of common colors using the ```KeeNum``` class.

```Python
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
import string
from __future__ import annotations

from worktoy.keenum import KeeNum, auto
from worktoy.base import FastObject, overload
from worktoy.desc import AttriBox, THIS


class RGB(FastObject):
  """Each color channel is an integer in the range 0-255 managed by 
  AttriBox instances."""

  red = AttriBox[int](0)
  green = AttriBox[int](0)
  blue = AttriBox[int](0)

  @overload(int, int, int)
  def __init__(self, r: int, g: int, b: int) -> None:
    self.red, self.green, self.blue = r, g, b

  @overload(int, int)
  def __init__(self, r: int, g: int) -> None:
    self.__init__(r, g, 0)

  @overload(int)
  def __init__(self, r: int) -> None:
    self.__init__(r, 0, 0)

  @overload(tuple)
  def __init__(self, rgb: tuple) -> None:
    self.__init__(*rgb)

  @overload(THIS)
  def __init__(self, other: RGB) -> None:
    self.red, self.green, self.blue = other.red, other.green, other.blue

  @overload()
  def __init__(self) -> None:
    self.__init__(0, 0, 0)

  def __str__(self) -> str:
    """Hex representation of the color"""
    return """#%02X%02X%02X""" % (self.red, self.green, self.blue)

  def __repr__(self, ) -> str:
    """Code representation"""
    return """RGB(%d, %d, %d)""" % (self.red, self.green, self.blue)


class Color(KeeNum):
  """Enumeration of common colors"""

  RED = auto(RGB(255, 0, 0))
  GREEN = auto(RGB(0, 255, 0))
  BLUE = auto(RGB(0, 0, 255))
  YELLOW = auto(RGB(255, 255, 0))
  CYAN = auto(RGB(0, 255, 255))
  MAGENTA = auto(RGB(255, 0, 255))
  WHITE = auto(RGB(255, 255, 255))
  BLACK = auto(RGB(0, 0, 0))

  def __str__(self) -> str:
    name = str.capitalize(self.name)
    return """%s: %s""" % (name, self.value)


if __name__ == '__main__':
  for color in Color:
    print(color)
```

The above outputs the following:

```terminal
Red: #FF0000
Green: #00FF00
Blue: #0000FF
Yellow: #FFFF00
Cyan: #00FFFF
Magenta: #FF00FF
White: #FFFFFF
Black: #000000
```

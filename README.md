[![wakatime](https://wakatime.com/badge/github/AsgerJon/WorkToy.svg)](
https://wakatime.com/badge/github/AsgerJon/WorkToy)

# WorkToy v0.99.xx

This library leverages the most advanced Python features including the
descriptor protocol and support for customizable metaclasses. The
documentation below explains these features and how **WorkToy** leverages
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
    + [```worktoy.parse.maybeType```](#worktoyparsemaybetype)

- [worktoy.desc](#worktoydesc)
  * [Background - The Python Descriptor Protocol](#background---the-python-descriptor-protocol)
    + [The ``__set_name__``method](#the-__set_name__method)
    + [The `__get__` method](#the-__get__-method)
    + [The `__set__` method](#the-__set__-method)
    + [The ``delete`` method](#the-delete-method)
    + [Descriptor Protocol Implementations](#descriptor-protocol-implementations)
  * [The `property` class](#the-property-class)
    * [The `AbstractDescriptor` class](#the-abstractdescriptor-class)
    * [The `Field` class](#the-field-class)
    * [The `AttriBox` class](#the-attribox-class)
    * [``THIS`` - Advanced ``AttriBox`` Usage](#this---advanced-attribox-usage)
    * [Using ``AttriBox`` in PySide6 - Qt for Python](#using-attribox-in-pyside6---qt-for-python)
    * [``worktoy.desc`` Conclusion](#worktoydesc-conclusion)

* [The Python metaclass - ``worktoy.meta``](#the-python-metaclass---worktoymeta)
  * [Introduction - Python is the Best](#introduction---python-is-the-best)
  * [Background - The Python Metaclass](#background---the-python-metaclass)
  * [Everything is an object!](#everything-is-an-object)
  * [Extensions of ``object``](#extensions-of-object)
  * [The Python Function](#the-python-function)
  * [The ``*`` and ``**`` operators](#the--and---operators)
  * [The Python ``lambda`` Function](#the-python-lambda-function)
  * [Class Instantiations](#class-instantiations)
  * [The Custom Class](#the-custom-class)
  * [The Custom Metaclass](#the-custom-metaclass)
  * [The Custom Namespace](#the-custom-namespace)
  * [The Python Metaclass - Conclusion](#the-python-metaclass---conclusion)
* [The ``worktoy.meta`` Module](#the-worktoymeta-module)
  * [Nomenclature](#nomenclature)
  * [Metaclass and Namespace Pattern](#metaclass-and-namespace-pattern)
  * [Function Overloading](#function-overloading)
  * [Singleton](#singleton)
  * [Summary](#summary)
* [The ``worktoy.keenum`` module](#the-worktoykeenum-module)
* [The ``worktoy.ezdata`` module](#the-worktoyezdata-module)
  * [Summary of ``worktoy.ezdata`` module](#summary-of-worktoyezdata-module)
* [The ``worktoy.text`` module](#the-worktoytext-module)
  * [``worktoy.text.stringList``](#worktoytextstringlist)
  * [``worktoy.text.monoSpace``](#worktoytextmonospace)
  * [``worktoy.text.wordWrap``](#worktoytextwordwrap)
  * [``worktoy.text.typeMsg``](#worktoytexttypemsg)
  * [``worktoy.text.joinwords``](#worktoytextjoinwords)
  * [``worktoy.parse`` module](#worktoyparse-module)

# Installation

The stable version of **WorkToy** may be installed using the following
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
the **WorkToy** library. For a more detailed explanation that includes
discussions on Python itself, please refer to the **A Deep Dive into
Python** section.

# Usage

This section explains the packages included in the **WorkToy** library in
the order they are imported.

## ```WorkToy.text```

This package provides functions for manipulating text. The functions are
very simple but widely used across **WorkToy**.

### ```WorkToy.text.stringList```

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

### ```WorkToy.text.monoSpace```

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

### ```WorkToy.text.wordWrap```

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
  bar = wordWrap(40, foo)
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

### ```WorkToy.text.typeMsg```

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

### ```WorkToy.text.joinWords```

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
  bar = joinWords(*foo)  # Each string should be a positional argument
  print(bar)
```

The above outputs the following:

```terminal
Tom, Dick and Harry
```

In summary, ```WorkToy.text``` provides the following:

- ```stringList```
- ```monoSpace```
- ```wordWrap```
- ```typeMsg```
- ```joinWords```

## ```WorkToy.parse```

This module provides a pair of ```None```-aware functions.

### ```WorkToy.parse.maybe```

This function takes any number of arguments and returns the first that is
different from ```None```. Suppose a function intends to apply VAT to a
base price with a default VAT-rate of 10 %:

```Python
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.parse import maybe

fallbackRate = 0.1


def badApplyVAT(basePrice: float, rate: float = None) -> float:
  """Bad implementation!"""
  return basePrice * (1 + (rate or fallbackRate))


def goodApplyVAT(basePrice: float, rate: float = None) -> float:
  """Good implementation"""
  if rate is None:
    return basePrice * (1 + fallbackRate)
  return basePrice * (1 + rate)


def bestApplyVAT(basePrice: float, rate: float = None) -> float:
  """Best implementation using 'maybe'. This is functionality equivalent 
  to the good implementation above, but with the added syntactic sugar."""
  return basePrice * (1 + maybe(rate, fallbackRate))


if __name__ == '__main__':
  actualRate = 0.
  print('Bad implementation: badApplyVAT(100, actualRate)')
  print('Expected: 100, Actual: %.2f' % badApplyVAT(100, actualRate))
  print('Best implementation: bestApplyVAT(100, actualRate)')
  print('Expected: 100, Actual: %.2f' % bestApplyVAT(100, actualRate))
```

The above outputs the following:

```terminal
Bad implementation: badApplyVAT(100, actualRate)
Expected: 100, Actual: 110.00
Best implementation: bestApplyVAT(100, actualRate)
Expected: 100, Actual: 100.00
```

As is obvious, the bad implementation replaced the intended rate of
```0``` with the fallback rate of ```0.1```. Good thing such a thing has
never happened in reality to any reasonably sized financial institution.
This is because ```0``` while a valid rate here, is falsy which is all
the bad implementation checks for. Instead, comparing against ```None```
does not cause falsy but valid values to be overwritten. The ```maybe```
function provides syntactic sugar for selecting only the value different
from ```None```.

### ```WorkToy.parse.maybeType```

This is identical to the ```maybe``` function, but with the added
type check, meaning that it takes first a type and then any number of
positional arguments. It then returns the first of the positional
arguments that is different from ```None``` *and* is of the given type.

```Python
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.parse import maybeType

if __name__ == '__main__':
  foo = [None, '69', dict(value=420), None, 1337, None, .80085]
  bar = maybeType(int, *foo)  # passes all elements of foo to maybeType
  print('Expected: 1337, Actual: %d' % bar)
```

The above outputs the following:

```terminal
Expected: 1337, Actual: 1337
```

In summary, the ```WorkToy.parse``` module provides the following:

- ```maybe```
- ```maybeType```

## ```WorkToy.desc```

This module provides classes implementing the descriptor protocol

### ```worktoy.desc.Field```

In situations were an attribute requires significant customization, the
```Field``` class exposes the features available in the descriptor
protocol allowing full customization. Like the builtin ```property```,
instances of ```Field``` must decorate the accessor methods explicitly
to enable. This is done by using the ```GET```, ```SET``` and ```DEL```
decorators. Unlike ```property``` however, the field instance must be
instantiated *before* it can decorate the accessor methods.

For example, consider the following class representation a complex number
using the ```Field``` class to fields ```r``` and ```t``` to represent
absolute value and angle respectively. Notice that the real and imaginary
parts are represented by instances of AttriBox, which is the subject of
the next section.

```Python
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.base import FastObject, overload
from worktoy.desc import AttriBox, Field, THIS
from worktoy.parse import maybeType


class Complex(FastObject):
  """The real and imaginary parts are implemented with AttriBox"""

  IM = AttriBox[float](0.)
  RE = AttriBox[float](0.)

  r = Field()  # same as absolute value
  t = Field()  # angle in range -pi, pi

  @overload(float, float)
  def __init__(self, x: float, y: float) -> None:
    self.RE, self.IM = x, y

  @overload(complex)
  def __init__(self, z: complex) -> None:
    self.RE, self.IM = z.real, z.imag

  @overload(THIS)
  def __init__(self, other: Self) -> None:
    self.RE, self.IM = other.RE, other.IM





```

### ```worktoy.desc.AttriBox```

This class provides a powerful implementation of the descriptor protocol
allowing for lazy instantiation while requiring only one line in the
class body. When instantiating ```AttriBox``` in the class body, the
following novel syntax is used:

```Python
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox


class Complex:
  """Complex number implementation using AttriBox"""

  RE = AttriBox[float](0.)
  IM = AttriBox[float](0.)

  def __init__(self, *args) -> None:
    if len(args) > 1:
      self.RE, self.IM = args[:2]
    elif len(args):
      self.RE = args[0]

  #  __add__, __mul__ and other arithmetic operations omitted here
```

The above implementation of the ```Complex``` class provides a real and
imaginary part as attributes. The ```AttriBox``` class is instantiated
with a field type in the brackets and the arguments to be used for
instantiating the field type. When the ```__get__``` method is first
called, that is, the attribute is accessed, the field is instantiated
using the arguments passed after the brackets.

Consider the following example where another class owns attributes
defined as instances of ```AttriBox``` whose field type is ```Complex```.

```Python
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox


class Complex:
  """Complex number implementation using AttriBox"""
  #  Same as before


class Quarternion:
  """Quarternion defined with two complex numbers as attributes. """

  z1 = AttriBox[Complex](0, 0)
  z2 = AttriBox[Complex](69, 420)
```

Attributes created this way require one line of code, but possesses the
following powerful features:

- Lazy, but still flexible instantiation.
- Strongly typed.

For a deeper dive into the even more powerful features not mentioned here,
refer to the **A Deep Dive into Python** section.

## ```WorkToy.base```

By leveraging the custom metaclass and descriptor protocol, ```WorkToy```
is able to provide two powerful and general baseclasses for general use.
Both of which support an important feature found in other programming
languages: function overloading.

To use overloading in a new class, have the class inherit from either
```BaseObject``` or ```FastObject```. The usage is quite intuitive and is
instantly recognized by copilot, for example:

```Python
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Self

from worktoy.desc import AttriBox, THIS
from worktoy.base import FastObject, overload


class Complex(FastObject):
  """Complex number implementation using AttriBox"""

  RE = AttriBox[float]()
  IM = AttriBox[float]()

  @overload(float, float)
  def __init__(self, x: float, y: float) -> None:
    self.RE, self.IM = x, y

  @overload(complex)
  def __init__(self, z: complex) -> None:
    self.RE, self.IM = z.real, z.imag

  @overload(THIS)
  def __init__(self, other: Self) -> None:
    """Note the use of 'THIS' to indicate an instance of the class we are 
    only just implementing!"""
    self.RE, self.IM = other.RE, other.IM
```

In the above implementation of the complex number, we subclass
```FastObject```, which is faster, but restricts attributes to being
instances of ```AttriBox``` and disallows dynamic attribute creation.
These restrictions allow the use of the ```__slots__``` mechanism for
attribute access. The ```BaseObject``` class is more flexible, but slower
as it does not implement ```__slots__```.

## ```WorkToy.keenum```

Provides a simple enumeration class. Please note that it does not support
inheritance. Classes must define enumerate using the ```keenum. auto```
function. This function allows instances to be associated with any
arbitrary object passed to the function. If no such object is passed,
they name of the enumeration is used instead. Please note that this
public value has only semantic meaning and is never accessed by any
internal mechanism in the enumeration class. Thus, it may be any object.

Consider the following example of enumerating colors in the context of
**Qt for Python**.

```Python
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import Field
from worktoy.keenum import auto, KeeNum


class QColor:  # Imagine this was: from pyside6.QtGui import QColor

  def __init__(self, *args, **kwargs) -> None:
    pass


class RGB(KeeNum):
  """Assigns instances of QColor as public values to the enumeration. """

  WHITE = auto(QColor(255, 255, 255))
  BLACK = auto(QColor(0, 0, 0))
  RED = auto(QColor(255, 0, 0))
  GREEN = auto(QColor(0, 255, 0))
  BLUE = auto(QColor(0, 0, 255))
```

In the above example, please imagine that QColor is from the
```pyside6``` module. Each enumeration is assigned a public value of a
```QColor``` instance. The ```auto``` function is used to associate the
instance with the enumeration. If no object is passed to the ```auto```
function, the name of the enumeration is used instead.

While this public value is entirely semantic from the perspective of the
internal logic, a subclass may implement functionality expecting the
public value of each enumeration to be of a particular type. For example:

Please note that the names of enumerations are case-insensitive!

```Python
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Self

from worktoy.parse import maybe
from worktoy.desc import Field, AttriBox, THIS
from worktoy.base import FastObject, overload
from worktoy.keenum import auto, KeeNum


class QColor(FastObject):
  """QColor from pyside6 is not here right now, may I help?"""

  R = AttriBox[int](255)
  G = AttriBox[int](255)
  B = AttriBox[int](255)

  @overload(int, int, int)
  def __init__(self, *rgb) -> None:
    self.R, self.G, self.B = rgb

  @overload(THIS)
  def __init__(self, other: Self) -> None:
    self.R, self.G, self.B = other.R, other.G, other.B

  @overload()
  def __init__(self, ) -> None:
    pass

  def red(self) -> int:
    return self.R

  def green(self) -> int:
    return self.G

  def blue(self) -> int:
    return self.B


class RGB(KeeNum):
  """Assigns instances of QColor as public values to the enumeration.
  Additionally, it requires auto to be of type QColor (the one above,
  not the real one lol). """

  r = Field()
  g = Field()
  b = Field()

  WHITE = auto(QColor(255, 255, 255))
  BLACK = auto(QColor(0, 0, 0))
  RED = auto(QColor(255, 0, 0))
  GREEN = auto(QColor(0, 255, 0))
  BLUE = auto(QColor(0, 0, 255))

  #  Further enumerations are left as an exercise to the reader

  @r.GET
  def _getRed(self) -> int:
    """Getter-function for value at red channel"""
    return self.value.red()

  @g.GET
  def _getBlue(self) -> int:
    """Getter-function for value at red channel"""
    return self.value.green()

  @b.GET
  def _getGreen(self) -> int:
    """Getter-function for value at red channel"""
    return self.value.blue()

  def __str__(self, ) -> str:
    """Returns hex representation of the color value"""
    return ('#%02x%02x%02x' % (self.r, self.g, self.b)).upper()

  def __repr__(self, ) -> str:
    """Returns code that would match this instance"""
    return """%s.%s""" % (self.__class__.__name__, self.name)


if __name__ == '__main__':
  for rgb in RGB:
    print(rgb)
```

The above outputs the following:

```terminal
RGB.WHITE as hex: #FFFFFF
RGB.BLACK as hex: #000000
RGB.RED as hex: #FF0000
RGB.GREEN as hex: #00FF00
RGB.BLUE as hex: #0000FF
```

In summary, the ```WorkToy.keenum``` module provides flexible
enumerations.

## Summary

```WorkToy``` contains the following packages:

- ```WorkToy.text```
- ```WorkToy.parse```
- ```WorkToy.desc```
- ```WorkToy.base```
- ```WorkToy.keenum```
- ```WorkToy.ezdata```

# A Deep Dive into Python

This section provides a deeper examination of the contents of **WorkToy**
and the background in **Python** itself.

## ```WorkToy.parse```: ```None```-awareness

There is a programming language out there possessing exactly one
redeeming feature: ```??``` As if this wonderful operator is asking *How
did I end up in javascript?* The unfortunately named *nullish coalescing*
operator provides awareness of the ```null``` object, which is called
```None``` in Python. For example:

```Javascript

const susVal = null;

const fallbackVal = 69420;

const midWare = (req, res, next) => {
  res['someValue'] = susVal ?? fallbackVal;
  next();
}

module.exports = midWare;
```

In the above ```susVal ?? fallbackVal``` uses ```fallbackVal``` only when
```susVal``` is ```null```. Regrettably, Python provides no such operator,
nevertheless the logic behind it still finds widespread use in Python.
Consider a function implementing a default value:

```Python
def concatLists(X: list, Y: list = []) -> list:
  """Don't do this. This is disgusting!"""
  return [*X, *Y]
```

The above function uses a mutable default argument. Never do this! Instead,
this author recommends always using ```None``` as the default value **WITHOUT
EXCEPTION!** For example:

```Python
def concatList(X: list, Y: list = None) -> list:
  """This is the way!"""
  if Y is None:
    return X
  return [*X, *Y]
```

Here, the comparison against ```None``` relies on the ```is None``` check
in a multiline conditional clause. The ```parse``` module provides a pair
of None-aware functions.

## Background - The Python Descriptor Protocol

The descriptor protocol in Python allows significant customisation of the
attribute access mechanism. To illustrate, let us implement a descriptor
class ```Integer``` which wraps integer values. Such a class is intended
to be instantiated in the class bodies of other classes.

This discussion will now continue in the docstrings found in the
implementation of this class.

```python
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any


class Integer:
  """Let us continue this discussion in the docstrings of the 'Integer'
    class.
    
    This descriptor class defines the following instance attributes:
    - __fallback_value__: If instantiated without a default value, this 
      value is used.
    - __default_value__: The default value of the descriptor instance.
    - __field_name__: The name by which the descriptor instance appears in 
      the class body.
    - __field_owner__: The class owning the descriptor instance.
    - __pvt_name__: The name of the private variable used to store the 
      value of the attribute.
    
    It also defines the following methods which each provides a docstring
    explaining their purpose and function:
    - __init__
    - __set_name__
    - __get__
    - __set__
    - __delete__  # DO NOT MISTAKE WITH __del__! 
    """

  __fallback_value__ = 0
  __default_value__ = None
  __field_name__ = None
  __field_owner__ = None

  def __init__(self, *args) -> None:
    """This constructor method accepts any number of positional arguments.
     It then implements the under used and underappreciated 'for-loop'
     ending with an 'else' clause. The code in the 'else' block runs 
     after the loop completes. The point is that the 'break' keyword also 
     applies to this block. So if 'break' is encountered, the code in the 
     'else' block does not run. To translate to natural language: 
     
     'Go through each positional argument and when you find an integer, 
     assign it to the default value. If you have not found any integer 
     after looking through each positional argument, use the fallback 
     value.'  
     
     It is the opinion of this author that the 'else' clause in a loop is
     underused and underappreciated."""
    for arg in args:
      if isinstance(arg, int):
        self.__default_value__ = arg
        break
    else:
      self.__default_value__ = self.__fallback_value__

  def __set_name__(self, owner: type, name: str) -> None:
    """This is the method that elevates the power of the descriptor 
    protocol beyond the mundane getter and setter pattern! This feature 
    was added in Python 3.6 released on December 23, 2016. Does this make it
    a recent feature? Well, Minecraft Java 1.11 had been released on 
    November 14, 2016, meaning that this feature is about the same age as 
    totems of undying, shulker boxes and the observer block.
     
    This method is invoked when the class owning the descriptor is created. 
    It informs the instance of the descriptor of its owner and the name 
    by which it appears in the class body of the owner. This means that the 
    descriptor instance is aware of its own name in the namespace of its 
    owner.  
    
    """
    self.__field_name__ = name
    self.__field_owner__ = owner
    self.__pvt_name__ = '__%s_value__' % (name,)

  def __get__(self, instance: object, owner: type) -> Any:
    """This method is called when the descriptor instance is accessed. It 
    returns the value of the attribute. If the descriptor instance is 
    accessed through the owning class, the descriptor instance itself is 
    returned. For example:
    
    class Owner:
      num = Integer(69)
    
    if __name__ == '__main__':
      owner = Owner()
      print(type(owner.num))  # <class 'int'>, the wrapped value instance
      print(type(Owner.num))  # <class 'Integer'>, the descriptor instance
    
    'owner.num' results in the following call:
    '__get__(owner, Owner)'
    
    'Owner.num' results in the following call:
    '__get__(None, Owner)'
    
    By making the above distinction, the descriptor instance object may 
    be accessed by going through the owning class. This is the most 
    common and highly recommended pattern. However, it also means that 
    ambiguity exists for the type-hint: When accessing through the 
    instance the hint should be 'int', but when accessing through the 
    class, the hint should be 'type'. For this reason, the 'Any' type is
    used here. 
    """
    if instance is None:
      return self
    if getattr(instance, self.__pvt_name__, None) is None:
      return self.__default_value__
    return getattr(instance, self.__pvt_name__)

  def __set__(self, instance: object, value: object) -> None:
    """This method is called when the attribute at the field name of the 
    descriptor instance is attempted to be set on the instance of the 
    owning class. Unlike the '__get__' method defined above, this method 
    is invoked only when the attribute is set on the instance. If set on 
    the owner, the descriptor instance itself is overwritten. This is 
    consistent with the pattern that access through the owning class 
    refers to the descriptor instance, whilst access through the owning 
    instance is managed by the descriptor class. For example:
    
    class Owner:
      num = Integer(420)
      
    if __name__ == '__main__':
      owner = Owner()
      print(owner.num)  # 420
      owner.num = 69 
      print(owner.num)  # 69
      
      print(Owner.num)  # <Integer object at 0x1EE7B00B5>
      print(type(Owner.num))  # <class 'Integer'>
      Owner.num = 69
      print(Owner.num)  # 69
      print(type(Owner.num))  # <class 'int'>
      
      owner.num = 69  # This results in the following call:
      '__set__(owner, 69)'
      
      Owner.num = 69  # This results in the following call:
      'type(Owner).__setattr__(Owner, 'num', 69)'
    """
    setattr(instance, self.__pvt_name__, value)

  def __delete__(self, instance: object) -> None:
    """This method is called when the attribute is attempted to be 
    deleted. DO NOT MISTAKE WITH '__del__'! The '__del__' method is 
    called when the instance is destroyed. Both of these are outside the 
    scope of this discussion."""
    delattr(instance, self.__pvt_name__)
```

In summary, the ``Integer`` class defined above provides integer valued
attributes to other classes. The accessor functions implements only
trivial functionality here, but serves to illustrate the possibilities
for customization.

### Pythons ``property`` class

Python does provide a built-in class for creating descriptors: the
``property`` class. This class allows the use of a decorator to define
getter, setter and deleter functions for an attribute. Alternatively, the
``property`` may be instantiated in the class body with the getter, setter
and deleter functions as arguments. The following class has attributes
``name`` and ``number`` both instances of ``property`` implemented with
the decorator and the constructor respectively.

```python
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations


class OwningClass:
  """This class uses 'property' to implement the 'name' and 'number' 
  attributes. """

  __fallback_number__ = 0
  __fallback_name__ = 'Unnamed'
  __inner_number__ = None
  __inner_name__ = None

  def __init__(self, *args, **kwargs) -> None:
    self.__inner_number__ = kwargs.get('number', None)
    self.__inner_name__ = kwargs.get('name', None)
    for arg in args:
      if isinstance(arg, int) and self.__inner_number__ is None:
        self.__inner_number__ = arg
      elif isinstance(arg, str) and self.__inner_name__ is None:
        self.__inner_name__ = arg

  @property
  def name(self) -> str:
    """Name property"""
    if self.__inner_name__ is None:
      return self.__fallback_name__
    return self.__inner_name__

  @name.setter
  def name(self, value: str) -> None:
    """Name setter"""
    self.__inner_name__ = value

  @name.deleter
  def name(self) -> None:
    """Name deleter"""
    del self.__inner_name__

  def _getNumber(self, ) -> int:
    """Number getter"""
    if self.__inner_number__ is None:
      return self.__fallback_number__
    return self.__inner_number__

  def _setNumber(self, value: int) -> None:
    """Number setter"""
    self.__inner_number__ = value

  def _delNumber(self) -> None:
    """Number deleter"""
    del self.__inner_number__

  number = property(_getNumber, _setNumber, _delNumber, doc='Number')
```

Before proceeding further, let us briefly discuss the ``@decorator``
syntax.

#### The ``@decorator`` syntax

When using the keywords: ``def``, ``async def`` and ``class``, we
begin a compound statement that creates a new object at the name
following the keyword. When such a compound statement is 'decorated' it
means that the created object is passed to the decorating function upon
creation and the object returned by the decorator is assigned to the name
instead.

A decorator could return an object wrapping the decorated object to
augment its behaviour. Alternatively, it could record the decorated
function for a particular purpose and return the object exactly as
received. Or even a combination of the two.

Let us now examine a few decorators beginning with a simple notifier:

```python
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Callable


def notify(callMeMaybe: Callable) -> Callable:
  """This decorator notifies the creation of the received object by 
  printing its name. """
  print(callMeMaybe.__name__)
  return callMeMaybe


@notify
class SomeClass:
  """This is just some class. """

  @notify
  def someMethod(self, ) -> None:
    """This is just some method. """

    @notify
    def nestedMethod() -> None:
      """It even has a nested method!"""


if __name__ == '__main__':
  print('Entry point!')
  someInstance = SomeClass()
```

The above code will output the following:

```terminal
someMethod
SomeClass
Entry point!
```

The above may surprise some readers anticipating the output to begin with
the 'Entry point!' message. However, the class body is executed
immediately even before the ``if __name__ == '__main__':`` block is
entered. During this execution, the ``someMethod`` function is created
and passed to the ``notify`` decorator. Upon completion of the class body
execution, the newly created class object is passed to the ``notify``
decorator. Both happen prior to the normal entry point. But what about
the nested method? The ``someMethod`` creates it when called, not when
created. In the example, the class body creates the ``someMethod``, but
nobody actually invokes it. Thus, the nested method remains uncreated.

### ``Field``, like ``property`` but better

Having introduced the Python descriptor protocol and the ``property``
class, we shall now introduce the ``Field`` class provided by the
``worktoy.desc`` module. This class aims at providing the same
functionality as the ``property`` class. Class owning instances of
``Field`` can heavily customize the attribute access mechanism at a
particular name. In fact, the ``Field`` descriptor provides no actual
functionality itself, but simply allows the owning class to define each
of the accessor functions. If multiple classes are to implement multiple
attributes with similar behaviour using the ``Field`` class, it will
introduce significant boilerplate code. To implement general attribute
behaviour requires a different approach. Foreshadowing...

The following is a truncated version of the ``Field`` class provided by
the ``worktoy.desc`` module. This documentation will continue in the
docstrings below.

```python
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Callable, Never


class Field:
  """Welcome back to the docstrings, where our discussion continues! 
  Please note that the 'Field' class found in 'worktoy.desc' is 
  significantly more complicated than the code below, which simply 
  illustrates the concept. """

  #  Accessor functions for the accessors of the attribute. 
  __getter_function__ = None
  __setter_function__ = None
  __deleter_function__ = None

  def _getGetter(self, ) -> Callable:
    """This method returns the getter function. """
    return self.__getter_function__

  def _setGetter(self, value: Callable) -> None:
    """This method sets the getter function. """
    self.__getter_function__ = value

  def _getSetter(self, ) -> Callable:
    """This method returns the setter function. """
    return self.__setter_function__

  def _setSetter(self, value: Callable) -> None:
    """This method sets the setter function. """
    self.__setter_function__ = value

  def _getDeleter(self, ) -> Callable:
    """This method returns the deleter function. """
    return self.__deleter_function__

  def _setDeleter(self, value: Callable) -> None:
    """This method sets the deleter function. """
    self.__deleter_function__ = value

  #  So much boilerplate code!

  __field_name__ = None
  __field_owner__ = None

  def __set_name__(self, owner: type, name: str) -> None:
    """This is the same as in the previous 'Integer' class example."""
    self.__field_name__ = name
    self.__field_owner__ = owner

  def _getPrivateName(self) -> str:
    """Parses a private name from the field name. """
    return '__%s_value__' % (self.__field_name__,)

  #  We are finally ready to implement the descriptor protocol!

  def __get__(self, instance: object, owner: type) -> object:
    """This method is called when the descriptor instance is accessed. """
    if instance is None:
      return self
    pvtName = self._getPrivateName()
    getFunc = self._getGetter()  # Existence check omitted
    return getFunc(instance)

  def __set__(self, instance: object, value: object) -> None:
    """This method is called when the attribute at the field name of the 
    descriptor instance is attempted to be set on the instance of the 
    owning class. """
    pvtName = self._getPrivateName()
    setFunc = self._getSetter()  # Existence check omitted
    setFunc(instance, value)

  def __delete__(self, instance: object) -> Never:
    """Outside the scope of this discussion."""
    e = """This example does not implement attribute deletion!"""
    raise TypeError(e)

  #  Public names for the accessor decorators:

  def GET(self, func: Callable) -> Callable:
    """This decorator marks the function as the getter function. """
    self._setGetter(func)
    return func

  def SET(self, func: Callable) -> Callable:
    """This decorator marks the function as the setter function. """
    self._setSetter(func)
    return func

  def DEL(self, func: Callable) -> Callable:
    """This decorator marks the function as the deleter function. """
    self._setDeleter(func)
    return func
```

To illustrate the use of the ``Field`` class, we will implement a class
encapsulation of a complex number having the real and imaginary parts as
separate attributes. The example will illustrate decorators, the
``Field`` class and the dangers of boilerplate code.

```python
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import Field
from worktoy.parse import maybe  # None-aware filter


#  The 'maybe' function provides None-awareness. It is similar to the 
#  null-coalescing operator in javascript.
#  maybe(a, b) returns 'a' if 'a' is not None, otherwise it returns 'b'.
#  Same as: a ?? b in javascript.
#  Likely, the only redeeming feature of javascript.


class Complex:
  """More boilerplate??"""

  __real_fallback__ = 0.
  __imag_fallback__ = 0.
  __real_part__ = None
  __imag_part__ = None

  RE = Field()
  IM = Field()

  @RE.GET
  def _getReal(self) -> float:
    """Getter function for the real part."""
    return maybe(self.__real_part__, self.__real_fallback__)

  @RE.SET
  def _setReal(self, value: float) -> None:
    """Setter function for the real part."""
    self.__real_part__ = value

  @IM.GET
  def _getImag(self) -> float:
    """Getter function for the imaginary part."""
    return maybe(self.__imag_part__, self.__imag_fallback__)

  @IM.SET
  def _setImag(self, value: float) -> None:
    """Setter function for the imaginary part."""
    self.__imag_part__ = value

  def __init__(self, *args) -> None:
    x, y = None, None

    for arg in args:
      if isinstance(arg, int):
        arg = float(arg)
      if isinstance(arg, float) and x is None:
        x = arg
      elif isinstance(arg, float) and y is None:
        y = arg
        break
      elif isinstance(arg, complex):
        x, y = arg.real, arg.imag
        break
    else:
      x, y = 69., 420.
    self.RE, self.IM = x, y

  def __add__(self, other: object) -> Complex:
    """This method is left as an exercise to the reader along with: 
     __sub__
     __mul__
     __truediv__
     __pow__
     __abs__
     Any 'try-hard' reader may also implement the 'i' and 'r' versions."""
```

The ``Complex`` class leverages the ``Field`` implementation of the
descriptor protocol to provide attributes for the real and imaginary parts
of a complex number. Below is usage example:

```python
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

if __name__ == '__main__':
  z1 = Complex(69, 420)
  z2 = Complex(1, 2)
  z2.RE = 3
  z2.IM = 4
  z3 = z1 + z2
  print(z3.RE, z3.IM)
  z4 = 1337 * z1  # Hopefully, a try-hard reader implemented this!
  print(z4.RE, z4.IM)
```

The above code will output the following:

```terminal
70.0 422.0
93003.0 56180.0
```

In summary, both the ``Field`` and ``property`` classes provide a way to
customize the attribute access mechanism for each class. This comes at
the cost of significant boilerplate code for attributes that are frequently
behaving in the same way. In fact, most attributes might reasonably be
expected to behave as the ``Field`` class does. The ``worktoy.desc``
module provides a class for this exact purpose: the ``AttriBox`` class.

## The `AttriBox` class

Where ``Field`` relies on the owning class itself to specify the accessor
functions, the ``AttriBox`` class provides an attribute of a specified
class. This class is not instantiated until an instance of the owning
class calls the ``__get__`` method. Only then will the inner object of
the specified class be created. The inner object is then placed on a
private variable belonging to the owning instance. When the ``__get__``
is next called the inner object at the private variable is returned. When
instantiating the ``AttriBox`` class, the following syntactic sugar
should be used: ``fieldName = AttriBox[FieldClass](*args, **kwargs)``.
The arguments placed in the parentheses after the brackets are those used
to instantiate the ``FieldClass`` given in the brackets.

Below is an example of a class using the ``AttriBox`` class to implement
a ``Circle`` class. It uses the ``Point`` class defined above to manage
the center of the circle. Notice how the ``Point`` class itself is wrapped
in an ``AttriBox`` instance. The ``area`` attribute is defined using the
``Field`` class and illustrates the use of the ``Field`` class to expose
a value as an attribute.

```python
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox, Field

pi = 3.1415926535897932


class Point:
  """This class provides a point in 2D space. """
  x = AttriBox[float](0)
  y = AttriBox[float](0)

  def __init__(self, *args) -> None:
    for arg in args:
      if isinstance(arg, int):
        arg = float(arg)
      if isinstance(arg, float) and self.x is None:
        self.x = arg
      elif isinstance(arg, float) and self.y is None:
        self.y = arg
        break
    else:
      self.x, self.y = 0, 0


class Circle:
  """This class uses the 'AttriBox' descriptor to manage the radius and
  center, and it also illustrates a use case for the 'Field' class."""

  radius = AttriBox[float](0)
  center = AttriBox[Point](0, 0)
  area = Field()

  @area.GET
  def _getArea(self) -> float:
    return pi * self.radius ** 2

  def __str__(self) -> str:
    msg = """Circle centered at: (%.3f, %.3f), with radius: %.3f"""
    return msg % (self.center.x, self.center.y, self.radius)

  def __init__(self, *args) -> None:
    """This constructor is left as an exercise to the reader."""


if __name__ == '__main__':
  circle = Circle(69, 420, 1337)
  print(circle)
  circle.radius = 80085
  print(circle)
```

Running the code above will output the following:

```terminal
Circle centered at: (69.000, 420.000), with radius: 4.000
Circle centered at: (69.000, 420.000), with radius: 1.000
```

## ``THIS`` - Advanced ``AttriBox`` Usage

So far the ``AttriBox`` instantiation has used the following syntax:

```python
"""Basic instantiation of the 'AttriBox' class."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox


class Owner:
  """Basic instantiation of the 'AttriBox' class."""

  floatBox = AttriBox[float](69.)
  intBox = AttriBox[int](420)
```

In the above example, the ``AttriBox`` instantiates **before** the owning
class is even created. However, suppose the boxed class require the
owning instance to be passed to the constructor. This presents a
challenge as the ``AttriBox`` instance exists **before** the owning class
event exists. Enter the ``THIS`` object!

**TL;DR**

```python
"""Advanced instantiation of the 'AttriBox' class."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox, THIS


class WhoDat:
  """Boxed class aware of its owning instance."""

  __the_boss__ = None

  def __init__(self, who: object) -> None:
    self.__the_boss__ = who

  def getBoss(self) -> object:
    return self.__the_boss__

  def __str__(self) -> str:
    return 'Mah boss: %s' % (self.getBoss(),)


class Boss:
  """Owning class."""

  whoDat = AttriBox[WhoDat](THIS)
  name = AttriBox[str]()

  def __init__(self, name: str) -> None:
    self.name = name

  def __str__(self) -> str:
    return 'Mr. %s' % (self.name,)


if __name__ == '__main__':
  boss = Boss('Guido')
  print(boss.whoDat)
  print(boss.whoDat.getBoss() is boss)
```

The above produces:

```Shell
Mah boss: Mr. Guido
True
```

When the ``AttriBox.__get__`` is called on the ``whoData`` attribute, the
``WhoDat`` class instantiates, but the ``AttriBox`` instance replaces
``THIS`` with the owning instance. This allows the ``WhoDat`` instance to
be aware of its owning instance. Likewise, ``TYPE`` would be replaced by
the owning class, ``BOX`` with the ``AttriBox`` instance and ``ATTR`` with
the ``AttriBox`` class (or subclass) itself.

As have been demonstrated and explained, the ``worktoy.desc`` module
provides helpful, powerful and flexible implementations of the descriptor
protocol. The ``Field`` allows classes to customize attribute access
behaviour in significant detail. The ``AttriBox`` class provides a way to
set as attribute any class on another class in a single line. As
mentioned briefly, the class contained by the ``AttriBox`` instance is
not instantiated until an instance of the owning class calls the
``__get__`` method.

## Using ``AttriBox`` in PySide6 - Qt for Python

The PySide6 library provides Python bindings for the Qt framework. Despite
involving bindings to a C++ library, the code itself remains Python and
not C++, thank the LORD. Nevertheless, certain errors do not have a
Pythonic representation. The ``AttriBox`` clas was envisioned to provide
a convenient way to develop PySide6 applications, whilst remaining
oblivious to terms like "Segmentation Fault".

``AttriBox`` provides two features of particularly significance for
developing in PySide6: lazy instantiation and the ``THIS`` object.

### Lazy Instantiation

This refers to the fact that the ``AttriBox`` is instantiated before its
inner class is. When an instance of the owning class calls the ``__get__``
method, the inner class is instantiated. Not before. This seamlessly
satisfies the unintuitive-adjacent requirement that the first ``QObject``
to be instantiated is the singular ``QCoreApplication`` instance.

### ``THIS`` parent

When instantiating any ``QObject`` or subclass hereof, the constructor
may be passed another ``QObject`` instance. This instance is then set as
the parent of the newly instantiated object. However, when placing an
instance of ``AttriBox`` in the class body with a ``QObject`` inside, the
parent class does not actually exist yet. (Unintuitive-adjacent).
Fortunately, ``THIS`` provides a temporary placeholder for the owning
instance, such that when the class inside the ``AttriBox`` is
instantiated, the ``THIS`` object is replaced by the owning instance. For
example:

```python
"""Using 'AttriBox' and 'THIS' in PySide6."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox, THIS
from PySide6.QtWidgets import QMainWindow, QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import QObject


class MainWindow(QMainWindow):
  """This subclass of QMainWindow provides the main application window. """

  baseWidget = AttriBox[QWidget](THIS)
  baseLayout = AttriBox[QVBoxLayout]()  # QLayout should NOT have parent
  welcomeLabel = AttriBox[QLabel]('Welcome to AttriBox!', THIS, )

  def __init__(self, *args, ) -> None:
    for arg in args:
      if isinstance(arg, QObject):
        QMainWindow.__init__(self, arg)
    else:
      QMainWindow.__init__(self)

  def initUi(self) -> None:
    """This method sets up the user interface"""
    self.setWindowTitle("Welcome to WorkToy!")
    self.welcomeLabel.setText("""Welcome to WorkToy!""")
    self.baseLayout.addWidget(self.welcomeLabel)
    self.baseWidget.setLayout(self.baseLayout)
    #  If passing 'THIS' to the layout box, it would set the window 
    #  instance at the layout instead of the widget instance. 
    self.setCentralWidget(self.baseWidget)

  def show(self) -> None:
    """This reimplementation calls 'initUi' before calling the parent 
    implementation"""
    self.initUi()
    QMainWindow.show(self)
```

## ``worktoy.desc`` Conclusion

The Python descriptor protocol provides powerful customization of
attribute behaviour, but at the cost of considerable amounts of
boilerplate code. The functionality may be seen as a feature of the class
owning the attribute or as a feature of the attribute class. The
``worktoy.desc`` implements a class for each. The ``Field`` class allows
the owning class to define the attribute behaviour through the use of
decorators. The ``AttriBox`` class provides an attribute of a specified
class on a single line. Both are subclasses of the ``AbstractDescriptor``
class which provides the core functionality of the descriptor protocol.

The ``worktoy.desc`` module exposes the powerful descriptor protocol. In
the following we shall see how ``worktoy.meta`` exposes an even more
powerful Python feature: the metaclass. The remaining modules in the
``worktoy`` module combine these to achieve even greater power!

# The Python metaclass - ``worktoy.meta``

## Introduction - Python is the Best

Python is the best programming language. Why? Because you feel happy when
coding in Python. Your experience while programming depends on the syntax
not on the underlying technology. Python made syntax king.

Python is freedom. This author might reject out of hand any contribution
lacking type hints, but the Python interpreter will not. Thus, Python types
are the best. Because they are voluntary.

Just like Python blesses voluntary efforts such as type-hints, it also
permits things like:

```python
#  NO RIGHTS RESERVED
try:
  crime()
except BaseException:  # Don't show your parole officer
  pass
```

While the above code is a sign of a severe personality disorder, Python
permits it. It is said that Python is named after UK comedy efforts, but this
author suspects a deeper meaning in the name being that of a snake:
Granting free will. This freedom allows good code to be genuinely clear and
intentional, reflecting a developer's honest effort to make the code
understandable for others, rather than merely satisfying compiler demands.

There may be readers crying, having to wipe saliva of their screens
having screamed about speed, GIL, memory usage, dynamic typing and so on.
Objections relating to the permissive nature of Python miss the point:
You don't have to. You can do better. You are free to choose. This leaves
objections about performance, but again you are free to implement
something faster, for example by using a just in time compiler such as
provided by the [Numba](https://numba.pydata.org/) library as needed. As
for memory uses, this author is presently using PyCharm, a Java based
application, with an allowance of 8192MB of memory. Remaining objections
are either outdated or soon to be outdated as is the case for the GIL,
which is scheduled for removal in Python 3.14.

If you are still not convinced Python is the best, but are still reading, it
signifies that you have an open mind. A personality trait indicating that you
will love the subject of the following discussion.

## Background - The Python Metaclass

It is likely that you have never heard of the Python metaclass. In fact,
you may have quite negative associations with the word 'meta' on account of
recent smooth-brained conduct of several multi-billion dollar companies.

Many concepts have implementations in most programming languages, but
'metaclass' is exclusive to Python. No other programming language has
anything like it. Java reflections? No, no, no. Rust macros? Not even
close! C++ templates? Get it out of here!

Understanding the Python metaclass does require some background. In the
following sections, we will examine:

- **The Python object**
- **Object Extensions** (classes)
- **The Python Function**
- **The ``*`` and ``**`` operators**
- **The Python ``lambda`` Function**  (anonymous functions)
- **Class Instantiations**
- **The Custom Class**
- **The Custom Metaclass**
- **The Custom Namespace**

## Everything is an object!

Python operates on one fundamental idea: Everything is an object.
Everything. All numbers, all strings, all functions, all modules and
everything that you can reference. Even ``object`` itself is an object.
This means that everything supports a core set of attributes and methods
defined on the core ``object`` type.

## Extensions of ``object``

With everything being an object, it is necessary to extend the
functionalities in the core ``object`` type to create new types,
hereinafter classes. This allows objects to share the base ``object``,
while having additional functionalities depending on their class. Python
provides a number of special classes listed below:

- **``object``** - The base class for all classes. This class provides
  the most basic functionalities.
- **``int``** - Extension for integers. The python interpreter uses
  heavily optimized C code to handle integers. This is the case for
  several classes on this list.
- **``float``** - Extension for floating point numbers. This class
  provides a number of methods for manipulating floating point numbers.
- **``list``** - Extension for lists of objects of dynamic size allowing
  members to be of any type. As the amount of data increases, the greater
  the performance penalty for the significant convenience.
- **``tuple``** - Extension for tuples of objects of fixed size. This
  class is similar to the list class, but the size is fixed. This means
  that the tuple is immutable. While this is inflexible, it does allow
  instances to be used as keys in mappings.
- **``dict``** - Extension for mappings. Objects of this class map keys
  to values. Keys be of a hashable type, meaning that ``object`` itself
  is not sufficient. The hashables on this list are: ``int``, ``float``,
  ``str`` and ``tuple``.
- **``set``** - Extension for sets of objects. This class provides a
  number of methods for manipulating sets. The set class is optimized for
  membership testing.
- **``frozenset``** - Provides an immutable version of ``set`` allowing
  it to be used as a key in mappings.
- **``str``** - Extension for strings. This class provides a number of
  methods for manipulating strings. The ``worktoy.text`` module expands
  upon some of these.

To reiterate, everything is an object. Each object belongs to the
``object`` class but may additionally belong to a class that extends the
``object`` class. For example: ``7`` is an object. It is an instance of
``object`` by being an instance of ``int`` which extends ``object``.
Classes are responsible for defining the instantiation of instances
belonging to them. Generally speaking, classes may be instantiated by
calling the class object treating it like a function. Classes may accept
or even require arguments when instantiated.

Before proceeding, we need to talk about functions. Python provides two
builtin extensions of ``object`` that provide standalone objects that
implement functions: ``function`` and ``lambda``. Both of these have
quite unique instantiation syntax and does not follow the conventions we
shall see later in this discussion.

## Defining a ``function``

Python allows the following syntax for creating a function. Please note
that all functions are still objects, and all functions created with the
syntax below belong to the same class ``function``. Unfortunately, this
class cannot be referred to directly. Which is super weird. Anyway, to
create a function, use the following syntax:

```python
def multiplication(a: int, b: int) -> int:
  """This function returns the product of two integers."""
  return a * b
```

### RANT

The above function implements multiplication. It also provides the
optional features: type hints and a docstring. The interpreter completely
ignores these, but they are very helpful for humans. It is the opinion of
this author that omitting type hints and docstrings is acceptable only
when running a quick test. If anyone except you or God will ever read
your code, it must have type hints and docstrings!

### END OF RANT

Below is the syntax that invokes the function:

```python
result = multiplication(7, 8)  # result is 56
```

In the function definition, the positional arguments were named ``a`` and
``b``. In the above invocation, the positional arguments were given
directly. Alternatively, they might have been given as keyword arguments:

```python
result = multiplication(a=7, b=8)  # result is 56
tluser = multiplication(b=8, a=7)  # result is 56
```

When keyword arguments are used instead of positional arguments, the
order is irrelevant, but names are required.

## The star ``*`` and double star ``**`` operators

Suppose the function were to be invoked with the numbers from a
list: ``numbers = [7, 8]``, then we might invoke the ``multiplication``
function as follows:

```python
result = multiplication(numbers[0], numbers[1])  # result is 56
```

Imagine the function took more than two arguments. The above syntax would
still work, but would be cumbersome. Enter the star ``*`` operator:

```python
result = multiplication(*numbers)  # result is 56
```

Wherever multiple positional arguments are expected, and we have a list
or a tuple, the star operator unpacks it. This syntax will seem confusing,
but it is very powerful and is used extensively in Python. It is also
orders of magnitude more readable than the equivalent in C++ or Java.

### RANT

This rant is left as an exercise to the reader

### END OF RANT

Besides function calls, the star operator conveniently concatenates lists
and tuples. Suppose we have two lists: ``a = [1, 2]`` and ``b = [3, 4]``
we may concatenate them in several ways:

```python
a = [1, 2]
b = [3, 4]
ab = [a[0], a[1], b[0], b[1]]  # Method 1: ab is [1, 2, 3, 4]
ab = a + b  # Method 2: ab is [1, 2, 3, 4]
ab = [*a, *b]  # Method 3: ab is [1, 2, 3, 4]
a.extend(b)  # Method 4 modifies list 'a' in place. 
a = [1, 2, 3, 4]  # a is extended by b

```

Obviously, don't use the first method. The one relevant for the present
discussion is the third, but the second and fourth have merit as well,
but will not be used here. Finally, list comprehension is quite powerful
as well but is the subject for a different discussion.

## The double star ``**`` operator

The single star is to lists and tuples as the double star is to
dictionaries. Suppose we have a dictionary: ``data = {'a': 1, 'b': 2}``
then we may invoke the ``multiplication`` function as follows:

```python   
data = {'a': 1, 'b': 2}
result = multiplication(**data)  # result is 2
```

Like the star operator, the double star operator can be used to
concatenate two dictionaries. Suppose we have two dictionaries:
``A = {'a': 1, 'b': 2}`` and ``B = {'c': 3, 'd': 4}``. These may be
combined in several ways:

```python
A = {'a': 1, 'b': 2}
B = {'c': 3, 'd': 4}
#  Method 1
AB = {**A, **B}  # AB is {'a': 1, 'b': 2, 'c': 3, 'd': 4}
#  Method 2
AB = A | B
#  Method 3 updates A in place
A |= B
A = {'a': 1, 'b': 2}  # Resetting A
#  Method 4 updates A in place
A.update(B)
```

As before, the first method is the most relevant for the present
discussion. Unlike the example with lists, there is not really a method
that is bad like the first method with lists.

In conclusion, the single and double star operators provide powerful
unpacking of iterables and mappings respectively. Each have reasonable
alternatives, but it is the opinion of this author that the star
operators are preferred as they are unique to this use. The plus and
pipe operators are used for addition and bitwise OR respectively. When
the user first sees the plus or the pipe, they cannot immediately infer
that the code is unpacking the operands. Not before having identified the
types of the operands. In contrast, the star in front of an object
without space immediately says unpacking.

## The famous function signature: ``def someFunc(*args, **kwargs)``

Anyone having browsed through Python documentation or code may have
marvelled at the function signature: ``def someFunc(*args, **kwargs)``.
The signature means that the function accepts any number of positional
arguments as well as any number of keyword arguments. This allows one
function to accept multiple different argument signatures. While this may
be convenient, the ubiquitous use of this pattern is likely motivated by
the absense of function overloading in native Python. **(Foreshadowing...)**

## The ``lambda`` function

Before getting back to class instantiation, we will round off this
discussion of functions with the ``lambda`` function. The ``lambda``
function is basically the anonymous function. The syntax of it is
``lambda arguments: expression``. Whatever the expression on the right
hand side of the colon evaluates to is returned by the function. The
``lambda`` function allows inline function definition which is much more
condensed than the regular function definition as defined above. This
allows it to solve certain problems in one line, for example:

```python
fb = lambda n: ('' if n % 3 else 'Fizz') + ('' if n % 5 else 'Buzz') or n
fb = lambda n: ('Fizz' * n % 3 < 1) + ('Buzz' * n % 5 < 1) or n
```

Besides flexing, the ``lambda`` function is useful when working with
certain fields of mathematics, requiring implementation of many functions
that fit on one line. Below is an example of a series of functions
implementing Taylor series expansions. While type-hints should always be
used, the single line nature of the ``lambda`` function makes it
impractical to include type-hints inside the function definition. This
author suggests instead the inclusion of type hints separately, for
example for the ``fizzBuzz`` function above:

```python
from typing import Callable

fb: Callable[[int], str]
```

The above signifies that ``fb`` is a callable that takes an integer and
returns a string. Lambda functions will not fit type hints, so this seems
a reasonably helpful alternative.

```python
"""Lambda function implementations of common mathematical functions."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Callable, TypeAlias

#  int2int is a type alias for a mapping from int to int
int2int: TypeAlias = Callable[[int], int]
factorial: int2int
#  The following functions take other functions as arguments
recursiveSum: Callable[[int2int, int], int]
taylorTerm: Callable[[float, int2int], float]
#  The following maps term order to term value
expTerm: int2int
sinTerm: int2int
cosTerm: int2int
sinhTerm: int2int
coshTerm: int2int
#  Combining the above allows implementation of the following functions. 
#  The float is the independent variable and the int is the number of 
#  terms to be used in the Taylor expansion. 
exp: Callable[[float, int], float]
sin: Callable[[float, int], float]
cos: Callable[[float, int], float]
sinh: Callable[[float, int], float]
cosh: Callable[[float, int], float]
#  Below are the actual implementations using type hints as indicated above.
factorial = lambda n: factorial(n - 1) * n if n else 1
recursiveSum = lambda F, n: F(n) + (recursiveSum(F, n - 1) if n else 0)
taylorTerm = lambda x, t: (lambda n: t(n) * x ** n / factorial(n))
expTerm = lambda n: 1
sinTerm = lambda n: (-1 if ((n - 1) % 4) else 1) if n % 2 else 0
cosTerm = lambda n: sinTerm(n + 1)
sinhTerm = lambda n: 1 if n % 2 else 0
coshTerm = lambda n: sinhTerm(n + 1)
exp = lambda x, n: recursiveSum(taylorTerm(x, expTerm), n)
sin = lambda x, n: recursiveSum(taylorTerm(x, sinTerm), n)
cos = lambda x, n: recursiveSum(taylorTerm(x, cosTerm), n)
sinh = lambda x, n: recursiveSum(taylorTerm(x, sinhTerm), n)
cosh = lambda x, n: recursiveSum(taylorTerm(x, coshTerm), n)
```

The above collection of functions implement recursive lambda functions to
calculate function values of common mathematical functions including:

- ``exp``: The exponential function.
- ``sin``: The sine function.
- ``cos``: The cosine function.
- ``sinh``: The hyperbolic sine function.
- ``cosh``: The hyperbolic cosine function.

The lambda functions implement Taylor-Maclaurin series expansions at a
given number of terms and then begin by calculating the last term
adding the previous term to it recursively, until the 0th term is reached.
This implementation demonstrates the power of the recursive lambda
function and is not at all flexing.

## Instantiation of classes

Since this discussion includes class instantiations, the previous section
discussing functions will be quite relevant. We left the discussion of
builtin Python classes having listed common ones. Generally speaking,
Python classes have a general syntax for instantiation except for those
listed. Below is the instantiation of the builtin classes.

- **object**: ``obj = object()`` - This creates an object. Not
  particularly useful but does show the general syntax.
- **int**: ``number = 69`` - This creates an integer.
- **float**: ``number = 420.0`` - This creates a float.
- **str**: ``message = 'Hello World!'`` - This creates a string.
- **list**: ``data = [1, 2, 3]`` - This creates a list.
- **tuple**: ``data = (1, 2, 3)`` - This creates a tuple.
- **?**: ``what = (1337)`` - What does this create? Well, you might
  imagine that this creates a tuple, but it does not. The interpreter
  first removes the redundant parentheses and then the evaluation makes
  it an integer. To create a single element tuple, you must add the
  trailing comma: ``what = (1337,)``. This applies to one element tuples,
  as the comma separating the elements of a multi-element tuple
  sufficiently informs the interpreter that this is a tuple. The empty
  tuple requires no commas: ``empty = ()``.
- **set**: ``data = {1, 2, 3}`` - This creates a set.
- **dict**: ``data = {'key': 'value'}`` - This creates a dictionary. If
  the keys are strings, the general syntax may be of greater convenience:
  ``data = dict(key='value')``. Not requiring quotes around the keys.
  Although this syntax does not support non-string keys.
- **?**: ``data = {}`` - What does this create? Does it create an empty
  set or an empty dictionary. This author is not actually aware, and
  recommends instead ``set()`` or ``dict()`` respectively when creating
  empty sets or dictionaries.

Except for ``list`` and ``tuple``, the general class instantiation syntax
may be applied as seen below:

- **int**: ``number = int(69)``
- **float**: ``number = float(420.0)``
- **str**: ``message = str('Hello World!')``
- **dict**: ``data = dict(key='value')`` - This syntax is quite
  reasonable, but is limited to keys of string type.

Now let's have a look at what happens if we try to instantiate ``tuple``,
``list``, ``set`` or ``frozenset`` using the general syntax:

- **list**: ``data = list(1, 2, 3)`` - NOPE! This does not create the
  list predicted by common sense: ``data = [1, 2, 3]``. Instead, we are
  met by the following error message: "TypeError: list expected at most 1
  argument, got 3". Instead, we must use the following syntax:
  ``data = list((1, 2, 3))`` or ``data = list([1, 2, 3])``. Now the
  attentive reader may begin to object, as one of the above require a list
  to already be defined and the other requires the tuple to be defined.
  Let's see how one might instantiate a tuple directly:
- **tuple**: ``data = tuple(1, 2, 3)`` - NOPE! This does not work either!
  We receive the exact same error message as before. Instead, we must use
  one of the following: ``data = tuple((1, 2, 3))``
  or ``data = tuple([1, 2, 3])``. The logically sensitive readers now see
  a significant inconsistency in the syntax: One cannot in fact
  instantiate a tuple nor a list directly without having a list or tuple
  already created. This author suggests that the following syntax should
  be accepted: ``data = smartTuple(1, 2, 3)`` and even:
  ``data = smartList(1, 2, 3)``. Perhaps this author is just being
  pedantic. The existing syntax is not a problem, and it's not like the
  suggested instantiation syntax is used anywhere else in Python.
- **set**: ``data = set(1, 2, 3,)`` This is correct syntax. So this works,
  but the suggested ``smartList`` and ``smartTuple`` functions does not, OK
  sure, makes sense...
- **frozenset**: ``data = frozenset([69, 420])`` - This is correct syntax.

Let us have another look at the instantiations of ``dict`` and of ``set``,
but not ``list`` and ``tuple``.

```python
def newDict(**kwargs) -> dict:
  """This function creates a new dictionary having the key value pairs 
  given by the keyword arguments. """
  return dict(**kwargs)  # Unpacking the keyword arguments creates the dict.


def newSet(*args) -> set:
  """This function creates a new set having the elements given by the 
  positional arguments. """
  return set(args)  # Unpacking the positional arguments creates the set.


def newList(*args) -> list:
  """As long as we don't use the word 'list', we can actually instantiate 
  a list in a reasonable way."""
  return [*args, ]  # Unpacking the positional arguments creates the list.


def newTuple(*args) -> tuple:
  """Same as for list, but remember the hanging comma!"""
  return (*args,)  # Unpacking the positional arguments creates the tuple.
```

## Custom classes

In the previous section, we examined functions and builtin classes. To
reiterate, in the context of this discussion a class is an extension of
``object`` allowing objects to belong to different classes implementing
different extensions of ``object``. This raises a question: What
extension of ``object`` contains ``object`` extensions? If ``7`` is an
instance of the ``int`` extension of ``object``, of what extension is
``int`` and instance. The answer is the ``type``. This extension of
``object`` provides all extensions of ``object``. This implies the
surprising that ``type`` is an instance of itself.

The introduction of the ``type`` class allows us to make the following
insightful statement:

``7`` is to ``int`` as ``int`` is to ``type``. This means that ``type``
is responsible for instantiating new classes. A few readers may now begin
to see where this is going, but before we get there, let us examine how
``type`` creates a new class.

```python
"""Sample class."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox


class PlanePoint:
  """Class representing a point in the plane """

  x = AttriBox[float](0)
  y = AttriBox[float](0)

  def __init__(self, *args, **kwargs) -> None:
    """Constructor omitted..."""

  def magnitude(self) -> float:
    """This method returns the magnitude of the point. """
    return (self.x ** 2 + self.y ** 2) ** 0.5


if __name__ == '__main__':
  P = PlanePoint(69, 420)
```

After the import statement, which is not the subject of the present
discussion, the first line of code encountered by the interpreter is the
``class PlanePoint:``. The line omits some default values shown here:
``class PlanePoint(object, metaclass=type)``. What the interpreter does
next is entirely up to the metaclass. Whatever object the metaclass
returns will be place at the name ``PlanePoint``. We will now look at
what the ``type`` metaclass, which is the default, does when it creates a
class, but keep mind that the metaclass my do whatever it wants.

- **name**: ``PlanePoint`` is recorded as the name of the class about to
  be created.
- **bases**: A tuple of the base classes is created. The ``object`` does
  not actually arrive in this tuple and the ``type`` provides implicitly.

Please note that it is possible to pass keyword arguments similarly to
the metaclass=type, but this is beyond the scope of the present
discussion. With the name and the bases, the metaclass now creates a
namespace object. The ``type`` simply uses an empty dictionary. Then the
interpreter goes through the class body line by line look for assignments,
function definitions and even nested classes. Basically every statement
in the class body that assigns a value to a key and for each such pair
the ``__setitem__`` method is called on the namespace object. The
implication of this is that where the value to be assigned is the return
value of a function, then that function is called during the class
creation process. This means that in the ``PlanePoint`` class above, the
instances of ``AttriBox`` are created before the class object is created.
When the interpreter finishes, it calls the ``__new__`` method on the
metaclass and passes to it: the name, the bases, the namespace and any
keyword arguments initially passed to class creation. The interpreter
then waits for the metaclass to return the class object. When this
happens all the objects that implement ``__set_name__`` has the method
called informing the descriptor instances that their owner has been
created. Finally, the interpreter applies the ``__init__`` method of the
metaclass on the newly created class.

In summary:

- **Setting up class creation** The interpreter records the name of the
  class to be created, the base classes, the keyword arguments and which
  metaclass is responsible for creating the class.
- **Namespace creation** The items collected are passed to the
  ``__prepare__`` method on the metaclass:
  ``namespace = type.__prepare__(name, bases, **kwargs)``
- **Class Body Execution** The interpreter goes through the class body
  line by line and assigns the values to the namespace object:
  ``namespace['x'] = AttriBox[float](0)  # Creates the AttriBox object``
- **Class Object Creation** The namespace object is passed to the
  ``__new__`` method on the metaclass:
  ``cls = type.__new__(type, name, bases, namespace, **kwargs)``
- **Descriptor Class Notification** The objects implementing the descriptor
  protocol are notified that the class object has been created:
  ``AttriBox[float].__set_name__(PlanePoint, 'x')``
- **``type.__init__``** The metaclass is called with the class object:
  ``type.__init__(cls, name, bases, namespace, **kwargs)`` Although on
  ``type`` the ``__init__`` method is a noop.

An impractical alternative to the above syntax is to create the new class
inline: ``PlanePoint = type('PlanePoint', (object,), {})``. Although,
this line has an empty dictionary where the namespace should have been.

## The Custom Metaclass

This brings us to the actual subject of this discussion: The custom
metaclass. Because every step mentioned above may be customized by
subclassing ``type``. Doing so takes away every limitation. The line
discussed before:

```python
"""The syntax can create anything you want!"""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations


class AnyWayUWantIt(metaclass=MyMeta):
  """The syntax can create anything you want!"""
```

This line can create anything. A class for example, but anything. It can
create a string, it can return ``None``, it can create a new function,
any object possible may be created here.

This present discussion is about creating new classes, but readers are
encouraged to experiment.

As mentioned, the ``type`` object provides a very helpful class creation
process. What it does is defined in the heavily optimized C code of the
Python interpreter. This cannot be inspected as Python code. For the
purposes of this discussion, we will now create a custom metaclass that
does the same as the ``type`` metaclass, but exposed as Python code.

```python
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations


class MetaType(type):
  """This custom metaclass illustrates the class creation process as it 
  is done by the 'type' metaclass. """

  @classmethod
  def __prepare__(mcls, name: str, bases: tuple, **kwargs) -> dict:
    """This method creates the namespace object, which for 'type' is 
    merely an empty dictionary. """
    return dict()

  def __new__(cls, name: str, bases: tuple, namespace: dict, **kw) -> type:
    """This method creates the class object. There is not much to see 
    here, as the 'type' metaclass does most of the work. This is normal 
    in custom metaclasses where this method, if implemented, performs 
    some tasks, creates the class object, possibly does some more tasks, 
    before returning the class object. """
    cls = type.__new__(type, name, bases, namespace)
    return cls

  def __init__(cls, name: str, bases: tuple, namespace: dict, **kw) -> None:
    """A custom metaclass may implement this method. Doing so allows 
    further initialization after the '__set_name__' calls have finished. """
    pass

  def __call__(cls, *args, **kwargs) -> object:
    """This method is called when the class object is called. The 
    expected behaviour even from custom metaclasses, is for it to create 
    a new instance of the class object. Please note, that generally 
    speaking, custom classes are free to implement their own 
    instantiation in the form of the '__new__' and '__init__' methods. If 
    a custom metaclass does not intend to adhere to these, then when 
    encountering a class body that tries to implement them, the namespace 
    object should raise an error. Do not allow classes derived from the 
    custom metaclass to implement a function that you do not intend to 
    actually use. """
    self = cls.__new__(cls, *args, **kwargs)
    if isinstance(self, cls):
      self.__init__(*args, **kwargs)
    return self

  def __instance_check__(cls, instance: object) -> bool:
    """Whenever the 'isinstance' function is called, this method on the 
    metaclass is responsible for determine if the instance should be 
    regarded an instance of the class object. """
    otherCls = type(instance)
    if cls is otherCls:
      return True
    for item in otherCls.__mro__:
      if item is cls:
        return True
    return False

  def __subclass_check__(cls, subclass: type) -> bool:
    """Similar to the above instance check method, this method is 
    responsible for deciding of the subclass provided should be regarded 
    as a subclass of the class object. """
    if cls is subclass:
      return True
    for item in subclass.__mro__:
      if item is cls:
        return True
    return False
```

Since the ``type`` metaclass is heavily optimized in the C code of the
Python interpreter, the above implementation is for illustrative purposes
only. It shows what methods a custom metaclass may customize to achieve a
particular behaviour.

## The Custom Namespace

The custom namespace object must implement ``__getitem__`` and
``__setitem__``. Additionally, it must satisfy the key error preservation
and the ``type.__new__`` method must receive a namespace of ``dict``-type.
This is elaborated below:

### ``KeyError`` preservation

When a dictionary is accessed with a key that does not exist, a
``KeyError`` is raised. The interpreter relies on this behaviour to
handle lines in the class body that are not directly assignments
correctly. This is a particularly important requirement because failing
to raise the expected ``KeyError`` will affect only classes that happen
to include a non-assignment line. Below is a list of known situations
that causes the issue:

- **Decorators**: Unless the decorator is a function defined earlier in
  the class body as an instance method able to receive a callable at the
  ``self`` argument, the decorator will cause the issue described. Please
  note that a static method would be able to receive a callable at the
  first position, but the static method decorator itself would cause the
  issue even sooner.
- **Function calls**: If a function not defined previously in the class
  body is called during the class body without being assigned to a name,
  the error will occur.

The issue raises an error message that will not bring attention to the
namespace object. Further, classes will frequently work fine, if they
happen to not include any of the above non-assignments. In summary:
failing to raise the expected error must be avoided at all costs, as it
will cause undefined behaviour without any indication as to the to cause.

### The ``type.__new__`` expects a namespace of ``dict``-type

After the class body is executed the namespace object is passed to the
``__new__`` method on the metaclass. If the metaclass is intended to
create a new class object, the metaclass must eventually call the
``__new__`` method on the parent ``type`` class. The ``type.__new__``
method must receive a namespace object that is a subclass of ``dict``. It
is only at this stage the requirement is enforced. Thus, it is possible
to use a custom namespace object that is not a subclass of ``dict``, but
then it is necessary to implement functionality in the ``__new__`` method
on the metaclass such that a ``dict`` is passed to the ``type.__new__``
call.

## Applications of Custom Namespace

During class body execution the namespace object is passed the key value
pairs encountered. When using the empty dictionary as the namespace,
information is lost when a key receives multiple values as only the most
recently set value is retained. A custom namespace might collect all
values set at each name thus preserving all information. This application
is implemented in the ``worktoy.meta`` module. Beyond the scope of this
module is the potential for the namespace object to dynamically change
during the class body execution. This potential is not explored here, but
readers are encouraged to experiment.

Preserving multiple values on the same key can only be provided for by a
custom namespace. An obvious use case would be function overloading. This
brings up an important distinction: A class implementing function
overloading is in some ways the exact same class as before. Only the
overloaded methods are different. Providing a custom namespace does not
actually result in classes that exhibit different behaviour. Achieving
this requires customization of the metaclass itself beyond the
``__prepare__`` method.

# The ``worktoy.meta`` module

We have discussed class creation by use of ``type``, we have illustrated
what methods might be customized. In particular the custom namespace
returned by the ``__prepare__`` method. This brings us to the
``worktoy.meta`` module. Our discussion will proceed with an examination
of the contents.

## Nomenclature

Below is a list of terms used in the ``worktoy.meta`` module:

- **``cls``** - A newly created class object
- **``self``** - A newly created object that is an instance of the newly
  created class.
- **``mcls``** - The metaclass creating the new class.
- **``namespace``** - This is where the class body is stored during class
  creation.

## Metaclass and Namespace Pattern

The ``worktoy.meta`` module implements a pattern where the metaclass is
responsible for defining the functionality of the class, while the
namespace object is responsible for collecting items from the class body
execution. Rather than simply passing on the namespace object it receives,
the namespace object class is expected to implement a method called
``compile``. The metaclass uses the ``dict`` returned by the ``compile``
when it calls the ``type.__new__`` method.

This pattern is based on the separation of responsibilities: The
namespace object class is responsible for processing the contents of the
class body. The metaclass is responsible for defining the functionality
of the class itself.

## Function Overloading

The ``worktoy.meta`` module provides a decorator factory called
``overload`` used to mark an overloaded method with a type signature. The
``Dispatcher`` class contains a dictionary of functions keyed by their
type signatures. When calling an instance of this class, the types of the
arguments received determine what function to call. The ``BaseNamespace``
class is a custom namespace object that collects overloaded functions and
replaces each such name with a relevant instance of the ``Dispatcher``. The
``BaseMetaclass`` class is a custom metaclass using the ``BaseNamespace``
class as the namespace object. Finally, the ``BaseObject`` class derives
from the ``BaseMetaclass`` and implements function overloading.

## Singleton

Singleton classes are characterized by the fact that they are allowed
only one instance. The ``worktoy.meta`` provides ``Singleton`` class
derived from a custom metaclass. Subclasses of it are singletons. When
calling the class object of a subclass of ``Singleton`` the single
instance of the class is returned. If the subclass implements
``__init__`` then it is called on the single instance. This allows
dynamic behaviour of singletons. If this is not desired, the singleton
subclass should provide functionality preventing the ``__init__`` method
from running more than once.

## Summary

The ``worktoy.meta`` module provides base classes and a pattern for
custom metaclass creation and uses them to implement function overloading
in the ``BaseObject`` class. Additionally, the module provides a
``Singleton`` class for creating singletons, which is based on a custom
metaclass derived from the module. Other parts of the ``worktoy`` module
makes use of the ``worktoy.meta`` in their implementation. This includes
the ``KeeNum`` enumeration module and the ``ezdata`` module.

# The ``worktoy.keenum`` module

The ``worktoy.keenum`` module provides the ``KeeNum`` enumeration class.
This class makes use of the ``worktoy.meta`` module to create the
enumeration class. This discussion will demonstrate how to create
enumerations with this class. Every enumeration class must be indicated
in the class body using the ``worktoy.keenum.auto`` function. Each such
instances may provide a public value by passing it to the ``auto``
function. Please note however, that the public value is not used for any
purpose by the module. The ``KeeNum`` implements a hidden value that it
uses internally.

```python
"""Enumeration of weekdays using KeeNum."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeNum, auto


class Weekday(KeeNum):
  """Enumeration of weekdays."""
  MONDAY = auto()
  TUESDAY = auto()
  WEDNESDAY = auto()
  THURSDAY = auto()
  FRIDAY = auto()
  SATURDAY = auto()
  SUNDAY = auto()
```

In the documentation of the ``worktoy.desc`` module, the **PySide6**
framework were mentioned as a use case for the ``AttriBox`` class. Below
is a use case for the ``KeeNum`` class in the **PySide6** framework. In
fact, the ``Alignment`` class shown below is a truncated version
of a enumeration class included in the ``ezside`` module currently under
development.

```python
"""Enumeration of alignment using KeeNum. """
# AGPL-3.0 license
# Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Qt
from worktoy.keenum import KeeNum, auto


class Alignment(KeeNum):
  """Enumeration of alignment."""
  CENTER = auto()

  LEFT = auto()
  RIGHT = auto()
  TOP = auto()
  BOTTOM = auto()

  TOP_LEFT = auto()
  TOP_RIGHT = auto()
  BOTTOM_RIGHT = auto()
  BOTTOM_LEFT = auto()
``` 

The ``KeeNum`` class might also have been used to enumerate the different
accessor functions, which might have been useful in the ``worktoy.desc``.

```python
"""Enumeration of accessor functions using KeeNum."""
# AGPL-3.0 license
# Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeNum, auto


class Accessor(KeeNum):
  """Enumeration of accessor functions."""
  GET = auto(getattr)
  SET = auto(setattr)
  DEL = auto(delattr)
```

In the above, the ``Accessor`` class enumerates the accessor functions
``getattr``, ``setattr`` and ``delattr``. But the ``auto`` function can
also be used to decorate enumerations, which makes their public values
functions.

```python
"""Implementation of math functions using KeeNum"""
# AGPL-3.0 license
# Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Callable, Any
from worktoy.keenum import KeeNum, auto


class Trig(KeeNum):
  """Enumeration of trigonometric functions."""

  @classmethod
  def factorial(cls, n: int) -> int:
    """This function returns the factorial of the argument."""
    if n:
      return n * cls.factorial(n - 1)
    return 1

  @classmethod
  def recursiveSum(cls, callMeMaybe: Callable, n: int) -> float:
    """This function returns the sum of the function F from 0 to n."""
    if n:
      return callMeMaybe(n) + cls.recursiveSum(callMeMaybe, n - 1)
    return callMeMaybe(n)

  @classmethod
  def taylorTerm(cls, x: float, callMeMaybe: Callable) -> Callable:
    """This function returns a function that calculates the nth term of a
    Taylor series expansion."""

    def polynomial(n: int) -> float:
      return callMeMaybe(n) * x ** n / cls.factorial(n)

    return polynomial

  @auto
  def SIN(self, x: float) -> float:
    """This method returns the sine of the argument."""
    term = lambda n: [0, 1, 0, -1][n % 4]
    return self.recursiveSum(self.taylorTerm(x, term), 17)

  @auto
  def COS(self, x: float) -> float:
    """This method returns the cosine of the argument."""
    term = lambda n: [1, 0, -1, 0][n % 4]
    return self.recursiveSum(self.taylorTerm(x, term), 17)

  @auto
  def SINH(self, x: float) -> float:
    """This method returns the hyperbolic sine of the argument."""
    term = lambda n: n % 2
    return self.recursiveSum(self.taylorTerm(x, term), 16)

  @auto
  def COSH(self, x: float) -> float:
    """This method returns the hyperbolic cosine of the argument."""
    term = lambda n: (n + 1) % 2
    return self.recursiveSum(self.taylorTerm(x, term), 16)

  def __call__(self, *args, **kwargs) -> Any:
    """Calls are passed on to the public value"""
    return self.value(self, *args, **kwargs)
```

# The ``worktoy.ezdata`` module

The ``worktoy.ezdata`` module provides the ``EZData`` class, which
provides a dataclass based on the ``AttriBox`` class. This is achieved by
leveraging the custom metaclass provided by the ``worktoy.meta`` module.
The main convenience of the ``EZData`` is the auto generated ``__init__``
method that will populate fields with values given as positional
arguments or keyword arguments. The keys to the keyword arguments are the
field names.

Below is an example of the ``EZData`` class in use:

```python
"""Dataclass for a point in the plane using EZData."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy._WORK_IN_PROGRESS.ezdata import EZData
from worktoy.desc import AttriBox


class PlanePoint(EZData):
  """Dataclass representing a point in the plane."""
  x = AttriBox[float](0)
  y = AttriBox[float](0)

  def __str__(self, ) -> str:
    """String representation"""
    return """(%.3f, %.3f)""" % (self.x, self.y)


if __name__ == '__main__':
  P = PlanePoint(69, 420)
  print(P)
  P.x = 1337
  print(P)
  P.y = 80085  # Copilot suggested this for reals, lol
  print(P)
```

## Summary of ``worktoy.ezdata`` module

The ``EZData`` class supports fields with ``AttriBox`` instances. As
explained in the documentation of the ``worktoy.desc`` module, the
``AttriBox`` can use any class as the inner class. Thus, subclasses of
``EZData`` may use any number of fields of any class.

# ``worktoy.text`` module

The ``worktoy.text`` module provides a number of functions implementing
text formatting as listed below:

- ``stringList``: This function allows creating a list of strings from a
  single string with separated values. The separator symbol may be
  provided at keyword argument ``separator``, but defaults to ``','``.
  Strings in the returned lists are stripped meaning that spaces are
  removed from the beginning and end of each string.
- ``monoSpace``: This function fixes the frustrating reality of managing
  longer strings in Python. Splitting a string over multiple lines
  provides only one good option for long strings and that is by using
  triple quotes. This option is great except for the fact that it
  preserves line breaks verbatim. The ``monoSpace`` function receives a
  string and returns it with all continuous whitespace replaced by a
  single space. Additionally, strings may specify explicitly where line
  breaks and tabs should occur by include ``'<br>'`` and ``'<tab>'``
  respectively. Once the initial space replacement is done, the function
  replaces the explicit line breaks and tabs with the appropriate symbol.
- ``wordWrap``: This function receives an int specifying the maximum line
  length and a string. The function returns the string with line breaks
  inserted at the appropriate places. The function does not break words
  in the middle, but instead moves the entire word to the next line. The
  function also removes any leading or trailing whitespace.
- ``typeMsg``: This function composes the message to be raised with a
  ``TypeError`` exception when an ``object`` named ``name`` did not
  belong to the expected class ``cls``.
- ``joinWords``: This function receives a list of words which it
  concatenates into a single string, separated by commas except for the
  final two words which are separated by the word 'and'.

Below are examples of each of the above

## ``worktoy.text.stringList``

```python
"""Example of the 'stringList' function."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations
from worktoy.text import stringList

if __name__ == '__main__':
  baseString = """69, 420, 1337, 80085"""
  baseList = stringList(baseString)
  for item in baseList:
    print(item)

```

## ``worktoy.text.monoSpace``

```python
"""Example of the 'monoSpace' function."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.text import monoSpace

if __name__ == '__main__':
  baseString = """This is a string that is too long to fit on one line. 
    It is so long that it must be split over multiple lines. This is 
    frustrating because it is difficult to manage long strings in Python. 
    This is a problem that is solved by the 'monoSpace' function."""
  print(baseString.count('\n'))
  oneLine = monoSpace(baseString)
  print(oneLine.count('\n'))
```

## ``worktoy.text.wordWrap``

```python
"""Example of the 'wordWrap' function."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.text import wordWrap

if __name__ == '__main__':
  baseString = """This is a string that is too long to fit on one line. 
    It is so long that it must be split over multiple lines. This is 
    frustrating because it is difficult to manage long strings in Python. 
    This is a problem that is solved by the 'wordWrap' function."""
  wrapped = wordWrap(40, baseString)
  print(baseString.count('\n'))
  print(len(wrapped))
  print('\n'.join(wrapped))
```

## ``worktoy.text.typeMsg``

```python
"""Example of the 'typeMsg' function."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.text import typeMsg

if __name__ == '__main__':
  susObject = 69 + 0j
  susName = 'susObject'
  expectedClass = float
  e = typeMsg(susName, susObject, expectedClass)
  print(e)
```

## ``worktoy.text.joinWords``

```python
"""Example of the 'joinWords' function."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.text import joinWords

if __name__ == '__main__':
  words = ['one', 'two', 'three', 'four', 'five']
  print(joinWords(words))
```

# ``worktoy.parse`` module

This module provides two ``None``-aware functions:

- ``maybe``: This functions returns the first positional argument it
  received that is different from ``None``.
- ``maybeType``: Same as ``maybe`` but ignoring arguments that are not of
  the expected type given as the first positional argument.

```python
"""Example of the 'maybe' and 'maybeType' functions."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.parse import maybe, maybeType

someFalse = [0, '', dict(), set(), list(), 0j, .0, ]

if __name__ == '__main__':
  for item in someFalse:
    print(maybe(None, None, item, ))  # item from 'someFalse'
  print(maybeType(int, None, *someFalse))  # 0
  print(maybeType(str, None, *someFalse))  # ''
  print(maybeType(dict, None, *someFalse))  # {}
  print(maybeType(set, None, *someFalse))  # set()
  print(maybeType(list, None, *someFalse))  # []
  print(maybeType(complex, None, *someFalse))  # 0j
  print(maybeType(float, None, *someFalse))  # 0.0

```

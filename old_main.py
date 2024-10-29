"""Main Tester Script"""
#  AGPL-3.0 license
#  Copyright (c) 2023-2024 Asger Jon Vistisen
from __future__ import annotations

import os
import sys
from typing import Self

from worktoy.desc import AttriBox, Field, THIS
from worktoy._WORK_IN_PROGRESS.ezdata import EZData
from worktoy.base import BaseObject, overload, FastObject
from worktoy.keenum import auto, KeeNum
from worktoy.meta import CallMeMaybe
from worktoy.parse import maybe, maybeType
from worktoy.text import wordWrap, typeMsg, joinWords
from yolo import yolo, runTests


def tester00() -> int:
  """Hello World!"""
  stuff = ['hello world!', os, sys, frozenset]
  for item in stuff:
    print(item)
  return 0


class Slotted(EZData):
  """EZ complex number"""

  RE = AttriBox[float](0.0)
  IM = AttriBox[float](0.0)


class Complex(BaseObject):
  """Normal implementation"""

  RE = AttriBox[float](0.0)
  IM = AttriBox[float](0.0)

  @overload(float, float)
  def __init__(self, realPart: float, imagPart: float) -> None:
    self.RE = realPart
    self.IM = imagPart

  @overload(complex)
  def __init__(self, z: complex) -> None:
    self.RE = z.real
    self.IM = z.imag

  @overload(float, )
  def __init__(self, realPart: float) -> None:
    self.__init__(realPart, 0.0)

  @overload()
  def __init__(self) -> None:
    self.__init__(0.0, 0.0)


def tester01() -> int:
  """Testing memory usage."""
  print('Slotted:', sys.getsizeof(Slotted(69, 420)))
  print('Complex:', sys.getsizeof(Complex(69, 420)))
  return 0


def tester02() -> int:
  """Testing speed."""
  from time import perf_counter_ns

  start = perf_counter_ns()
  for _ in range(10 ** 6):
    Slotted(69, 420)
  print('Slotted:', perf_counter_ns() - start)

  start = perf_counter_ns()
  for _ in range(10 ** 6):
    Complex(69, 420)
  print('Complex:', perf_counter_ns() - start)
  return 0


def tester03() -> int:
  """LMAO"""
  print(['lmao', *[None, ] * 3])
  return 0


def tester04() -> int:
  """Testing wordWrap"""
  foo = """This is a long string that needs to be wrapped. It is 
  important that the wrapping is done correctly. Otherwise, the text 
  will not be readable. """
  bar = wordWrap(40, foo)
  for line in bar:
    print(line)
  else:
    return 0


def tester05() -> int:
  """Testing typeMsg"""

  def foo(bar: int) -> None:
    if not isinstance(bar, int):
      e = typeMsg('bar', bar, int)
      raise TypeError(e)
    print(bar)

  if __name__ == '__main__':
    susBar = 'sixty-nine'
    try:
      foo(susBar)
    except TypeError as typeError:
      errorMsg = str(typeError)  # Let's wrap this string at 50 characters
      wrapped = wordWrap(50, errorMsg)  # We apply 'str.join' to the list
      msg = '\n'.join(wrapped)
      print(msg)
    return 0


def tester06() -> int:
  """Testing joinWords"""

  foo = ['Tom', 'Dick', 'Harry']
  bar = joinWords(*foo)  # Each string should be a positional argument
  print(bar)
  return 0


def tester07() -> int:
  """Testing maybe"""

  fallbackRate = 0.1

  def badApplyVAT(basePrice: float, rate: float = None) -> float:
    """Bad implementation!"""
    return basePrice * (1 + (rate or fallbackRate))

  def bestApplyVAT(basePrice: float, rate: float = None) -> float:
    """Best implementation using 'maybe'. This is functionality equivalent
    to the good implementation above, but with the added syntactic sugar."""
    return basePrice * (1 + maybe(rate, fallbackRate))

  actualRate = 0.
  print('Bad implementation: badApplyVAT(100, actualRate)')
  print('Expected: 100, Actual: %.2f' % badApplyVAT(100, actualRate))
  print('Best implementation: bestApplyVAT(100, actualRate)')
  print('Expected: 100, Actual: %.2f' % bestApplyVAT(100, actualRate))
  return 0


def tester08() -> int:
  """maybeType test"""
  foo = [None, '69', dict(value=420), None, 1337, None, 80085]
  bar = maybeType(int, *foo)  # passes all elements of foo to maybeType
  print('Expected: 1337, Actual: %d' % bar)
  return 0


def tester09() -> int:
  """LOL"""

  def trolling(x: complex) -> complex:
    """LMAO"""
    if isinstance(x, int):
      x = float(x) + 0j
    elif isinstance(x, float):
      x += 0j
    out = x ** 4
    try:
      out = x ** out
    except OverflowError:
      out = float('inf') + float('inf') * 0j
    if out.real != float('inf'):
      try:
        out = x ** out
      except OverflowError:
        out = float('inf') + float('inf') * 0j
    lol = 'x**(x**(x**4)) for x=%.3f+%.3f*I: %.3f+%.3f*I'
    print(lol % (x.real, x.imag, out.real, out.imag))
    return out

  def lmao(z: complex) -> complex:
    if isinstance(z, int):
      z = float(z)
    if isinstance(z, float):
      z += 0j
    out = z ** z
    lol = 'x**(x**(x**4)) for x=%.3f+%.3f*I: %.3f+%.3f*I'
    print(lol % (z.real, z.imag, out.real, out.imag))
    return out

  e = 2.71828182845904523536028747135266249775724709369995
  pi = 3.14159265358979323846264338327950288419716939937510
  gamma = 0.57721566490153286060651209008240243104215933593992

  def D(func: CallMeMaybe, ) -> CallMeMaybe:
    """Diffs"""

    def d(z: complex) -> complex:
      """Diff"""
      h = 1e-6 * (1 + 1j)
      return (func(z + h) - func(z)) / h

    newName = """d(%s)/dz""" % func.__name__
    setattr(d, '__name__', newName)

    return d

  def testFunc(func: CallMeMaybe, independent: complex) -> complex:
    out = func(independent)
    fName = """%s(%s)""" % (func.__name__, independent)
    res = """%s = %.3f+%.3f*I""" % (fName, out.real, out.imag)
    print(res)
    return out

  def square(z: complex) -> complex:
    return z * z

  testFunc(D(square), 1 + 1j)

  return 0


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


def tester10() -> int:
  """Testing colors"""
  for rgb in RGB:
    print('%s as hex: %s' % (repr(rgb), rgb))
  return 0


def tester11() -> int:
  """Testing maybeType"""

  foo = ['lol', '69', 420, 80085.1337]
  print(maybeType(int, *foo))
  try:
    print(maybeType(dict, *foo))
  except TypeError as typeError:
    print(typeError)
  return 0


class Label:
  """This class demonstrates the use of the 'THIS' object in instances
   AttriBox. """

  __base_object__ = None

  def __init__(self, base: object) -> None:
    """The assumption is that the given base object implements
    '__contains__'. """
    self.__base_object__ = base

  def __call__(self, *args, **kwargs) -> str:
    """This example method returns the string representation of the
    base object. """
    return str(self.__base_object__)


class Point:
  """A point in 2D space"""

  x = AttriBox[int](0)
  y = AttriBox[int](0)
  label = AttriBox[Label](THIS)

  def __init__(self, *args) -> None:
    intArgs = [arg for arg in args if isinstance(arg, int)]
    _x, _y = [*intArgs, None, None][:2]
    if _x is not None:
      self.x = _x
    if _y is not None:
      self.y = _y

  def __str__(self, ) -> str:
    return """Point: (%d, %d)""" % (self.x, self.y)


def tester12() -> int:
  """Testing the 'THIS' object in AttriBox instances. """

  point = Point(69, 420)
  print(point.label())
  if point.label() == str(point):
    return 1
  return 0


class Point:
  """A point in 2D space"""

  x = AttriBox[int](0)
  y = AttriBox[int](0)

  def __init__(self, x: int = None, y: int = None) -> None:
    self.x = maybe(x, 0)
    self.y = maybe(y, 0)
    print("""Created: %s""" % str(self))

  def __str__(self, ) -> str:
    return """Point: (%d, %d)""" % (self.x, self.y)


class Circle:
  """A circle in 2D space"""

  center = AttriBox[Point](69, 420)
  radius = AttriBox[float](1.337)

  def __str__(self, ) -> str:
    x0, y0, r = self.center.x, self.center.y, self.radius
    return """Circle: (x-%d)^2+(y-%d)^2=%.3f^2""" % (x0, y0, r)


def tester13() -> int:
  """Testing the 'THIS' object in AttriBox instances. """
  circle = Circle()
  P = circle.center
  Q = circle.center
  if P is Q:
    return 0
  return 1


class Owner:
  """A class that uses THIS to pass itself to the attribute"""

  def __init__(self, name: str) -> None:
    self.name = name

  def __str__(self) -> str:
    return f"Owner: {self.name}"


class Dependent:
  """A class that gets initialized with an instance of Owner"""

  def __init__(self, composition: object) -> None:
    owner = getattr(composition, 'owner', None)
    if owner is None:
      raise ValueError
    self.owner = owner

  def __str__(self) -> str:
    return f"Dependent of {self.owner}"


class Composition:
  """Composition class demonstrating use of THIS with AttriBox"""

  owner = AttriBox[Owner]('John Doe')
  dependent = AttriBox[Dependent](THIS)

  def __init__(self) -> None:
    pass


def tester14() -> int:
  """Testing the 'THIS' object in AttriBox instances. """
  composition = Composition()
  print(composition.dependent)
  return 0


class Point:
  """A point in 2D space"""

  x = AttriBox[int](0)
  y = AttriBox[int](0)

  def __init__(self, x: int = None, y: int = None) -> None:
    self.x = maybe(x, 0)
    self.y = maybe(y, 0)
    print("""Created: %s""" % str(self))

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
    return """Circle spanning %.3f from %s""" % (self.radius, self.center)


def tester15() -> int:
  """Testing set before get"""

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
    return 1
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
    return 1
  return 0


if __name__ == '__main__':
  yolo(runTests, tester15)

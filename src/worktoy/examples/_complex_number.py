"""
ComplexNumber demonstrates the use of the function overloading system and
the 'AttriBox' and 'Field' descriptors to create an encapsulation of
complex numbers.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.utilities.mathematics import atan2, cos, sin
from worktoy.mcls import BaseObject
from worktoy.desc import AttriBox, Field
from worktoy.dispatch import overload
from worktoy.core.sentinels import THIS

if TYPE_CHECKING:
  from typing import Self  # For type hinting in the class methods


class ComplexNumber(BaseObject):
  """
  Function overloading requires customization of the 'type' object
  itself. 'worktoy' provides 'BaseObject' which is derived from the
  'BaseMeta' class which implements the necessary methods for
  overloading.
  """

  REAL = AttriBox[float](0.0)  # Yes, really. AttriBox[TYPE](DEFAULT)
  IMAG = AttriBox[float](0.0)  # But linters may indicate warnings

  ABS = Field()  # Field is quite similar to property
  ARG = Field()  # Requiring accessor methods to be explicitly decorated.

  #  Constructor methods

  @overload(float, float)
  @overload(float, int)
  @overload(int, float)
  @overload(int, int)
  def __init__(self, realPart: float, imagPart: float) -> None:
    """
    This constructor is overloaded with any combination of int and float.
    Since the overload decorator returns the function object without
    changes, as many overloads as needed can be added.
    """
    self.REAL = float(realPart)
    self.IMAG = float(imagPart)

  @overload(complex)  # Instantiating from a complex number instead
  def __init__(self, complexNumber: complex) -> None:
    """
    To instantiate from a complex number, a different function
    implementation is necessary.
    """
    self.REAL = complexNumber.real
    self.IMAG = complexNumber.imag

  @overload(THIS)  # THIS?
  def __init__(self, other: Self) -> None:
    """
    But what if you wanted to instantiate the class from another instance
    of the class? The moment this function object is created, the owning
    class itself does not actually exist yet. 'worktoy' provides the
    special token object 'THIS' to indicate the class yet to be created.
    """
    self.REAL = other.REAL
    self.IMAG = other.IMAG

  @overload()  # No arguments
  def __init__(self, **kwargs) -> None:
    """
    This constructor is called when no positional arguments are given. The
    positional arguments determine which constructor is called. The above
    constructors do not support keyword arguments, but this one does.
    """
    if 'real' in kwargs:
      self.REAL = kwargs['real']
    if 'imag' in kwargs:
      self.IMAG = kwargs['imag']

  #  Virtual accessor methods
  @ABS.GET
  def _getAbs(self) -> float:
    """
    The @ABS.GET decorator specifies that this method is the getter
    for the ABS property. When the ABS property is accessed through an
    instance of the class, this method is called.
    """
    return abs(self)  # Yes, we implement __abs__ further down

  @ABS.SET
  def _setAbs(self, value: float) -> None:
    """
    But how does one 'set' a virtual attribute? Well, however one
    wants! In this case, we scale the number to the new absolute value.
    """
    if not self:  # Yes, __bool__ is implemented further down
      raise ZeroDivisionError
    scale = value / abs(self)
    self.REAL *= scale
    self.IMAG *= scale

  @ARG.GET
  def _getArg(self) -> float:
    """
    The ARG property is the argument of the complex number. The @ARG.GET
    decorator specifies this method as getter.
    """
    return atan2(self.IMAG, self.REAL)  # With math.atan2

  @ARG.SET
  def _setArg(self, value: float) -> None:
    """
    The @ARG.SET decorator specifies this method as setter for the ARG
    property. The argument is set by rotating the complex number to the
    new angle.
    """
    if not self:
      raise ZeroDivisionError
    r = abs(self)
    self.REAL = r * cos(value)
    self.IMAG = r * sin(value)

  #  Bonus dunder methods as promised

  def __abs__(self, ) -> float:
    """
    The __abs__ method is called when the built-in abs() function is
    called on an instance of the class. It returns the absolute value
    of the complex number.
    """
    return (self.REAL ** 2 + self.IMAG ** 2) ** 0.5

  def __bool__(self, ) -> bool:
    """
    The __bool__ method is called when the built-in bool() function is
    called on an instance of the class. It returns True if the complex
    number is not zero, and False otherwise.
    """
    return True if self.REAL ** 2 + self.IMAG ** 2 > 1e-12 else False

  def __complex__(self, ) -> complex:
    """
    The __complex__ method is called when the built-in complex() function
    is called on an instance of the class. It returns the complex number
    as a complex object.
    """
    return self.REAL + self.IMAG * 1j

  def __str__(self, ) -> str:
    """
    This returns a human-readable string representation of the complex
    number.
    """
    if not self:
      return '0'
    if self.IMAG and self.REAL:
      if self.IMAG < 0:
        return """%.3f - %.3fJ""" % (self.REAL, abs(self.IMAG))
      return """%.3f + %.3fJ""" % (self.REAL, abs(self.IMAG))
    if self.IMAG:
      if self.IMAG < 0:
        return """-%.3fJ""" % abs(self.IMAG)
      return """%.3fJ""" % abs(self.IMAG)
    return """%.3f""" % self.REAL

  def __repr__(self, ) -> str:
    """
    The string returned by this method should ideally be a valid Python
    expression that recreates the 'self' object when passed to 'eval()'.
    """
    clsName = type(self).__name__  # Get the class name
    x, y = self.REAL, self.IMAG  # Get the real and imaginary parts
    return """%s(%s, %s)""" % (clsName, x, y)

  #  Further dunder methods are left as an exercise to the try-hard readers.

"""ComplexNumber"""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen

from worktoy.desc import AttriBox
from typing import Never, Self


class ComplexNumber:
  """This class encapsulates a complex number. """

  __fallback_real__ = 0.0
  __fallback_imag__ = 0.0

  realPart = AttriBox[float]()
  imagPart = AttriBox[float]()

  def __init__(self, *args, **kwargs) -> None:
    """This method initializes the complex number. """
    #  First, let us look if the keyword arguments provides us with the
    #  values for the real and imaginary parts.
    _real = kwargs.get('real', None)
    _imag = kwargs.get('imag', None)
    #  In case any of the above is None, maybe the positional arguments
    #  provide the values.
    for arg in args:
      if isinstance(arg, complex):
        _real = arg.real
        _imag = arg.imag
        break  # This tells the loop to exit early
      if isinstance(arg, int):
        arg = float(arg)
      if isinstance(arg, float):
        if _real is None:
          _real = arg
          continue  # This tells the loop to stop and continue at the next
        if _imag is None:
          _imag = arg
          break  # This tells the loop to exit early
    else:  # This under-appreciated syntax is explained below
      if _real is None:
        _real = self.__fallback_real__
      if _imag is None:
        _imag = self.__fallback_imag__
    self.realPart = _real
    self.imagPart = _imag

  def __str__(self) -> str:
    """This method returns a string representation of the complex number. """
    return """%.3f + %.3f*I""" % (self.realPart, self.imagPart)

  def __repr__(self, ) -> str:
    """The purpose of '__repr__' generally is to return code that would
    create the instance when evaluated. """
    clsName = self.__class__.__name__
    return """%s(%.3f, %.3f)""" % (clsName, self.realPart, self.imagPart)

  def __abs__(self, ) -> float:
    """This method returns the absolute value of the complex number. """
    return (self.realPart ** 2 + self.imagPart ** 2) ** 0.5

  def __gt__(self, *_) -> Never:  # 'Never' means never returns
    """Complex numbers are unordered, meaning that the inequality
    operators are undefined. """
    e = """Complex numbers are unordered!"""
    raise TypeError(e)

  def __ge__(self, *_) -> Never:
    """Same as greater than """
    e = """Complex numbers are unordered!"""
    raise TypeError(e)

  def __lt__(self, *_) -> Never:
    """Same as greater than """
    e = """Complex numbers are unordered!"""
    raise TypeError(e)

  def __le__(self, *_) -> Never:
    """Same as greater than """
    e = """Complex numbers are unordered!"""
    raise TypeError(e)

  def __eq__(self, other: Self) -> bool:
    """Two complex numbers are equal when the absolute value of the
    difference between them is low enough. """
    if isinstance(other, complex):
      return self == ComplexNumber(other)
    if isinstance(other, ComplexNumber):
      return True if abs(self - other) ** 2 < 1e-12 else False

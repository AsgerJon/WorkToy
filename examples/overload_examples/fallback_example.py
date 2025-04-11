"""The 'fallbackExample' function demonstrates how the overloading
protocol can be used to implement a fallback function that is called when
none of the other overloads match the type signature of the arguments
received. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.mcls import BaseObject
from worktoy.static import overload, THIS


class ComplexNumber(BaseObject):
  """The 'ComplexNumber' class represents a complex number. """
  __slots__ = ('RE', 'IM')

  @overload(int, int)
  @overload(float, float)
  def __init__(self, realNum: float, imagNum: float) -> None:
    """Initialize the complex number with the given real and imaginary
    parts. """
    self.RE = float(realNum)
    self.IM = float(imagNum)

  @overload(complex)
  def __init__(self, complexNum: complex) -> None:
    """Initialize the complex number with the given complex number. """
    self.RE = complexNum.real
    self.IM = complexNum.imag

  @overload(THIS)
  def __init__(self, other: ComplexNumber) -> None:
    """Initialize the complex number with the given complex number. """
    self.RE = other.RE
    self.IM = other.IM

  @overload()
  def __init__(self) -> None:
    """Initialize the complex number with zero. """
    self.RE = 0.0
    self.IM = 0.0

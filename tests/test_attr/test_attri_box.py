"""TestAttriBox - Test the Attribox class."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase
from math import atan2
from random import random

from worktoy.attr import AttriBox, Field
from worktoy.mcls import BaseMeta
from worktoy.parse import maybe
from worktoy.static import overload, THIS
from worktoy.waitaminute import DispatchException

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Self, Any


class RealNumber:
  """Real number representation. """
  __fallback_value__ = 0.0
  __inner_value__ = None

  def __init__(self, value: float = None) -> None:
    """Initialize the RealNumber object."""
    if value is not None:
      self.__inner_value__ = float(value)

  def __float__(self) -> float:
    """Convert the RealNumber to a float."""
    return maybe(self.__inner_value__, self.__fallback_value__)

  def _resolveOther(self, other: Any) -> Self:
    """Resolve the other RealNumber."""
    cls = type(self)
    if isinstance(other, cls):
      return other
    try:
      return cls(other)
    except DispatchException:
      return NotImplemented

  def __eq__(self, other: Any) -> bool:
    """Check if two RealNumbers are equal."""
    other = self._resolveOther(other)
    if other is NotImplemented:
      return False
    return True if (float(self) - float(other)) ** 2 < 1e-10 else False


class R2(metaclass=BaseMeta):
  """R2 is a 2D vector class."""

  r0 = AttriBox[RealNumber](0.0)
  r1 = AttriBox[RealNumber](0.0)

  @overload(int, int)
  @overload(float, float)
  def __init__(self, x: float = 0.0, y: float = 0.0) -> None:
    """Initialize the R2 object."""
    self.r0 = RealNumber(x)
    self.r1 = RealNumber(y)

  @overload(THIS)
  def __init__(self, other: R2) -> None:
    """Initialize the R2 object."""
    self.r0 = RealNumber(other.r0)
    self.r1 = RealNumber(other.r1)

  @overload()
  def __init__(self, ) -> None:
    pass


class ComplexNumber(R2):
  """ComplexNumber is a complex number class."""

  real = Field()
  imag = Field()

  @real.GET
  def _getReal(self) -> float:
    """Get the real part of the complex number."""
    return float(self.r0)

  @imag.GET
  def _getImag(self) -> float:
    """Get the imaginary part of the complex number."""
    return float(self.r1)

  @overload(complex)
  def __init__(self, z: complex) -> None:
    """Initialize the R2 object."""
    self.r0 = RealNumber(z.real)
    self.r1 = RealNumber(z.imag)


class TestAttriBox(TestCase):
  """Test the AttriBox class."""

  def setUp(self, ) -> None:
    """Testing that complex numbers initialize correctly."""
    self.R2_0 = R2()
    self.R2_1 = R2(69, 420)
    self.R2_2 = R2(69.0, 420.0)
    self.R2_3 = R2(self.R2_0)
    self.C_0 = ComplexNumber()
    self.C_1 = ComplexNumber(69, 420)
    self.C_2 = ComplexNumber(69.0, 420.0)
    self.C_3 = ComplexNumber(self.C_0)
    self.C_4 = ComplexNumber(complex(69.0, 420.0))

  def test_values(self, ) -> None:
    """Test the values of the R2 class."""
    self.assertEqual(self.R2_0.r0, 0.0)
    self.assertEqual(self.R2_0.r1, 0.0)
    self.assertEqual(self.R2_1.r0, 69.0)
    self.assertEqual(self.R2_1.r1, 420.0)
    self.assertEqual(self.R2_2.r0, 69.0)
    self.assertEqual(self.R2_2.r1, 420.0)
    self.assertEqual(self.R2_3.r0, 0.0)
    self.assertEqual(self.R2_3.r1, 0.0)

  def test_accessors(self) -> None:
    """Test the accessors of the R2 class."""
    self.assertEqual(self.R2_0.r0, 0.0)
    self.R2_0.r0 = 69.0
    self.assertEqual(self.R2_0.r0, 69.0)
    self.assertEqual(self.R2_0.r1, 0.0)
    self.R2_0.r1 = 420.0
    self.assertEqual(self.R2_0.r1, 420.0)
    self.assertEqual(self.C_0.r0, 0.0)
    self.C_0.r0 = 69.0
    self.assertEqual(self.C_0.r1, 0.0)
    self.C_0.r1 = 420.0
    self.assertEqual(self.C_0.r0, 69.0)
    self.assertEqual(self.C_0.r1, 420.0)

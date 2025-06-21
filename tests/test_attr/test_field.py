"""TestField tests the Field descriptor functionality."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.attr import Field
from worktoy.mcls import BaseMeta
from worktoy.parse import maybe
from worktoy.static import overload
from worktoy.static.zeroton import THIS
from worktoy.waitaminute import ProtectedError

try:
  from typing import TYPE_CHECKING
except ImportError:  # pragma: no cover
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  pass


class R2(metaclass=BaseMeta):
  """R2 is a class that represents a point in 2D space."""

  __fallback_r0__ = 0.0
  __fallback_r1__ = 0.0

  __r_0__ = None
  __r_1__ = None

  r0 = Field()
  r1 = Field()

  @r0.GET
  def _getR0(self) -> float:
    """Get the x-coordinate."""
    return maybe(self.__r_0__, self.__fallback_r0__)

  @r0.SET
  def _setR0(self, value: float) -> None:
    """Set the x-coordinate."""
    self.__r_0__ = float(value)

  @r1.GET
  def _getR1(self) -> float:
    """Get the y-coordinate."""
    return maybe(self.__r_1__, self.__fallback_r1__)

  @r1.SET
  def _setR1(self, value: float) -> None:
    """Set the y-coordinate."""
    self.__r_1__ = float(value)

  @overload(int, int)
  @overload(float, float)
  def __init__(self, x: float = 0.0, y: float = 0.0) -> None:
    """Initialize the R2 object."""
    self.r0 = float(x)
    self.r1 = float(y)

  @overload(THIS)
  def __init__(self, other: R2) -> None:
    """Initialize the R2 object."""
    self.r0 = other.r0
    self.r1 = other.r1

  @overload()
  def __init__(self, ) -> None:
    pass


class ComplexNumber(R2):
  """ComplexNumber is a class that represents a complex number."""

  @overload(complex)
  def __init__(self, z: complex) -> None:
    """Initialize the R2 object."""
    self.r0 = z.real
    self.r1 = z.imag


class TestField(TestCase):
  """Test the Field descriptor functionality."""

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

  def test_init_get(self, ) -> None:
    """Test the values of the R2 class."""
    self.assertEqual(self.R2_0.r0, 0.0)
    self.assertEqual(self.R2_0.r1, 0.0)
    self.assertEqual(self.R2_1.r0, 69.0)
    self.assertEqual(self.R2_1.r1, 420.0)
    self.assertEqual(self.R2_2.r0, 69.0)
    self.assertEqual(self.R2_2.r1, 420.0)
    self.assertEqual(self.R2_3.r0, 0.0)
    self.assertEqual(self.R2_3.r1, 0.0)

  def test_good_set(self) -> None:
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

  def test_bad_delete(self) -> None:
    """Tests that the correct errors are raised."""
    with self.assertRaises(ProtectedError):
      del self.R2_0.r0
    with self.assertRaises(ProtectedError):
      del self.R2_0.r1
    with self.assertRaises(ProtectedError):
      del self.C_0.r0
    with self.assertRaises(ProtectedError):
      del self.C_0.r1

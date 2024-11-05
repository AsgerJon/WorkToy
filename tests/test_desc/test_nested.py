"""TestNested class tests the use of AttriBox with field classes that
themselves contain AttriBox instances. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.base import BaseObject, overload
from worktoy.desc import AttriBox
from worktoy.parse import floatCast, NumCastException


class Float(BaseObject):
  """Float class represents floating point valued real numbers"""

  value = AttriBox[float](0.0)

  @overload(float)
  def __init__(self, val: float) -> None:
    self.value = val

  @overload()
  def __init__(self) -> None:
    pass

  def __eq__(self, other: Float) -> bool:
    if isinstance(other, Float):
      return True if self.value == other.value else False
    try:
      return True if self.value == floatCast(other) else False
    except NumCastException:
      return NotImplemented


class Complex(BaseObject):
  """Complex class represents complex numbers with real and imaginary
  parts as AttriBox instances with field classes of type Float. """

  RE = AttriBox[Float]()
  IM = AttriBox[Float]()

  @overload(float, float)
  def __init__(self, *args) -> None:
    self.RE, self.IM = args

  @overload(float)
  def __init__(self, *args) -> None:
    self.RE = args[0]

  @overload()
  def __init__(self) -> None:
    pass

  @overload(complex)
  def __init__(self, val: complex) -> None:
    self.RE = val.real
    self.IM = val.imag


class TestNested(TestCase):
  """TestNested class tests the use of AttriBox with field classes that
  themselves contain AttriBox instances. """

  def setUp(self, ) -> None:
    self.xFloat = Float(420.69)
    self.xEmpty = Float()
    self.zFloatFloat = Complex(420., 69.)

  def test_float(self, ) -> None:
    self.assertEqual(self.xFloat.value, 420.69)
    self.assertEqual(self.xEmpty.value, 0.0)

  def test_complex(self, ) -> None:
    self.assertEqual(self.zFloatFloat.RE.value, 420.)
    self.assertEqual(self.zFloatFloat.IM.value, 69.)
    self.assertEqual(self.zFloatFloat.RE.value, 420.)
    self.assertEqual(self.zFloatFloat.IM.value, 69.)

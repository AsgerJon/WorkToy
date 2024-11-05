"""TestBaseAttriBox tests the basic functionalities of the AttriBox. This
includes the accessor functions, correct use of arguments to construct the
initial values, correct behaviour of field classes in AttriBox that
themselves implement AttriBox fields. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.base import BaseObject, overload
from worktoy.desc import AttriBox
from worktoy.parse import NumCastException


class Complex(BaseObject):
  """Complex number representation with real and imaginary parts
  implemented as instances of AttriBox."""

  RE = AttriBox[float]()
  IM = AttriBox[float]()

  @overload(float, float)
  def __init__(self, *args) -> None:
    self.RE, self.IM = args

  @overload(float)
  def __init__(self, *args) -> None:
    self.RE, self.IM = [*args, 0]

  @overload()
  def __init__(self) -> None:
    self.RE, self.IM = [0, 0]

  @overload(complex)
  def __init__(self, z: complex) -> None:
    self.RE, self.IM = [z.real, z.imag]


class TestComplex(TestCase):
  """TestBaseAttriBox tests the basic functionalities of the AttriBox. This
  includes the accessor functions, correct use of arguments to construct the
  initial values, correct behaviour of field classes in AttriBox that
  themselves implement AttriBox fields. """

  def setUp(self, ) -> None:
    self.zFloatFloat = Complex(69., 420.)
    self.zFloat = Complex(69.)
    self.zEmpty = Complex()
    self.zComplex = Complex(69. + 420.j)
    self.zIntInt = Complex(69, 420)
    self.zInt = Complex(69)
    self.zFloatInt = Complex(69., 420)
    self.zIntFloat = Complex(69, 420.)

  def testValues(self, ) -> None:
    """Test that the values of the Complex instances are correct. """
    self.assertEqual(self.zFloatFloat.RE, 69.)
    self.assertEqual(self.zFloatFloat.IM, 420.)
    self.assertEqual(self.zFloat.RE, 69.)
    self.assertEqual(self.zFloat.IM, 0.)
    self.assertEqual(self.zEmpty.RE, 0.)
    self.assertEqual(self.zEmpty.IM, 0.)
    self.assertEqual(self.zComplex.RE, 69.)
    self.assertEqual(self.zComplex.IM, 420.)
    self.assertEqual(self.zIntInt.RE, 69.)
    self.assertEqual(self.zIntInt.IM, 420.)
    self.assertEqual(self.zInt.RE, 69.)
    self.assertEqual(self.zInt.IM, 0.)
    self.assertEqual(self.zFloatInt.RE, 69.)
    self.assertEqual(self.zFloatInt.IM, 420.)
    self.assertEqual(self.zIntFloat.RE, 69.)
    self.assertEqual(self.zIntFloat.IM, 420.)

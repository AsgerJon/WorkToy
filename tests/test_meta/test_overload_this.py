"""TestOverloadThis tests that the overload protocol implemented in
'worktoy' supports the use of 'THIS' when overloading functions. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from random import random
from unittest import TestCase

from worktoy.desc import AttriBox, THIS
from worktoy.base import BaseObject, overload

try:
  from typing import TYPE_CHECKING
except ImportError:
  TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Self, Any
else:
  Any = object


  class Self:
    IM: float
    RE: float

eps = 1e-10


class Complex(BaseObject):
  """Class encapsulation of complex numbers. """
  RE = AttriBox[float]()
  IM = AttriBox[float]()

  @overload(float, float)
  def __init__(self, re_: float, im_: float) -> None:
    self.RE = re_
    self.IM = im_

  @overload(float)
  def __init__(self, re_: float) -> None:
    self.__init__(re_, 0.0)

  @overload(complex)
  def __init__(self, z: complex) -> None:
    self.__init__(z.real, z.imag)

  @overload(THIS)
  def __init__(self, other: Self) -> None:
    self.__init__(other.RE, other.IM)

  @overload()
  def __init__(self, ) -> None:
    self.__init__(0.0, 0.0)

  @overload(float)
  def __add__(self, other: float) -> Self:
    """Subtract a real number from this complex number."""
    return self + self.__class__(other + 0j)

  @overload(complex)
  def __add__(self, other: complex) -> Self:
    return self + self.__class__(other)

  @overload(THIS)
  def __add__(self, other: Self) -> Self:
    return self.__class__(self.RE + other.RE, self.IM + other.IM)

  def __radd__(self, other: Any) -> Self:
    """Add a complex number to this complex number."""
    return self + other

  @overload(float)
  def __sub__(self, other: float) -> Self:
    """Subtract a real number from this complex number."""
    return self - self.__class__(other + 0j)

  @overload(complex)
  def __sub__(self, other: complex) -> Self:
    """Subtract a complex number."""
    return self - self.__class__(other)

  @overload(THIS)
  def __sub__(self, other: Self) -> Self:
    """Subtract another Complex instance."""
    return self.__class__(self.RE - other.RE, self.IM - other.IM)

  @overload(float)
  def __mul__(self, other: float) -> Self:
    """Multiply by a real number."""
    return self * self.__class__(other + 0j)

  @overload(complex)
  def __mul__(self, other: complex) -> Self:
    """Multiply by a complex number."""
    return self * self.__class__(other)

  @overload(THIS)
  def __mul__(self, other: Self) -> Self:
    """Multiply by another Complex instance."""
    realPart = self.RE * other.RE - self.IM * other.IM
    imagPart = self.RE * other.IM + self.IM * other.RE
    return self.__class__(realPart, imagPart)

  @overload(float)
  def __truediv__(self, other: float) -> Self:
    """Divide by a real number."""
    return self / self.__class__(other)

  @overload(complex)
  def __truediv__(self, other: complex) -> Self:
    """Divide by a complex number."""
    return self / self.__class__(other)

  @overload(THIS)
  def __truediv__(self, other: Self) -> Self:
    """Divide by another Complex instance."""
    if other:
      denominator = other.RE ** 2 + other.IM ** 2
      re_part = (self.RE * other.RE + self.IM * other.IM) / denominator
      im_part = (self.IM * other.RE - self.RE * other.IM) / denominator
      return self.__class__(re_part, im_part)
    raise ZeroDivisionError("Division by zero.")

  @overload(float)
  def __eq__(self, other: float) -> bool:
    """Check if the real part is equal to the given number."""
    return self == self.__class__(other + 0j)

  @overload(complex)
  def __eq__(self, other: complex) -> bool:
    """Check if the real and imaginary parts are equal to the given complex
    number."""
    return self == self.__class__(other)

  @overload(THIS)
  def __eq__(self, other: Self) -> bool:
    """Check if the real and imaginary parts are equal to the given complex
    number."""
    if abs(self - other) < eps:
      return True
    return False

  def __neg__(self, ) -> Self:
    """Return the negation of the complex number."""
    return self.__class__(-self.RE, -self.IM)

  def __invert__(self, ) -> Self:
    """Return the conjugate of the complex number."""
    return self.__class__(self.RE, -self.IM)

  def __bool__(self) -> bool:
    """True when both real and imaginary parts are zero"""
    if self.RE or self.IM:
      return True
    return False

  def __abs__(self) -> float:
    """Return the absolute value of the complex number."""
    return (self * ~self).RE ** 0.5

  def __str__(self, ) -> str:
    """String representation"""
    return """%.3f + %.3f I""" % (self.RE, self.IM)

  def __repr__(self, ) -> str:
    """Code representation"""
    return """Complex(%.3f, %.3f)""" % (self.RE, self.IM)


class TestOverloadThis(TestCase):
  """TestOverloadThis tests that the overload protocol implemented in
  'worktoy' supports the use of 'THIS' when overloading functions. """

  def setUp(self) -> None:
    """Setting up each test"""
    self.sampleFloat = random()
    self.sampleComplex = random() + random() * 1j
    self.sampleTHIS = Complex(random() + random() * 1j)

  def test_init(self) -> None:
    """Test the __init__ method of the Complex class."""
    #  Test the float overload
    self.assertEqual(Complex(self.sampleFloat),
                     Complex(self.sampleFloat, 0.0))
    #  Test the complex overload
    self.assertEqual(Complex(self.sampleComplex),
                     Complex(self.sampleComplex))
    #  Test the 'THIS' overload
    self.assertEqual(Complex(self.sampleTHIS),
                     Complex(self.sampleTHIS.RE, self.sampleTHIS.IM))
    #  Test the default overload
    self.assertEqual(Complex(), Complex(0.0, 0.0))

  def test_add(self) -> None:
    """Test the __add__ method of the Complex class."""
    #  Test the float overload
    self.assertEqual(Complex(self.sampleFloat) + self.sampleFloat,
                     Complex(self.sampleFloat + self.sampleFloat, 0.0))
    #  Test the complex overload
    self.assertEqual(Complex(self.sampleComplex) + self.sampleComplex,
                     Complex(self.sampleComplex + self.sampleComplex))
    #  Test the 'THIS' overload
    self.assertEqual(self.sampleTHIS + self.sampleTHIS,
                     Complex(self.sampleTHIS.RE * 2, self.sampleTHIS.IM * 2))

  def test_sub(self) -> None:
    """Test the __sub__ method of the Complex class."""
    #  Test the float overload
    self.assertEqual(Complex(self.sampleFloat) - self.sampleFloat,
                     Complex(self.sampleFloat - self.sampleFloat, 0.0))
    #  Test the complex overload
    self.assertEqual(Complex(self.sampleComplex) - self.sampleComplex,
                     Complex(self.sampleComplex - self.sampleComplex))
    #  Test the 'THIS' overload
    self.assertEqual(self.sampleTHIS - self.sampleTHIS,
                     Complex(0.0, 0.0))

  def test_mul(self) -> None:
    """Test the __mul__ method of the Complex class."""
    #  Test the float overload
    self.assertEqual(Complex(self.sampleFloat) * self.sampleFloat,
                     Complex(self.sampleFloat * self.sampleFloat, 0.0))
    #  Test the complex overload
    self.assertEqual(Complex(self.sampleComplex) * self.sampleComplex,
                     Complex(self.sampleComplex * self.sampleComplex))
    #  Test the 'THIS' overload
    self.assertEqual(self.sampleTHIS * self.sampleTHIS,
                     Complex(self.sampleTHIS.RE ** 2 - self.sampleTHIS.IM
                             ** 2,
                             2 * self.sampleTHIS.RE * self.sampleTHIS.IM))

  def test_truediv(self) -> None:
    """Test the __truediv__ method of the Complex class."""
    #  Test the float overload
    self.assertEqual(Complex(self.sampleFloat) / self.sampleFloat,
                     Complex(self.sampleFloat / self.sampleFloat, 0.0))
    #  Test the complex overload
    self.assertEqual(Complex(self.sampleComplex) / self.sampleComplex,
                     Complex(self.sampleComplex / self.sampleComplex))
    #  Test the 'THIS' overload
    self.assertEqual(self.sampleTHIS / self.sampleTHIS,
                     Complex(1.0, 0.0))

  def test_eq(self) -> None:
    """Test the __eq__ method of the Complex class."""
    #  Test the float overload
    self.assertEqual(Complex(self.sampleFloat) == self.sampleFloat,
                     Complex(self.sampleFloat) == Complex(self.sampleFloat))
    #  Test the complex overload
    self.assertEqual(Complex(self.sampleComplex) == self.sampleComplex,
                     Complex(self.sampleComplex) == Complex(
                         self.sampleComplex))
    #  Test the 'THIS' overload
    self.assertEqual(self.sampleTHIS == self.sampleTHIS,
                     Complex(self.sampleTHIS.RE, self.sampleTHIS.IM) ==
                     Complex(self.sampleTHIS.RE, self.sampleTHIS.IM))

  def test_neg(self) -> None:
    """Test the __neg__ method of the Complex class."""
    self.assertEqual(-Complex(self.sampleFloat),
                     Complex(-self.sampleFloat, 0.0))

  def test_invert(self) -> None:
    """Test the __invert__ method of the Complex class."""
    self.assertEqual(~Complex(self.sampleFloat),
                     Complex(self.sampleFloat, 0.0))
    left = self.sampleTHIS * ~self.sampleTHIS
    right = abs(self.sampleTHIS) ** 2
    self.assertEqual(left, right)

  def test_type_matching(self):
    instance = Complex(3.0, 4.0)
    self.assertTrue(isinstance(instance + instance,
                               Complex))  # THIS overload
    self.assertTrue(isinstance(instance + 5, Complex))  # float overload
    self.assertTrue(isinstance(instance + (2 + 3j),
                               Complex))  # complex overload

  def test_method_resolution_order(self):
    instance = Complex(2.0, 3.0)
    self.assertEqual(str(instance + 5),
                     str(Complex(7.0, 3.0)))  # Ensures float adds correctly
    self.assertEqual(str(instance + (1 + 2j)),
                     str(Complex(3.0, 5.0)))  # complex adds correctly

  def test_error_handling(self):
    instance = Complex(1.0, 1.0)
    with self.assertRaises(TypeError):
      instance + 'string'
    with self.assertRaises(ZeroDivisionError):
      instance / Complex()  # Division by zero complex number

  def test_identity_and_inverse(self):
    identity = Complex(0, 0)
    inverse = Complex(-1, -1)
    instance = Complex(1, 1)
    self.assertEqual(instance + identity, instance)  # Adding zero
    self.assertEqual(instance * identity, identity)  # Multiplying by zero
    self.assertEqual(instance + inverse,
                     identity)  # Adding inverse results in zero

  def test_conformance(self):
    instances = [Complex(i, i) for i in range(5)]
    sum_instances = sum(instances, Complex(0, 0))
    self.assertTrue(isinstance(sum_instances, Complex))
    self.assertEqual(sum_instances, Complex(10, 10))

"""
TestComplex tests the overloading functionality as represented by the
'ComplexNumber' class.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.utilities import stringList
from worktoy.utilities.mathematics import sin, cos
from . import DispatcherTest, ComplexNumber, ComplexSubclass, ComplexMeta

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestComplex(DispatcherTest):
  """
  TestComplex tests the overloading functionality as represented by the
  'ComplexNumber' class.
  """

  def test_existence(self, ) -> None:
    self.assertIsNotNone(ComplexNumber)
    self.assertIsInstance(ComplexNumber, type)

  def test_init(self, ) -> None:
    float2args = 0.1337, 0.80085
    complexArg = 0.1337 + 0.80085j
    float1arg = 0.69
    for cls in (ComplexNumber, ComplexSubclass, ComplexMeta):
      zFloat2 = cls(*float2args)
      self.assertIsInstance(zFloat2, cls)
      self.assertAlmostEqual(zFloat2.RE, 0.1337)
      self.assertAlmostEqual(zFloat2.IM, 0.80085)
      self.assertAlmostEqual(complex(zFloat2), complexArg)
      zOther = cls(zFloat2)
      self.assertIsInstance(zOther, cls)
      self.assertAlmostEqual(zOther.RE, 0.1337)
      self.assertAlmostEqual(zOther.IM, 0.80085)
      self.assertEqual(complex(zOther), complexArg)
      zFloat1 = cls(float1arg)
      self.assertIsInstance(zFloat1, cls)
      self.assertAlmostEqual(zFloat1.RE, 0.69)
      self.assertAlmostEqual(zFloat1.IM, 0.0)
      self.assertAlmostEqual(complex(zFloat1), 0.69 + 0j)
      zComplex = cls(complexArg)
      self.assertIsInstance(zComplex, cls)
      self.assertAlmostEqual(zComplex.RE, 0.1337)
      self.assertAlmostEqual(zComplex.IM, 0.80085)
      self.assertAlmostEqual(complex(zComplex), complexArg)
      zOther = cls(zComplex)
      self.assertIsInstance(zOther, cls)
      self.assertAlmostEqual(zOther.RE, 0.1337)
      self.assertAlmostEqual(zOther.IM, 0.80085)
      self.assertAlmostEqual(complex(zOther), complexArg)
      zNoArgs = cls()
      self.assertIsInstance(zNoArgs, cls)
      self.assertAlmostEqual(zNoArgs.RE, 0.0)
      self.assertAlmostEqual(zNoArgs.IM, 0.0)
      self.assertAlmostEqual(complex(zNoArgs), 0.0 + 0j)

  def test_subclass_init(self, ) -> None:
    """
    Tests the '__init__' overloads specific to subclasses.
    """

    strArgs = stringList("""69 + 420I, 69+420j, 69 + 420J""")
    for args in strArgs:
      z = ComplexSubclass(args)
      self.assertIsInstance(z, ComplexSubclass)
      self.assertIsInstance(z, ComplexNumber)
      self.assertAlmostEqual(z.RE, 69.0)
      self.assertAlmostEqual(z.IM, 420.0)
      self.assertAlmostEqual(complex(z), 69 + 420j)

    parentInstance = ComplexNumber(69, 420)
    z = ComplexSubclass(parentInstance)  # Passing parent instance
    self.assertIsInstance(z, ComplexSubclass)
    self.assertIsInstance(z, ComplexNumber)
    self.assertAlmostEqual(z.RE, 69.0)
    self.assertAlmostEqual(z.IM, 420.0)
    self.assertAlmostEqual(complex(z), 69 + 420j)
    self.assertAlmostEqual(parentInstance, z)

  def test_arithmetic(self, ) -> None:
    """
    Tests the arithmetic operations of the complex number classes by
    applying the same arithmetic operations to each of ComplexNumber,
    ComplexSubclass, and ComplexMeta.
    """
    float2args = 0.1337, 0.80085
    complexArg = 69 + 420j
    float1arg = 1337

    for cls in (ComplexNumber, ComplexSubclass, ComplexMeta):
      zFloat2 = cls(*float2args)
      zOther = cls(zFloat2)
      zFloat1 = cls(float1arg)
      zComplex = cls(complexArg)
      zNoArgs = cls()
      Z = [zFloat2, zOther, zFloat1, zComplex, zNoArgs]
      for z0 in Z:
        for z1 in Z:
          #  Addition
          ExpReal = z0.RE + z1.RE
          ExpImag = z0.IM + z1.IM
          actual = z0 + z1
          self.assertIsInstance(actual, cls)
          self.assertAlmostEqual(actual.RE, ExpReal)
          self.assertAlmostEqual(actual.IM, ExpImag)
          #  Subtraction
          ExpReal = z0.RE - z1.RE
          ExpImag = z0.IM - z1.IM
          actual = z0 - z1
          self.assertIsInstance(actual, cls)
          self.assertAlmostEqual(actual.RE, ExpReal)
          self.assertAlmostEqual(actual.IM, ExpImag)
          #  Multiplication
          ExpReal = z0.RE * z1.RE - z0.IM * z1.IM
          ExpImag = z0.RE * z1.IM + z0.IM * z1.RE
          actual = z0 * z1
          self.assertIsInstance(actual, cls)
          self.assertAlmostEqual(actual.RE, ExpReal)
          self.assertAlmostEqual(actual.IM, ExpImag)
          #  Division

  def test_abs(self) -> None:
    """
    Tests the absolute value of the complex number classes.
    """
    float2args = 0.1337, 0.80085
    complexArg = 69 + 420j
    float1arg = 1337

    for cls in (ComplexNumber, ComplexSubclass, ComplexMeta):
      zFloat2 = cls(*float2args)
      zOther = cls(zFloat2)
      zFloat1 = cls(float1arg)
      zComplex = cls(complexArg)
      zNoArgs = cls()
      Z = [zFloat2, zOther, zFloat1, zComplex, zNoArgs]
      for z in Z:
        expectedAbs = (z.RE ** 2 + z.IM ** 2) ** 0.5
        self.assertAlmostEqual(abs(z), expectedAbs)

  def test_arg(self, ) -> None:
    """
    Tests the argument of the complex number classes.
    """
    float2args = 0.1337, 0.80085
    complexArg = 69 + 420j
    float1arg = 1337

    for cls in (ComplexNumber, ComplexSubclass, ComplexMeta):
      zFloat2 = cls(*float2args)
      zOther = cls(zFloat2)
      zFloat1 = cls(float1arg)
      zComplex = cls(complexArg)
      zNoArgs = cls()
      Z = [zFloat2, zOther, zFloat1, zComplex, zNoArgs]
      for z in Z:
        if not z:
          continue
        cosExp = z.RE / abs(z)
        sinExp = z.IM / abs(z)
        self.assertAlmostEqual(cos(z.ARG), cosExp)
        self.assertAlmostEqual(sin(z.ARG), sinExp)

  def test_exponentiation(self, ) -> None:
    """Tests the exponentiation of the complex number classes."""
    float2args = 2 ** 0.5, 3 ** 0.5
    complexArg = 1 + 1j
    float1arg = 0.5

    for cls in (ComplexNumber, ComplexSubclass, ComplexMeta):
      zFloat2 = cls(*float2args)
      zFloat1 = cls(float1arg)
      zComplex = cls(complexArg)
      Z = [zFloat2, zFloat1, zComplex]
      for z0 in Z:
        for z1 in Z:
          expected = complex(z0) ** complex(z1)
          actual = z0 ** z1
          self.assertIsInstance(actual, cls)
          self.assertAlmostEqual(complex(actual), expected)

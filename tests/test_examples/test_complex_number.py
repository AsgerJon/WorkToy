"""
TestComplexNumber tests the ComplexNumber class from the examples module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.examples import ComplexNumber
from worktoy.utilities.mathematics import pi
from . import ExampleTest

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestComplexNumber(ExampleTest):
  """
  TestComplexNumber tests the ComplexNumber class from the examples module.
  """

  def test_dev_null(self, ) -> None:
    """
    Sanity check that the test runs.
    """

    self.assertTrue(True)

  def test_init_int_int(self, ) -> None:
    """
    Test that the ComplexNumber class can be initialized on two integers.
    """

    z0 = ComplexNumber(69, 420)
    self.assertAlmostEqual(z0.REAL, 69)
    self.assertAlmostEqual(z0.IMAG, 420)
    self.assertIsInstance(z0, ComplexNumber)
    self.assertIsInstance(z0.REAL, float)
    self.assertIsInstance(z0.IMAG, float)

  def test_init_float_float(self, ) -> None:
    """
    Test that the ComplexNumber class can be initialized on two floats.
    """

    z0 = ComplexNumber(1337.0, 80085.0)
    self.assertAlmostEqual(z0.REAL, 1337.0)
    self.assertAlmostEqual(z0.IMAG, 80085.0)
    self.assertIsInstance(z0, ComplexNumber)
    self.assertIsInstance(z0.REAL, float)
    self.assertIsInstance(z0.IMAG, float)

  def test_init_float_int(self, ) -> None:
    """
    Test that the ComplexNumber class can be initialized on a float and an
    int.
    """

    z0 = ComplexNumber(3.14, 42)
    self.assertAlmostEqual(z0.REAL, 3.14)
    self.assertAlmostEqual(z0.IMAG, 42)
    self.assertIsInstance(z0, ComplexNumber)
    self.assertIsInstance(z0.REAL, float)
    self.assertIsInstance(z0.IMAG, float)

  def test_init_int_float(self, ) -> None:
    """
    Test that the ComplexNumber class can be initialized on an int and a
    float.
    """

    z0 = ComplexNumber(42, 3.14)
    self.assertAlmostEqual(z0.REAL, 42)
    self.assertAlmostEqual(z0.IMAG, 3.14)
    self.assertIsInstance(z0, ComplexNumber)
    self.assertIsInstance(z0.REAL, float)
    self.assertIsInstance(z0.IMAG, float)

  def test_init_complex(self, ) -> None:
    """
    Test that the ComplexNumber class can be initialized on a complex number.
    """

    z0 = ComplexNumber(69 + 420j)
    self.assertAlmostEqual(z0.REAL, 69)
    self.assertAlmostEqual(z0.IMAG, 420)
    self.assertIsInstance(z0, ComplexNumber)
    self.assertIsInstance(z0.REAL, float)
    self.assertIsInstance(z0.IMAG, float)

  def test_init_self(self, ) -> None:
    """
    Test that the ComplexNumber class can be initialized on another
    instance of
    itself.
    """

    z0 = ComplexNumber(69, 420)
    z1 = ComplexNumber(z0)
    self.assertAlmostEqual(z1.REAL, 69)
    self.assertAlmostEqual(z1.IMAG, 420)
    self.assertIsInstance(z1, ComplexNumber)
    self.assertIsInstance(z1.REAL, float)
    self.assertIsInstance(z1.IMAG, float)

  def test_init_kwargs(self, ) -> None:
    """
    Test that the ComplexNumber class can be initialized with no arguments.
    """

    z0 = ComplexNumber(real=69, imag=420)
    self.assertAlmostEqual(z0.REAL, 69)
    self.assertAlmostEqual(z0.IMAG, 420)
    self.assertIsInstance(z0, ComplexNumber)
    self.assertIsInstance(z0.REAL, float)
    self.assertIsInstance(z0.IMAG, float)

  def test_init_none(self, ) -> None:
    """
    Test that the ComplexNumber class can be initialized with no arguments.
    """

    z0 = ComplexNumber()
    self.assertAlmostEqual(z0.REAL, 0)
    self.assertAlmostEqual(z0.IMAG, 0)
    self.assertIsInstance(z0, ComplexNumber)
    self.assertIsInstance(z0.REAL, float)
    self.assertIsInstance(z0.IMAG, float)

  def test_abs_get(self, ) -> None:
    """
    Test that the ABS property of the ComplexNumber class returns the
    correct value.
    """

    samples = self.randFloatTuples(69, 2, -1000.0, 1000.0)
    for x, y in samples:
      z = ComplexNumber(x, y)
      self.assertAlmostEqual(z.ABS, abs(z))
      self.assertAlmostEqual(z.ABS ** 2, x ** 2 + y ** 2)

  def test_arg_get(self, ) -> None:
    """
    Test that the ARG property of the ComplexNumber class returns the
    correct value.
    """

    z45 = ComplexNumber(1, 1)
    self.assertAlmostEqual(z45.ARG * 4, pi)
    z30 = ComplexNumber(1, 3 ** 0.5 / 3)
    self.assertAlmostEqual(z30.ARG * 6, pi)
    z60 = ComplexNumber(1, 3 ** 0.5)
    self.assertAlmostEqual(z60.ARG * 3, pi)
    x15 = (6 ** 0.5 + 2 ** 0.5) / 4
    y15 = (6 ** 0.5 - 2 ** 0.5) / 4
    z15 = ComplexNumber(x15, y15)
    self.assertAlmostEqual(z15.ARG, pi / 12)
    z90 = ComplexNumber(0, 1)
    self.assertAlmostEqual(z90.ARG * 2, pi)

  def test_abs_set(self, ) -> None:
    """
    Test that the ABS property of the ComplexNumber class can be set to
    the correct value.
    """

    z = ComplexNumber(3, 4)
    z.ABS = 10
    self.assertAlmostEqual(z.ABS, 10)
    self.assertAlmostEqual(z.REAL / abs(z), 3 / 5)
    self.assertAlmostEqual(z.IMAG / abs(z), 4 / 5)
    z.ABS = 5
    self.assertAlmostEqual(z.ABS, 5)
    self.assertAlmostEqual(z.REAL / abs(z), 3 / 5)
    self.assertAlmostEqual(z.IMAG / abs(z), 4 / 5)

  def test_arg_set(self, ) -> None:
    """
    Test that the ARG property of the ComplexNumber class can be set to
    the correct value.
    """

    z = ComplexNumber(1, 0)
    z.ARG = pi / 4
    self.assertAlmostEqual(z.ARG, pi / 4)
    self.assertAlmostEqual(z.REAL, z.IMAG)
    z.ARG = pi / 3
    self.assertAlmostEqual(z.ARG, pi / 3)
    self.assertAlmostEqual(z.IMAG / abs(z), 3 ** 0.5 / 2)
    self.assertAlmostEqual(z.REAL / abs(z), 1 / 2)
    z.ARG = pi / 2
    self.assertAlmostEqual(z.ARG, pi / 2)
    self.assertAlmostEqual(z.REAL, 0)
    self.assertAlmostEqual(z.IMAG, z.ABS)

  def test_bool(self) -> None:
    """
    Test that the __bool__ method of the ComplexNumber class returns the
    correct value.
    """

    z0 = ComplexNumber(0, 0)
    self.assertFalse(z0)
    z1 = ComplexNumber(1, 0)
    self.assertTrue(z1)
    z2 = ComplexNumber(0, 1)
    self.assertTrue(z2)
    z3 = ComplexNumber(1, 1)
    self.assertTrue(z3)

  def test_complex(self) -> None:
    """
    Test that the __complex__ method of the ComplexNumber class returns the
    correct value.
    """

    z0 = ComplexNumber(69, 420)
    self.assertAlmostEqual(complex(z0).real, z0.REAL)
    self.assertAlmostEqual(complex(z0).imag, z0.IMAG)

  def test_str(self, ) -> None:
    """
    Test that the __str__ method of the ComplexNumber class returns the
    correct value.
    """

    z0 = ComplexNumber(69, 420)
    self.assertEqual(str(z0), "69.000 + 420.000J")
    z1 = ComplexNumber(1337, -80085)
    self.assertEqual(str(z1), "1337.000 - 80085.000J")
    z2 = ComplexNumber(0, 1)
    self.assertEqual(str(z2), "1.000J")
    z3 = ComplexNumber(0, -1)
    self.assertEqual(str(z3), "-1.000J")

  def test_repr(self, ) -> None:
    """
    Test that the __repr__ method of the ComplexNumber class returns the
    correct value.
    """
    z0 = ComplexNumber(69, 420)
    self.assertEqual(repr(z0), """ComplexNumber(69.0, 420.0)""")

  def test_bad_arg_set(self, ) -> None:
    """
    Test that setting the ARG property of the ComplexNumber class to a
    non-float value raises a TypeError.
    """
    z0 = ComplexNumber(0, 0)
    with self.assertRaises(ZeroDivisionError):
      z0.ARG = pi / 4

  def test_bad_abs_set(self, ) -> None:
    """
    Test that setting the ABS property of the ComplexNumber class to a
    non-float value raises a TypeError.
    """
    z0 = ComplexNumber(0, 0)
    with self.assertRaises(ZeroDivisionError):
      z0.ABS = 69

  def test_gymnastics(self) -> None:
    """
    Those difficult to cover bits
    """
    z0 = ComplexNumber(0, 0)
    self.assertEqual(str(z0), "0")
    z1 = ComplexNumber(1, 0)
    self.assertEqual(str(z1), "1.000")
    z2 = ComplexNumber(0, 1)
    self.assertEqual(str(z2), "1.000J")

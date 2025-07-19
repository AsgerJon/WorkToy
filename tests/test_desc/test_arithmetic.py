"""
TestArithmetic tests the shared arithmetic implementations on each of the
complex number implementations.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from random import random
from typing import TYPE_CHECKING

from . import DescTest

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestArithmetic(DescTest):
  """
  TestArithmetic tests the shared arithmetic implementations on each of the
  complex number implementations.
  """

  def setUp(self) -> None:
    from . import ComplexBox, ComplexFields, ComplexFieldsSubclass
    from . import ComplexLabel, ComplexAlias
    from tests.test_dispatch import ComplexNumber, ComplexSubclass
    from tests.test_dispatch import ComplexMeta, ComplexMetaSub
    self.classes = [
        ComplexBox,
        ComplexFields,
        ComplexFieldsSubclass,
        ComplexLabel,
        ComplexAlias,
        ComplexNumber,
        ComplexSubclass,
        ComplexMeta,
        ComplexMetaSub,
    ]
    self.posArgs = dict()
    n = 1  # Number of samples in each quadrant. Keep at 1 when developing
    for cls in self.classes:
      self.posArgs[cls] = []
      for _ in range(n):
        x, y = 1.0 + random(), 1.0 + random()
        self.posArgs[cls].append((x, y))
      for _ in range(n):
        x, y = 1.0 + random(), - 1.0 - random()
        self.posArgs[cls].append((x, y))
      for _ in range(n):
        x, y = -1.0 - random(), -1.0 - random()
        self.posArgs[cls].append((x, y))
      for _ in range(n):
        x, y = -1.0 - random(), 1.0 + random()
        self.posArgs[cls].append((x, y))
    self.numbers = dict()
    for cls in self.classes:
      self.numbers[cls] = [cls(*args) for args in self.posArgs[cls]]

  def test_addition(self) -> None:
    for cls in self.classes:
      for z0 in self.numbers[cls]:
        for z1 in self.numbers[cls]:
          z = z0 + z1
          self.assertAlmostEqual(z.RE, z0.RE + z1.RE)
          self.assertAlmostEqual(z.IM, z0.IM + z1.IM)

  def test_subtraction(self) -> None:
    for cls in self.classes:
      for z0 in self.numbers[cls]:
        for z1 in self.numbers[cls]:
          z = z0 - z1
          self.assertAlmostEqual(z.RE, z0.RE - z1.RE)
          self.assertAlmostEqual(z.IM, z0.IM - z1.IM)

  def test_multiplication(self) -> None:
    for cls in self.classes:
      for z0 in self.numbers[cls]:
        for z1 in self.numbers[cls]:
          z = z0 * z1
          self.assertAlmostEqual(z.RE, z0.RE * z1.RE - z0.IM * z1.IM)
          self.assertAlmostEqual(z.IM, z0.RE * z1.IM + z0.IM * z1.RE)

  def test_division(self) -> None:
    for cls in self.classes:
      for z0 in self.numbers[cls]:
        for z1 in self.numbers[cls]:
          z = z0 / z1
          expReal = complex(z).real
          expImag = complex(z).imag
          expected = expReal + expImag * 1j
          actual = complex(z)
          self.assertAlmostEqual(actual.real, expected.real)
          self.assertAlmostEqual(actual.imag, expected.imag)

  def test_powers(self, ) -> None:
    for cls in self.classes:
      for z0 in self.numbers[cls]:
        for z1 in self.numbers[cls]:
          z = z0 ** z1
          expReal = complex(z).real
          expImag = complex(z).imag
          expected = expReal + expImag * 1j
          actual = complex(z)
          self.assertAlmostEqual(actual.real, expected.real)
          self.assertAlmostEqual(actual.imag, expected.imag)

  def test_abs(self) -> None:
    for cls in self.classes:
      for z in self.numbers[cls]:
        absZ = abs(z)
        expected = (z.RE ** 2 + z.IM ** 2) ** 0.5
        self.assertAlmostEqual(absZ, expected)

  def test_bad_power(self) -> None:
    for cls in self.classes:
      for z0 in self.numbers[cls]:
        with self.assertRaises(TypeError):
          _ = z0 ** 'trololololo'

  def test_bad_multiplication(self) -> None:
    for cls in self.classes:
      for z0 in self.numbers[cls]:
        with self.assertRaises(TypeError):
          _ = z0 * 'trololololo'

  def test_bad_division(self) -> None:
    for cls in self.classes:
      for z0 in self.numbers[cls]:
        with self.assertRaises(ZeroDivisionError):
          _ = z0 / 0
        with self.assertRaises(TypeError):
          _ = z0 / 'trololololo'
      zero = cls(0, 0)
      self.assertFalse(zero / self.numbers[cls][0])
      with self.assertRaises(ZeroDivisionError):
        _ = ~zero

  def test_bad_addition(self) -> None:
    for cls in self.classes:
      for z0 in self.numbers[cls]:
        with self.assertRaises(TypeError):
          _ = z0 + 'trololololo'
        with self.assertRaises(TypeError):
          _ = 'trololololo' + z0

  def test_bad_subtraction(self) -> None:
    for cls in self.classes:
      for z0 in self.numbers[cls]:
        with self.assertRaises(TypeError):
          _ = z0 - 'trololololo'
        with self.assertRaises(TypeError):
          _ = 'trololololo' - z0

  def test_good_equals(self) -> None:
    """
    Test that the __eq__ method works correctly.
    """
    for cls in self.classes:
      for z0 in self.numbers[cls]:
        self.assertTrue(z0 == z0)
        self.assertFalse(z0 == 'bro im z0 too, trust!')

  def test_hash(self) -> None:
    """
    Test that the __hash__ method works correctly.
    """
    for cls in self.classes:
      for z0 in self.numbers[cls]:
        self.assertIsInstance(hash(z0), int)

  def test_str_repr(self) -> None:
    """
    Test that the __str__ and __repr__ methods work correctly.
    """
    for cls in self.classes:
      z0 = cls(.0, .0)
      z1 = cls(69, -420)
      z2 = cls(69, 420)
      self.assertEqual(str(z0), '0')
      self.assertIn('-', str(z1))
      self.assertIn('+', str(z2))
      z3 = cls(0.80085, 0)
      z4 = cls(0, 0.80085)
      self.assertEqual(str(z3), '%f' % (z3.RE,))
      self.assertEqual(str(z4), '%fJ' % (z4.IM,))
      expected = ('%s(%f, %f)' % (cls.__name__, .0, .0)).replace('0', '')
      actual = repr(z0).replace('0', '')
      self.assertEqual(actual, expected)

  def test_iter(self) -> None:
    """
    Test that the __iter__ method works correctly.
    """
    for cls in self.classes:
      z = cls(69, 420)
      a, b = z
      self.assertAlmostEqual(a, 69.)
      self.assertAlmostEqual(b, 420.)

  def test_bad_args(self) -> None:
    """
    Test that the __init__ method raises TypeError when given bad arguments.
    """
    for cls in self.classes:
      zero = cls(0, 0)
      with self.assertRaises(ZeroDivisionError):
        _ = zero.ARG

  def test_complex(self) -> None:
    """
    Test that the __complex__ method works correctly.
    """
    for cls in self.classes:
      z = cls(69, 420)
      c = complex(z)
      self.assertAlmostEqual(c.real, 69.)
      self.assertAlmostEqual(c.imag, 420.)

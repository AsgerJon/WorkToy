"""
TestArithmetic tests the shared arithmetic implementations on each of the
complex number implementations.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

import os
from random import random
from typing import TYPE_CHECKING

from worktoy.dispatch import TypeSig
from . import DescTest
from tests.test_dispatch import Comflex, ComflexMeta

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestArithmetic(DescTest):
  """
  TestArithmetic tests the shared arithmetic implementations on each of the
  complex number implementations.
  """

  def setUp(self) -> None:
    from . import ComplexBox, ComplexFields, ComplexFieldsSubclass
    from . import ComplexFix, ComplexAlias
    from tests.test_dispatch import ComplexNumber, ComplexSubclass
    from tests.test_dispatch import ComplexMeta, ComplexMetaSub
    from tests.test_dispatch import Comflex, ComflexMeta
    self.classes = [
      ComplexBox,
      ComplexFields,
      ComplexFieldsSubclass,
      ComplexFix,
      ComplexAlias,
      ComplexNumber,
      ComplexSubclass,
      ComplexMeta,
      ComplexMetaSub,
      Comflex,
      ComflexMeta
    ]
    self.posArgs = dict()
    n = 8  # Number during tests in CI/CD
    #  Reduces 'n' to 1 during development.
    if os.environ.get('DEVELOPMENT_ENVIRONMENT'):  # pragma: no cover
      n = 1
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

  def test_comflex(self, ) -> None:
    """
    More coverage gymnastics
    """
    z = 69 + 420j
    x = 1337.
    for Z in (Comflex, ComflexMeta):
      z1 = Comflex(x, z)
      z2 = Comflex(z, x)
      self.assertAlmostEqual(z1.RE, x + z.real)
      self.assertAlmostEqual(z1.IM, z.imag)
      self.assertAlmostEqual(z2.RE, x + z.real)
      self.assertAlmostEqual(z2.IM, z.imag)

  def test_fallback(self) -> None:
    for Z in (Comflex, ComflexMeta):
      gym = Z.__init__._getSigFuncMap()[TypeSig(float, complex)]
      breh = Z(0j)
      gym(breh, 'never', 'gonna', 'give', 'you', 'up', 69., 420 + 1337j)
      self.assertEqual(breh.RE, 69. + 420.)
      self.assertEqual(breh.IM, 1337.)

  def test_flex(self) -> None:
    """Test the ComflexMeta constructor"""

    z = ComflexMeta(69 + 420j, 1337.)
    self.assertAlmostEqual(z.RE, 69. + 1337.)
    self.assertAlmostEqual(z.IM, 420.)

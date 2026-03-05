"""
TestAlias tests specific functionality of the 'Alias' descriptor not
covered by the contextual tests in 'DescTest'.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import DescTest, ComplexAlias

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestAlias(DescTest):
  """
  TestAlias tests specific functionality of the 'Alias' descriptor not
  covered by the contextual tests in 'DescTest'.
  """

  def setUp(self, ) -> None:
    super().setUp()
    self.sampleArgs = self.randFloatTuples(32, 2, -69, 420)

  def assertAlmostEqual(self, *args, **kwargs) -> None:
    left, right, *rest = args
    if isinstance(left, ComplexAlias) or isinstance(right, ComplexAlias):
      loss = abs(left - right)
      scale = max(abs(left), abs(right), 1)
      return self.assertLess(loss, 1e-6 * scale)
    return super().assertAlmostEqual(*args, **kwargs)

  def test_init(self, ) -> None:
    """
    Testing initialization of 'ComplexAlias'.
    """
    for args in self.sampleArgs:
      z = ComplexAlias(*args)
      self.assertIsInstance(z, ComplexAlias)
      c = complex(*args)
      z1, z2 = ComplexAlias.cast(c), ComplexAlias(z)
      self.assertAlmostEqual(z1, z2)
      self.assertAlmostEqual(complex(z1), complex(z2))

  def test_get(self, ) -> None:
    """
    Testing that '__get__' matches the aliased descriptor.
    """
    for args in self.sampleArgs:
      z = ComplexAlias(*args)
      self.assertEqual(z.x, z.RE)
      self.assertEqual(z.y, z.IM)

  def test_set(self, ) -> None:
    """
    Testing that '__set__' matches the aliased descriptor.
    """
    for args in self.sampleArgs:
      z = ComplexAlias(0, 0)
      self.assertFalse(z.x)
      self.assertFalse(z.y)
      self.assertFalse(z.RE)
      self.assertFalse(z.IM)
      self.assertFalse(z.REAL)
      self.assertFalse(z.IMAG)
      newReal, newImag = args
      z.REAL = newReal
      self.assertEqual(z.RE, newReal)
      z.IMAG = newImag
      self.assertEqual(z.IM, newImag)

  def test_delete(self, ) -> None:
    """
    Testing that '__delete__' matches the aliased descriptor.
    """
    for args in self.sampleArgs:
      z1 = ComplexAlias(*args)
      z2 = ComplexAlias(*args)
      self.assertAlmostEqual(z1 * z1.conj(), z1.ABS ** 2)
      del z1.x
      del z1.y
      for attr in ('x', 'y', 'RE', 'IM', 'REAL', 'IMAG'):
        with self.assertRaises(AttributeError) as info:
          _ = getattr(z1, attr)
        self.assertIn('has no attribute', str(info.exception))
      del z2.REAL
      del z2.IMAG
      for attr in ('x', 'y', 'RE', 'IM', 'REAL', 'IMAG'):
        with self.assertRaises(AttributeError) as info:
          _ = getattr(z2, attr)
        self.assertIn('has no attribute', str(info.exception))

  def test_identity(self, ) -> None:
    """
    Testing 'ComplexAlias' as a valid complex number implementation.
    """
    self.assertIs(ComplexAlias.x, ComplexAlias.RE)
    self.assertIs(ComplexAlias.REAL, ComplexAlias.RE)
    self.assertIs(ComplexAlias.x, ComplexAlias.REAL)
    self.assertIs(ComplexAlias.y, ComplexAlias.IM)
    self.assertIs(ComplexAlias.IMAG, ComplexAlias.IM)
    self.assertIs(ComplexAlias.y, ComplexAlias.IMAG)

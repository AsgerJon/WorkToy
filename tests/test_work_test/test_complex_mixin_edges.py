"""
TestComplexMixinEdges subclasses 'BaseTest' and pins three edges of
'ComplexMixin'. Dividing by a small nonzero number used to raise
'ZeroDivisionError', since the divisor was compared with machine epsilon
rather than with zero. A third component given to the constructor was
dropped without a word, and is now refused. Equality took tuples and
strings, through the coercion the arithmetic uses, while the hash is
that of the builtin 'complex', so equal objects hashed apart; equality
now takes numbers and other implementations alone, which hash alike.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.work_test import BaseTest

from . import SimpleComplex


class TestComplexMixinEdges(BaseTest):
  """
  TestComplexMixinEdges provides tests for edge cases of 'ComplexMixin'.
  """

  def test_small_divisor(self) -> None:
    """Dividing by a small nonzero number works."""
    result = SimpleComplex(1, 0) / SimpleComplex(1e-9, 0)
    self.assertAlmostEqual(result.REAL / 1e9, 1.0)
    reflected = 1 / SimpleComplex(1e-9, 0)
    self.assertAlmostEqual(reflected.REAL / 1e9, 1.0)

  def test_zero_divisor(self) -> None:
    """Dividing by zero still raises 'ZeroDivisionError'."""
    with self.assertRaises(ZeroDivisionError):
      _ = SimpleComplex(1, 1) / SimpleComplex(0, 0)
    with self.assertRaises(ZeroDivisionError):
      _ = 1 / SimpleComplex(0, 0)

  def test_third_component_refused(self) -> None:
    """A third component raises 'TypeError'."""
    with self.assertRaises(TypeError):
      SimpleComplex(1, 2, 3)

  def test_equality_follows_hash(self) -> None:
    """Equal objects hash alike: numbers compare, tuples and strings do
    not."""
    z = SimpleComplex(1, 2)
    self.assertEqual(z, 1 + 2j)
    self.assertEqual(hash(z), hash(1 + 2j))
    self.assertEqual(SimpleComplex(3, 0), 3)
    self.assertEqual(hash(SimpleComplex(3, 0)), hash(3))
    self.assertNotEqual(z, (1, 2))
    self.assertNotEqual(z, '1+2j')

  def test_arithmetic_still_coerces(self) -> None:
    """Arithmetic still takes a tuple."""
    result = SimpleComplex(1, 2) + (1, 1)
    self.assertEqual((result.REAL, result.IMAG), (2.0, 3.0))

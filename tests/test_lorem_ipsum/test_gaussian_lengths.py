"""
TestGaussianLengths tests the 'GaussianLengths' distribution.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.lorem_ipsum import GaussianLengths
from . import LoremIpsumTest


class TestGaussianLengths(LoremIpsumTest):
  """
  TestGaussianLengths checks that 'GaussianLengths' reports the statistics
  it was constructed with, rejects inconsistent ones, and keeps every draw
  inside its bounds.
  """

  def test_statistics(self) -> None:
    """The four statistics are reported back as constructed."""
    dist = GaussianLengths(40, 15, 10, 70)
    self.assertEqual(dist.mean, 40.0)
    self.assertEqual(dist.var, 15.0)
    self.assertEqual(dist.minVal, 10)
    self.assertEqual(dist.maxVal, 70)

  def test_mean_below_min_rejected(self) -> None:
    """A mean below the lower bound is rejected at construction."""
    with self.assertRaises(ValueError):
      GaussianLengths(5, 1, 10, 70)

  def test_mean_above_max_rejected(self) -> None:
    """A mean above the upper bound is rejected at construction."""
    with self.assertRaises(ValueError):
      GaussianLengths(100, 1, 10, 70)

  def test_negative_variance_rejected(self) -> None:
    """A negative variance is rejected at construction."""
    with self.assertRaises(ValueError):
      GaussianLengths(40, -1, 10, 70)

  def test_sample_in_bounds(self) -> None:
    """Every draw lands within '[minVal, maxVal]'."""
    dist = GaussianLengths(40, 15, 10, 70)
    for _ in range(1000):
      value = dist.sampleInteger()
      self.assertGreaterEqual(value, 10)
      self.assertLessEqual(value, 70)

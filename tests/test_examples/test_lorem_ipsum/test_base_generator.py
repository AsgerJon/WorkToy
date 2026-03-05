"""
TestBaseGenerator tests the 'BaseGenerator' class from the
'worktoy.examples.lorem_ipsum' package.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from random import randint
from typing import TYPE_CHECKING
from worktoy.lorem_ipsum import BaseGenerator

from . import LoremIpsumTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias

  Result: TypeAlias = tuple[float, float]


class TestBaseGenerator(LoremIpsumTest):
  """
  TestBaseGenerator provides tests for the 'BaseGenerator' class from the
  'worktoy.examples.lorem_ipsum' package.
  """

  def setUp(self) -> None:
    super().setUp()
    self.sampleSize = 2 ** 8

  def test_init(self) -> None:
    """
    Testing that the 'BaseGenerator' initializes correctly.
    """
    for _ in range(16):
      count = randint(69, 420)
      generator = BaseGenerator(count)
      self.assertIsInstance(generator, BaseGenerator)
      self.assertEqual(generator.charCount, count)

  def roll_log_normal(self, mean: float, var: float) -> Result:
    """
    Roll a log-normal distribution with the given mean and variance.
    """
    n = self.sampleSize
    mean, var = float(mean), float(var)
    samples = [BaseGenerator.logNormal(mean, var, ) for _ in range(n)]
    observedMean = sum(samples) / n
    observedVariance = sum((x - observedMean) ** 2 for x in samples) / n
    return observedMean, observedVariance

  def test_log_normal(self, ) -> None:
    """
    Testing that the 'BaseGenerator' log-normal distribution is correctly
    implemented.
    """
    mean, var = 10., 1.
    vars_ = []
    for _ in range(2 ** 8):
      observedMean, observedVariance = self.roll_log_normal(mean, var)
      self.assertLessEqual(mean - 6 * var, observedMean, )
      self.assertLessEqual(observedMean, mean + 6 * var, )
      vars_.append(observedVariance)
    vars_.sort()
    minIndex = int(round(0.025 * len(vars_)))
    maxIndex = int(round(0.975 * len(vars_)))
    self.assertLess(var / 2, vars_[minIndex], )
    self.assertLess(vars_[maxIndex], var * 2, )

  def test_reduce_sum(self, ) -> None:
    """
    Testing that the 'BaseGenerator' reduceSum method correctly reduces the
    sum of a list of integers.
    """
    for i in (7 / 8, 9 / 8):
      lengths = [*(randint(15, 30) for _ in range(16)), ]
      targetSum = int(round(sum(lengths) * i))
      minVal = 15
      maxVal = 30

      adjusted = BaseGenerator.scaleSum(lengths, targetSum, minVal, maxVal)
      self.assertEqual(sum(adjusted), targetSum)

"""
TestBaseGenerator tests the 'BaseGenerator' class from the
'worktoy.examples.lorem_ipsum' package.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from random import randint
from typing import TYPE_CHECKING

from worktoy.lorem_ipsum import BaseGenerator
from worktoy.lorem_ipsum import Clause, Sentence, Paragraph
from worktoy.waitaminute import TypeException
from worktoy.waitaminute.lorem_ipsum import CharCountException
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

    blank = BaseGenerator()
    self.assertIsInstance(blank, BaseGenerator)
    expectedCount = BaseGenerator.charCount.getPosArgs()[0]
    actualCount = blank.charCount
    self.assertEqual(expectedCount, actualCount)

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

  def test_min_char_count(self) -> None:
    """
    Testing that a 'charCount' below the generator's minimum raises
    'CharCountException', while the minimum itself constructs cleanly.
    The floors differ per generator because each is built from a
    larger sub-unit than the one below it.
    """
    cases = [(Clause, 12), (Sentence, 40), (Paragraph, 80)]
    for generator, floor in cases:
      with self.assertRaises(CharCountException) as context:
        generator(floor - 1)
      e = context.exception
      self.assertEqual(str(e), repr(e))
      self.assertIs(e.generator, generator)
      self.assertEqual(e.charCount, floor - 1)
      self.assertEqual(e.minCount, floor)
      self.assertIsInstance(generator(floor), generator)

  def test_set_below_floor(self) -> None:
    """
    Testing that the 'charCount' floor is enforced on direct assignment
    too, not only at construction, via the descriptor's preSet hook.
    """
    clause = Clause(40)
    with self.assertRaises(CharCountException):
      clause.charCount = 3
    #  A whole-number float must not slip below the floor through the
    #  lossless 'float -> int' cast.
    with self.assertRaises(CharCountException):
      clause.charCount = 3.0
    #  A non-numeric value falls through to the normal type handling.
    with self.assertRaises(TypeException):
      clause.charCount = 'not a number'
    #  An in-range assignment still works.
    clause.charCount = 50
    self.assertEqual(clause.charCount, 50)

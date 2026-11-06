"""
TestGaussianLengths tests 'GaussianLengths' from 'worktoy.lorem_ipsum'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.lorem_ipsum import GaussianLengths, StochasticVariable
from worktoy.mcls import BaseObject
from worktoy.waitaminute import TypeException
from worktoy.work_test.samplers import IntSampler
from . import LoremTest


class TestGaussianLengths(LoremTest):
  """
  'GaussianLengths' states a distribution in four numbers held in boxes.
  The tests pin what the boxes keep and cast, the refusals of the
  constructor and of the boxes, a retuning after construction, and the
  draws staying within the bounds.
  """

  def test_keeps_and_widens(self) -> None:
    dist = GaussianLengths(40, 15, 12, 70)
    self.assertEqual(dist.mean, 40.0)
    self.assertIs(type(dist.mean), float)
    self.assertEqual(dist.var, 15.0)
    self.assertIs(type(dist.var), float)
    self.assertEqual(dist.minVal, 12)
    self.assertEqual(dist.maxVal, 70)
    self.assertIsInstance(dist, StochasticVariable)
    self.assertIsInstance(dist, BaseObject)

  def test_text_refused(self) -> None:
    with self.assertRaises(TypeException) as context:
      GaussianLengths('a', 1, 0, 10)
    self.assertEqual(context.exception.varName, 'mean')
    self.assertEqual(context.exception.actualObject, 'a')
    self.assertIs(context.exception.actualType, str)
    self.assertEqual(context.exception.expectedTypes, (float,))
    self.assertIn("'mean' to be an instance of 'float'",
                  str(context.exception))
    with self.assertRaises(TypeException) as context:
      GaussianLengths(5, 1, 0.5, 10)
    self.assertEqual(context.exception.varName, 'minVal')
    self.assertEqual(context.exception.actualObject, 0.5)
    self.assertIs(context.exception.actualType, float)
    self.assertEqual(context.exception.expectedTypes, (int,))
    self.assertIn("'minVal' to be an instance of 'int'",
                  str(context.exception))
    with self.assertRaises(TypeException) as context:
      GaussianLengths(5, 1, 0, '10')
    self.assertEqual(context.exception.varName, 'maxVal')
    self.assertEqual(context.exception.actualObject, '10')
    self.assertIs(context.exception.actualType, str)
    self.assertEqual(context.exception.expectedTypes, (int,))
    self.assertIn("'maxVal' to be an instance of 'int'",
                  str(context.exception))

  def test_mean_outside_bounds_refused(self) -> None:
    with self.assertRaises(ValueError) as context:
      GaussianLengths(100, 1, 0, 10)
    self.assertIn("Mean '100.0' must lie within the bounds '[0, 10]'",
                  str(context.exception))
    with self.assertRaises(ValueError) as context:
      GaussianLengths(-1, 1, 0, 10)
    self.assertIn("Mean '-1.0' must lie within the bounds '[0, 10]'",
                  str(context.exception))
    GaussianLengths(0, 1, 0, 10)
    GaussianLengths(10, 1, 0, 10)

  def test_negative_variance_refused(self) -> None:
    with self.assertRaises(ValueError) as context:
      GaussianLengths(5, -1, 0, 10)
    self.assertIn("Variance must be non-negative, but received '-1.0'",
                  str(context.exception))
    self.assertEqual(GaussianLengths(5, 0, 0, 10).var, 0.0)

  def test_retuned(self) -> None:
    dist = GaussianLengths(5, 1, 1, 10)
    dist.mean = 8
    self.assertEqual(dist.mean, 8.0)
    dist.maxVal = 8
    draws = {dist.sampleInteger() for _ in range(32)}
    self.assertTrue(draws <= set(range(1, 9)))
    with self.assertRaises(TypeException) as context:
      dist.minVal = 'one'
    self.assertEqual(context.exception.varName, 'minVal')
    self.assertEqual(context.exception.actualObject, 'one')
    self.assertIs(context.exception.actualType, str)
    self.assertEqual(context.exception.expectedTypes, (int,))
    self.assertIn("'minVal' to be an instance of 'int'",
                  str(context.exception))
    self.assertEqual(dist.minVal, 1)

  def test_draws_within_bounds(self) -> None:
    dist = GaussianLengths(40, 15, 12, 70)
    for _ in range(64):
      draw = dist.sampleInteger()
      self.assertIsInstance(draw, int)
      self.assertTrue(12 <= draw <= 70)

  def test_random_distributions(self) -> None:
    self.randomInteger = IntSampler(1, 50, seed=self.__sampler_seed__)
    self.randomInteger.size = 6
    for low in self.randomInteger.row:
      high = low + 10
      dist = GaussianLengths(low + 5, 9, low, high)
      with self.subTest(low=low):
        values = dist.partition(low * 3)
        self.assertEqual(sum(values), low * 3)
        self.assertTrue(all(low <= v <= high for v in values))

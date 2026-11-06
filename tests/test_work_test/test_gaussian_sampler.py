"""
TestGaussianSampler tests 'GaussianSampler' from
'worktoy.work_test.samplers'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from math import isfinite

from worktoy.waitaminute import TypeException
from worktoy.waitaminute.dispatch import DispatchException
from worktoy.work_test.samplers import GaussianSampler
from . import WorkTestTest


class TestGaussianSampler(WorkTestTest):
  """
  'GaussianSampler' draws normally distributed floats around a mean with
  a spread, the standard normal unless set otherwise, and refuses a mean
  or a deviation that is not finite and a negative deviation before the
  box stores it. The tests pin the defaults, the three constructors with
  and without keywords after them, every synonym, each refusal with its
  text, the two texts, and the draws of a seeded sampler.
  """

  def test_defaults(self) -> None:
    sampler = GaussianSampler()
    self.assertEqual((sampler.mean, sampler.stdDev), (0.0, 1.0))
    self.assertIs(sampler.valueType, float)
    self.assertEqual(repr(sampler), 'GaussianSampler(mean=0.0, stdDev=1.0,'
                                    ' colCount=1, rowCount=1, seed=None)')
    self.assertEqual(str(sampler),
                     '<GaussianSampler (mean: 0.000000, stdDev: 1.000000)>')

  def test_constructors(self) -> None:
    both = GaussianSampler(2.0, 0.5)
    self.assertEqual((both.mean, both.stdDev), (2.0, 0.5))
    one = GaussianSampler(2.0)
    self.assertEqual((one.mean, one.stdDev), (2.0, 1.0))
    cast = GaussianSampler(2)
    self.assertEqual((cast.mean, cast.stdDev), (2.0, 1.0))
    self.assertIs(type(cast.mean), float)
    self.assertEqual(GaussianSampler(2.0, 0.5, seed=1).seed, 1)
    self.assertEqual(GaussianSampler(2.0, size=3).colCount, 3)
    means = ('mean', 'average', 'avg', 'mean_value', 'meanValue')
    for key in means:
      with self.subTest(key=key):
        self.assertEqual(GaussianSampler(**{key: 5}).mean, 5.0)
    spreads = ('stdDev', 'std_dev', 'stdDeviation', 'std_deviation',
               'stdDevValue', 'std_dev_value', 'stdDeviationValue')
    for key in spreads:
      with self.subTest(key=key):
        self.assertEqual(GaussianSampler(**{key: 7}).stdDev, 7.0)
    self.assertEqual(GaussianSampler(stdDev=0).stdDev, 0.0)
    self.assertEqual(str(GaussianSampler(2.5, 0.25)),
                     '<GaussianSampler (mean: 2.500000, stdDev: 0.250000)>')

  def test_refusals(self) -> None:
    with self.assertRaises(ValueError) as context:
      GaussianSampler(mean=float('inf'))
    self.assertEqual(str(context.exception),
                     "Mean must be a finite number, but received: 'inf'!")
    with self.assertRaises(ValueError) as context:
      GaussianSampler(float('nan'))
    self.assertEqual(str(context.exception),
                     "Mean must be a finite number, but received: 'nan'!")
    with self.assertRaises(ValueError) as context:
      GaussianSampler(stdDev=-1)
    self.assertEqual(str(context.exception), 'Standard deviation must be '
                                             'a non-negative number, but '
                                             "received: '-1'!")
    with self.assertRaises(ValueError) as context:
      GaussianSampler(0.0, -1.0)
    self.assertEqual(str(context.exception), 'Standard deviation must be '
                                             'a non-negative number, but '
                                             "received: '-1.0'!")
    with self.assertRaises(ValueError) as context:
      GaussianSampler(stdDev=float('nan'))
    self.assertEqual(str(context.exception), 'Standard deviation must be '
                                             'a finite number, but '
                                             "received: 'nan'!")
    with self.assertRaises(TypeException) as context:
      GaussianSampler(stdDev='x')
    self.assertTypeRefused(context.exception, 'stdDev', 'x', float)
    with self.assertRaises(TypeException) as context:
      GaussianSampler(mean='x')
    self.assertTypeRefused(context.exception, 'mean', 'x', float)
    sampler = GaussianSampler()
    with self.assertRaises(ValueError) as context:
      sampler.stdDev = -0.5
    self.assertIn("received: '-0.5'", str(context.exception))
    self.assertEqual((sampler.mean, sampler.stdDev), (0.0, 1.0))
    with self.assertRaises(DispatchException) as context:
      GaussianSampler('x')
    self.assertIs(context.exception.dispatch,
                  GaussianSampler.__dict__['__init__'])
    self.assertEqual(context.exception.posArgs, ('x',))
    self.assertEqual(context.exception.keyArgs, {})
    self.assertIn("no overload of 'GaussianSampler.__init__' accepts",
                  str(context.exception))

  def test_draws(self) -> None:
    sampler = GaussianSampler(5.0, 1.0, seed=2, size=200)
    row = sampler.row
    self.assertEqual(row, GaussianSampler(5.0, 1.0, size=200, seed=2).row)
    for value in row:
      self.assertIs(type(value), float)
      self.assertTrue(isfinite(value))
    self.assertAlmostEqual(sum(row) / len(row), 5.0, delta=0.5)
    self.assertEqual(GaussianSampler(3.0, 0.0, size=3).row, (3.0, 3.0, 3.0))

  def test_random_draws(self) -> None:
    self.randomGaussian.size = 20
    for value in self.randomGaussian.row:
      with self.subTest(value=value):
        self.assertTrue(isfinite(value))
    self.assertEqual(self.randomGaussian.seed, self.__sampler_seed__)

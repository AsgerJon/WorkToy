"""
TestFloatSampler tests 'FloatSampler' from 'worktoy.work_test.samplers'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.waitaminute import TypeException
from worktoy.waitaminute.dispatch import DispatchException
from worktoy.work_test.samplers import FloatSampler, IntSampler
from . import WorkTestTest


class TestFloatSampler(WorkTestTest):
  """
  'FloatSampler' draws real numbers from an interval named as an integer
  range is named, with the bounds declared again as floats, so a pair of
  integers reaches them through the inherited signatures and is cast.
  The tests pin the defaults, the positional constructors of both kinds,
  the ordering of a pair, of a lone keyword and of an assignment through
  the notifier registered again on the float boxes, the refusals, and
  the draws within the interval.
  """

  def test_defaults(self) -> None:
    sampler = FloatSampler()
    self.assertIsInstance(sampler, IntSampler)
    self.assertEqual(self._bounds(sampler), (0.0, 1.0))
    self.assertIs(type(sampler.minVal), float)
    self.assertIs(sampler.valueType, float)
    self.assertEqual(repr(sampler), 'FloatSampler(minVal=0.0, maxVal=1.0, '
                                    'colCount=1, rowCount=1, seed=None)')
    self.assertEqual(str(sampler), "<FloatSampler: 'float' (1, 1)>")

  def test_positional_constructors(self) -> None:
    self.assertEqual(self._bounds(FloatSampler(1.5, 2.5)), (1.5, 2.5))
    self.assertEqual(self._bounds(FloatSampler(2.0, 1.0)), (1.0, 2.0))
    self.assertEqual(self._bounds(FloatSampler(3.0)), (0.0, 3.0))
    self.assertEqual(self._bounds(FloatSampler(-3.0)), (-3.0, 0.0))
    self.assertEqual(self._bounds(FloatSampler(1, 6)), (1.0, 6.0))
    self.assertEqual(self._bounds(FloatSampler(3)), (0.0, 3.0))
    self.assertIs(type(FloatSampler(1, 6).maxVal), float)
    self.assertEqual(self._bounds(FloatSampler(5.0, minVal=2.0)),
                     (2.0, 5.0))
    two = FloatSampler(1.0, 2.0, seed=3)
    self.assertEqual(two.seed, 3)
    one = FloatSampler(2.0, size=3)
    self.assertEqual((self._bounds(one), one.colCount), ((0.0, 2.0), 3))

  def test_keywords_and_assignment(self) -> None:
    self.assertEqual(self._bounds(FloatSampler(min=0.5, max=0.25)),
                     (0.25, 0.5))
    self.assertEqual(self._bounds(FloatSampler(maxVal=0.5)), (0.0, 0.5))
    self.assertEqual(self._bounds(FloatSampler(minVal=2)), (1.0, 2.0))
    sampler = FloatSampler()
    sampler.minVal = 5
    self.assertEqual(self._bounds(sampler), (1.0, 5.0))
    self.assertIs(type(sampler.maxVal), float)
    sampler.maxVal = 0.5
    self.assertEqual(self._bounds(sampler), (0.5, 1.0))
    sampler.maxVal = 7.5
    self.assertEqual(self._bounds(sampler), (0.5, 7.5))

  def test_refusals(self) -> None:
    with self.assertRaises(TypeException) as context:
      FloatSampler(minVal='x')
    self.assertTypeRefused(context.exception, 'minVal', 'x', float)
    sampler = FloatSampler()
    with self.assertRaises(TypeException) as context:
      sampler.maxVal = 'y'
    self.assertTypeRefused(context.exception, 'maxVal', 'y', float)
    self.assertEqual(self._bounds(sampler), (0.0, 1.0))
    with self.assertRaises(DispatchException) as context:
      FloatSampler('a')
    self.assertIs(context.exception.dispatch,
                  FloatSampler.__dict__['__init__'])
    self.assertEqual(context.exception.posArgs, ('a',))
    self.assertEqual(context.exception.keyArgs, {})
    self.assertIn("no overload of 'FloatSampler.__init__' accepts",
                  str(context.exception))
    self.assertIn('<TypeSig: [float, float]>', str(context.exception))

  def test_draws(self) -> None:
    sampler = FloatSampler(2.0, 3.0, seed=5, size=50)
    row = sampler.row
    self.assertEqual(row, FloatSampler(2.0, 3.0, size=50, seed=5).row)
    for value in row:
      self.assertIs(type(value), float)
      self.assertGreaterEqual(value, 2.0)
      self.assertLess(value, 3.0)
    self.assertEqual(len(set(row)), 50)
    flat = FloatSampler(4.0, 4.0, size=3)
    self.assertEqual(flat.row, (4.0, 4.0, 4.0))

  def test_random_draws(self) -> None:
    self.randomFloat.size = 20
    for value in self.randomFloat.row:
      with self.subTest(value=value):
        self.assertGreaterEqual(value, 0.0)
        self.assertLess(value, 1.0)
    self.assertEqual(self.randomFloat.seed, self.__sampler_seed__)

  @staticmethod
  def _bounds(sampler: FloatSampler) -> tuple:
    """The two bounds of the sampler as a pair."""
    return sampler.minVal, sampler.maxVal

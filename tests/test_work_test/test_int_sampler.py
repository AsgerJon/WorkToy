"""
TestIntSampler tests 'IntSampler' from 'worktoy.work_test.samplers'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.waitaminute import TypeException
from worktoy.waitaminute.dispatch import DispatchException
from worktoy.work_test.samplers import IntSampler
from . import WorkTestTest


class TestIntSampler(WorkTestTest):
  """
  'IntSampler' draws integers from a range named once, by position or by
  any spelling of the bounds, and keeps the pair ordered at every write.
  The tests pin the defaults, the three positional constructors with and
  without keywords after them, every synonym, the ordering of a pair, of
  a lone keyword and of an assignment, the refusals, the draws within
  the bounds, and the repeat of a seeded sampler.
  """

  def test_defaults(self) -> None:
    sampler = IntSampler()
    self.assertEqual((sampler.minVal, sampler.maxVal), (0, 255))
    self.assertIs(sampler.valueType, int)
    self.assertEqual(repr(sampler), 'IntSampler(minVal=0, maxVal=255, '
                                    'colCount=1, rowCount=1, seed=None)')
    self.assertEqual(str(sampler), "<IntSampler: 'int' (1, 1)>")
    self.assertFalse(sampler.__bounds_pending__)

  def test_positional_constructors(self) -> None:
    self.assertEqual(self._bounds(IntSampler(1, 6)), (1, 6))
    self.assertEqual(self._bounds(IntSampler(6, 1)), (1, 6))
    self.assertEqual(self._bounds(IntSampler(5)), (0, 5))
    self.assertEqual(self._bounds(IntSampler(-5)), (-5, 0))
    self.assertEqual(self._bounds(IntSampler(1.0, 6.0)), (1, 6))
    self.assertIs(type(IntSampler(1.0, 6.0).minVal), int)
    two = IntSampler(1, 6, seed=3, size=4)
    self.assertEqual((two.seed, two.colCount), (3, 4))
    one = IntSampler(5, count=2)
    self.assertEqual((self._bounds(one), one.rowCount), ((0, 5), 2))

  def test_keyword_bounds(self) -> None:
    lows = ('minVal', 'minimum', 'min', 'min_value', 'minValue')
    highs = ('maxVal', 'maximum', 'max', 'max_value', 'maxValue')
    for key in lows:
      with self.subTest(key=key):
        self.assertEqual(self._bounds(IntSampler(**{key: 7})), (7, 255))
    for key in highs:
      with self.subTest(key=key):
        self.assertEqual(self._bounds(IntSampler(**{key: 7})), (0, 7))
    self.assertEqual(self._bounds(IntSampler(minVal=9, maxVal=2)), (2, 9))
    self.assertEqual(self._bounds(IntSampler(min=2, max=9)), (2, 9))
    self.assertEqual(self._bounds(IntSampler(minVal=300)), (255, 300))
    self.assertEqual(self._bounds(IntSampler(maxVal=-5)), (-5, 0))
    self.assertEqual(self._bounds(IntSampler(minVal=2.0)), (2, 255))

  def test_assignment_keeps_the_pair_ordered(self) -> None:
    sampler = IntSampler(1, 6)
    sampler.minVal = 10
    self.assertEqual(self._bounds(sampler), (6, 10))
    sampler.maxVal = 0
    self.assertEqual(self._bounds(sampler), (0, 6))
    sampler.maxVal = 6
    self.assertEqual(self._bounds(sampler), (0, 6))
    sampler._setBounds(9, 3)
    self.assertEqual(self._bounds(sampler), (3, 9))
    self.assertFalse(sampler.__bounds_pending__)
    sampler._setBounds(3.0, 9.0)
    self.assertEqual(self._bounds(sampler), (3, 9))

  def test_refusals(self) -> None:
    with self.assertRaises(TypeException) as context:
      IntSampler(minVal=2.5)
    self.assertTypeRefused(context.exception, 'minVal', 2.5, int)
    with self.assertRaises(TypeException) as context:
      IntSampler(maxVal='x')
    self.assertTypeRefused(context.exception, 'maxVal', 'x', int)
    sampler = IntSampler(1, 6)
    with self.assertRaises(TypeException) as context:
      sampler.minVal = None
    self.assertTypeRefused(context.exception, 'minVal', None, int)
    self.assertEqual(self._bounds(sampler), (1, 6))
    for args in (('1',), (1.5,), (1, 2, 3)):
      with self.subTest(args=args):
        with self.assertRaises(DispatchException) as context:
          IntSampler(*args)
        self.assertIs(context.exception.dispatch,
                      IntSampler.__dict__['__init__'])
        self.assertEqual(context.exception.posArgs, args)
        self.assertEqual(context.exception.keyArgs, {})
        self.assertIn("no overload of 'IntSampler.__init__' accepts",
                      str(context.exception))
        self.assertIn('<TypeSig: [int, int]>', str(context.exception))

  def test_draws(self) -> None:
    sampler = IntSampler(1, 6, seed=3, size=5)
    row = sampler.row
    self.assertEqual(row, IntSampler(1, 6, size=5, randomSeed=3).row)
    self.assertEqual(len(row), 5)
    for value in row:
      self.assertIn(value, range(1, 7))
      self.assertIs(type(value), int)
    self.assertIn(sampler(), range(1, 7))
    table = IntSampler(3, 4, size=2, count=3, seed=1).table
    self.assertEqual(table, ((3, 3), (4, 3), (4, 4)))
    self.assertEqual(table, IntSampler(3, 4, size=2, count=3, seed=1).table)
    narrow = IntSampler(7, 7, size=4)
    self.assertEqual(narrow.row, (7, 7, 7, 7))

  def test_random_draws(self) -> None:
    self.randomInteger.size = 20
    for value in self.randomInteger.row:
      with self.subTest(value=value):
        self.assertIn(value, range(256))
    self.assertEqual(self.randomInteger.seed, self.__sampler_seed__)
    fresh = IntSampler(seed=self.__sampler_seed__, size=20)
    self.randomInteger.seed = self.__sampler_seed__
    self.assertEqual(self.randomInteger.row, fresh.row)

  @staticmethod
  def _bounds(sampler: IntSampler) -> tuple:
    """The two bounds of the sampler as a pair."""
    return sampler.minVal, sampler.maxVal

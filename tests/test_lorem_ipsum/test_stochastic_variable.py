"""
TestStochasticVariable tests 'StochasticVariable' from
'worktoy.lorem_ipsum'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.lorem_ipsum import StochasticVariable, GaussianLengths
from worktoy.work_test.samplers import IntSampler
from . import LoremTest


class TestStochasticVariable(LoremTest):
  """
  'StochasticVariable' cuts a total into values a distribution could
  have drawn, over the four statistics a subclass holds. The tests
  drive the cutting on a 'GaussianLengths', whose statistics are plain
  numbers: the clamp, the two passes of the settling with an explicit
  order, the choice of the count with every bound it is held to, the
  refusals, and the two partitions.
  """

  def setUp(self) -> None:
    LoremTest.setUp(self)
    self.dist = GaussianLengths(5, 1, 1, 10)

  def test_statistics_are_the_subclass_own(self) -> None:
    with self.assertRaises(AttributeError):
      StochasticVariable().sampleInteger()

    class Bare(StochasticVariable):
      """Declares no statistics."""

    with self.assertRaises(AttributeError):
      Bare().partition(3)

  def test_clamp(self) -> None:
    self.assertEqual(self.dist._clamp(0), 1)
    self.assertEqual(self.dist._clamp(1), 1)
    self.assertEqual(self.dist._clamp(5), 5)
    self.assertEqual(self.dist._clamp(10), 10)
    self.assertEqual(self.dist._clamp(11), 10)

  def test_sample_integer(self) -> None:
    exact = GaussianLengths(5, 0, 1, 10)
    self.assertEqual({exact.sampleInteger() for _ in range(16)}, {5})
    wide = GaussianLengths(5, 1000000, 4, 6)
    draws = {wide.sampleInteger() for _ in range(64)}
    self.assertTrue(draws <= {4, 5, 6})
    self.assertTrue({4, 6} <= draws)

  def test_spread(self) -> None:
    values = [5, 5, 5]
    self.assertEqual(self.dist._spread(values, [0, 1, 2], 0), 0)
    self.assertEqual(values, [5, 5, 5])
    values = [5, 5]
    self.assertEqual(self.dist._spread(values, [0, 1], 3), 0)
    self.assertEqual(values, [7, 6])
    values = [10, 2]
    self.assertEqual(self.dist._spread(values, [0, 1], 11), 3)
    self.assertEqual(values, [10, 10])
    values = [2, 2]
    self.assertEqual(self.dist._spread(values, [1, 0], -3), -1)
    self.assertEqual(values, [1, 1])

  def test_fill(self) -> None:
    values = [5, 5]
    self.assertEqual(self.dist._fill(values, [0, 1], 0), 0)
    self.assertEqual(values, [5, 5])
    values = [3, 3]
    self.assertEqual(self.dist._fill(values, [1, 0], 2), 0)
    self.assertEqual(values, [3, 5])
    values = [10, 10]
    self.assertEqual(self.dist._fill(values, [0, 1], 3), 3)
    self.assertEqual(values, [10, 10])
    values = [9, 2]
    self.assertEqual(self.dist._fill(values, [0, 1], 3), 0)
    self.assertEqual(values, [10, 4])

  def test_settle(self) -> None:
    values = [5, 5, 5]
    self.assertIs(self.dist._settle(values, 15), values)
    self.assertEqual(values, [5, 5, 5])
    values = [5, 5, 5]
    self.dist._settle(values, 20)
    self.assertEqual(sum(values), 20)
    self.assertTrue(all(1 <= v <= 10 for v in values))
    values = [5, 5]
    self.dist._settle(values, 3)
    self.assertEqual(sorted(values), [1, 2])
    values = [5, 5]
    self.dist._settle(values, 30)
    self.assertEqual(values, [10, 10])
    self.assertEqual(self.dist._settle([], 0), [])

  def test_count_for(self) -> None:
    self.assertEqual(self.dist._countFor(0, 0), 0)
    self.assertEqual(self.dist._countFor(0, 3), 0)
    self.assertEqual(self.dist._countFor(20, 0), 4)
    self.assertEqual(self.dist._countFor(100, 0), 20)
    self.assertEqual(self.dist._countFor(3, 0), 1)
    self.assertEqual(self.dist._countFor(1, 0), 1)
    self.assertEqual(self.dist._countFor(20, 5), 2)
    self.assertEqual(GaussianLengths(10, 1, 1, 10)._countFor(11, 0), 2)
    self.assertEqual(GaussianLengths(3, 1, 3, 10)._countFor(5, 0), 1)
    self.assertEqual(GaussianLengths(0, 1, 0, 3)._countFor(5, 0), 2)
    self.assertEqual(GaussianLengths(-1, 1, -2, 3)._countFor(5, 0), 2)

  def test_count_refused(self) -> None:
    with self.assertRaises(ValueError) as context:
      self.dist.partition(-1)
    self.assertIn('cannot cut -1 into values from 1 to 10:',
                  str(context.exception))
    self.assertNotIn('separator', str(context.exception))
    wide = GaussianLengths(40, 15, 12, 70)
    with self.assertRaises(ValueError) as context:
      wide.partitionSpaced(1, 2)
    self.assertIn('from 12 to 70, each with 2 more for its separator',
                  str(context.exception))
    with self.assertRaises(ValueError) as context:
      GaussianLengths(-2, 1, -3, -1).partition(5)
    self.assertIn("'GaussianLengths' cannot cut 5 into values from -3 to "
                  "-1: no number of such values adds up to it",
                  str(context.exception))
    with self.assertRaises(ValueError) as context:
      GaussianLengths(5.5, 1, 5, 6).partitionSpaced(8, 1)
    self.assertIn("'GaussianLengths' cannot cut 8", str(context.exception))

  def test_partition(self) -> None:
    self.assertEqual(self.dist.partition(0), [])
    values = self.dist.partition(23)
    self.assertEqual(sum(values), 23)
    self.assertTrue(all(1 <= v <= 10 for v in values))
    self.assertEqual(self.dist.partition(1), [1])
    self.assertEqual(sum(self.dist.partition(10)), 10)
    self.assertEqual(len(self.dist.partition(10)), 2)

  def test_partition_spaced(self) -> None:
    self.assertEqual(self.dist.partitionSpaced(0), [])
    values = self.dist.partitionSpaced(23)
    self.assertEqual(sum(values) + len(values), 23)
    values = self.dist.partitionSpaced(50, 3)
    self.assertEqual(sum(values) + 3 * len(values), 50)
    self.assertTrue(all(1 <= v <= 10 for v in values))

  def test_random_targets(self) -> None:
    self.randomInteger = IntSampler(3, 200, seed=self.__sampler_seed__)
    self.randomInteger.size = 10
    for target in self.randomInteger.row:
      with self.subTest(target=target):
        self.assertEqual(sum(self.dist.partition(target)), target)
        spaced = self.dist.partitionSpaced(target, 2)
        self.assertEqual(sum(spaced) + 2 * len(spaced), target)

  def test_count_for_with_spacing(self) -> None:
    self.assertEqual(GaussianLengths(3, 1, 3, 10)._countFor(23, 1), 5)
    self.assertEqual(GaussianLengths(5, 1, 3, 10)._countFor(20, 1), 3)
    self.assertEqual(GaussianLengths(5, 1, 3, 10)._countFor(22, 1), 4)
    self.assertEqual(GaussianLengths(9, 1, 3, 9)._countFor(20, 1), 2)
    self.assertEqual(GaussianLengths(0, 1, 0, 3)._countFor(5, 1), 5)
    self.assertEqual(GaussianLengths(1, 1, 1, 1)._countFor(3, 0), 3)
    with self.assertRaises(ValueError) as context:
      GaussianLengths(0, 1, 0, 0)._countFor(3, 0)
    self.assertIn("cannot cut 3 into values from 0 to 0",
                  str(context.exception))
    with self.assertRaises(ValueError) as context:
      GaussianLengths(0, 1, 0, 3)._countFor(-5, 0)
    self.assertIn("cannot cut -5 into values from 0 to 3",
                  str(context.exception))

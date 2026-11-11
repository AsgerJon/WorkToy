"""
PromiseSamplers promises the random-data samplers of
'worktoy.work_test.samplers'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import random
from unittest import TestCase

from worktoy.desc import AttriBox
from worktoy.work_test.samplers import BaseSampler, IntSampler
from worktoy.work_test.samplers import loremSentence, randomWord, LOREM_WORDS


class PromiseSamplers(TestCase):
  """
  A sampler draws one value with 'item', a row of 'colCount' values with
  'row' and a table of 'rowCount' rows with 'table', each anew at every
  read, sizes set by keyword as 'width' or 'size' for a row and
  'height' or 'count' for a table too, a size below one raising
  'ValueError'. A sampler seeded with 'seed=' draws alike every time,
  from a generator of its own. 'IntSampler(lo, hi)' draws integers
  between the bounds, both included, and corrects a swapped pair. A
  keyword naming no setting raises 'TypeError'. A sampler of a project
  subclasses 'BaseSampler' with '_getValueType' and '_getItem', and its
  settings are boxes assigned after construction; one without both
  hooks cannot be instantiated. 'loremSentence(n)' gives a sentence of
  'n' characters, capitalized and closed by a period, and 'randomWord()'
  a word of 'LOREM_WORDS'; both draw from Python's 'random'. Source: the
  docstrings of the 'samplers' package,
  'BaseSampler', 'IntSampler' and 'SamplerMeta'.
  """

  def test_shapes(self) -> None:
    sampler = IntSampler(1, 6, width=4, height=3)
    self.assertIn(sampler.item, range(1, 7))
    self.assertEqual(len(sampler.row), 4)
    self.assertEqual([len(row) for row in sampler.table], [4, 4, 4])
    with self.assertRaises(ValueError):
      IntSampler(1, 6, count=0)

  def test_fresh_draws_and_aliases(self) -> None:
    sampler = IntSampler(1, 1000)
    self.assertGreater(len({sampler.item for _ in range(50)}), 1)
    self.assertEqual(len(IntSampler(1, 6, size=5).row), 5)
    self.assertEqual(len(IntSampler(1, 6, count=3).table), 3)

  def test_bounds(self) -> None:
    sampler = IntSampler(6, 1, width=200)
    self.assertEqual((sampler.minVal, sampler.maxVal), (1, 6))
    self.assertEqual(set(sampler.row), set(range(1, 7)))

  def test_seed(self) -> None:
    first = IntSampler(0, 1000, seed=7, width=10).row
    second = IntSampler(0, 1000, seed=7, width=10).row
    self.assertEqual(first, second)

  def test_unknown_keyword(self) -> None:
    with self.assertRaises(TypeError):
      IntSampler(1, 6, colour='red')

  def test_own_sampler(self) -> None:
    class DieSampler(BaseSampler):
      sides = AttriBox[int](6)

      def _getValueType(self, **kwargs) -> type:
        return int

      def _getItem(self, *args, **kwargs) -> int:
        return self.random.randint(1, self.sides)

    class Broken(BaseSampler):
      pass

    die = DieSampler(seed=3)
    self.assertIn(die.item, range(1, 7))
    die.sides = 20
    self.assertEqual(die.sides, 20)
    with self.assertRaises(TypeError):
      Broken()

  def test_text(self) -> None:
    sentence = loremSentence(30)
    self.assertEqual(len(sentence), 30)
    self.assertTrue(sentence[0].isupper())
    self.assertTrue(sentence.endswith('.'))
    self.assertIn(randomWord(), LOREM_WORDS)
    random.seed(5)
    first = loremSentence(40)
    random.seed(5)
    self.assertEqual(loremSentence(40), first)

"""
TestStochasticWord tests 'StochasticWord' from 'worktoy.lorem_ipsum'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.lorem_ipsum import StochasticWord, StochasticVariable
from worktoy.lorem_ipsum import COMMON_WORDS, UNCOMMON_WORDS, RARE_WORDS
from worktoy.work_test.samplers import IntSampler
from . import LoremTest, Narrow


class TestStochasticWord(LoremTest):
  """
  'StochasticWord' is a word list read as a distribution over lengths
  and as a source of a word of any length it holds, analysed once at the
  class statement. The tests pin the statistics, the table by length,
  the three ways to draw, the refusal of a missing length, a subclass
  with words of its own, and the refusal of a gap at the class
  statement.
  """

  def test_statistics_at_the_class(self) -> None:
    tiers = ((COMMON_WORDS, 0.8), (UNCOMMON_WORDS, 0.15), (RARE_WORDS, 0.05))
    total = sum(len(words) * weight for words, weight in tiers)
    mean = sum(len(w) * weight for words, weight in tiers for w in words)
    mean = mean / total
    spread = sum((len(w) - mean) ** 2 * weight
                 for words, weight in tiers for w in words)
    self.assertAlmostEqual(StochasticWord.mean, mean)
    self.assertAlmostEqual(StochasticWord.var, spread / total)
    self.assertEqual(StochasticWord.minVal, 4)
    self.assertEqual(StochasticWord.maxVal, 12)
    self.assertIsSubclass(StochasticWord, StochasticVariable)
    word = StochasticWord()
    self.assertEqual((word.mean, word.minVal), (StochasticWord.mean, 4))

  def test_by_lengths(self) -> None:
    word = StochasticWord()
    table = word.byLengths
    self.assertEqual(sorted(table), [*range(4, 13)])
    every = {*COMMON_WORDS, *UNCOMMON_WORDS, *RARE_WORDS}
    self.assertEqual({w for words in table.values() for w in words}, every)
    for length, words in table.items():
      with self.subTest(length=length):
        self.assertIsInstance(words, tuple)
        self.assertTrue(all(len(w) == length for w in words))
    self.assertIsNot(word.byLengths, table)
    self.assertEqual(word.byLengths, table)

  def test_realize_length(self) -> None:
    word = StochasticWord()
    table = word.byLengths
    for length in range(4, 13):
      with self.subTest(length=length):
        drawn = word.realizeLength(length)
        self.assertEqual(len(drawn), length)
        self.assertIn(drawn, table[length])
        self.assertIn(word[length], table[length])

  def test_missing_length_refused(self) -> None:
    word = StochasticWord()
    for length in (3, 13, 0):
      with self.subTest(length=length):
        with self.assertRaises(IndexError) as context:
          word.realizeLength(length)
        self.assertEqual(str(context.exception),
                         "Found no words of length '%d'!" % length)
    with self.assertRaises(IndexError) as context:
      _ = word[2]
    self.assertEqual(str(context.exception), "Found no words of length '2'!")

  def test_realize(self) -> None:
    word = StochasticWord()
    every = {*COMMON_WORDS, *UNCOMMON_WORDS, *RARE_WORDS}
    lengths = set()
    for _ in range(64):
      drawn = word.realize()
      self.assertIn(drawn, every)
      lengths.add(len(drawn))
    self.assertTrue(lengths <= set(range(4, 13)))
    self.assertGreater(len(lengths), 1)

  def test_weights_favour_common_words(self) -> None:
    word = StochasticWord()
    common, other = 0, 0
    for _ in range(200):
      if word.realizeLength(6) in COMMON_WORDS:
        common += 1
      else:
        other += 1
    self.assertGreater(common, other)
    self.assertGreater(other, 0)

  def test_subclass_has_its_own(self) -> None:
    self.assertEqual(Narrow.minVal, 5)
    self.assertEqual(Narrow.maxVal, 6)
    self.assertAlmostEqual(Narrow.mean, 5.25)
    self.assertAlmostEqual(Narrow.var, 0.1875)
    self.assertEqual(Narrow().byLengths, {
      5: ('alpha', 'delta', 'gamma'), 6: ('zephyr', 'lambda'),
    })
    self.assertEqual(StochasticWord.minVal, 4)
    self.assertIn(Narrow()[6], ('zephyr', 'lambda'))
    with self.assertRaises(IndexError) as context:
      Narrow()[4]
    self.assertEqual(str(context.exception), "Found no words of length '4'!")

  def test_gap_refused_at_the_class_statement(self) -> None:
    with self.assertRaises(ValueError) as context:
      class Gappy(StochasticWord):
        __category_weights__ = ((('ab', 'abcd', 'abcdefg'), 1.0),)

    self.assertIn("'Gappy' has words of lengths from 2 to 7, but none of "
                  "length 3, 5 or 6.", str(context.exception))
    with self.assertRaises(ValueError) as context:
      class Lone(StochasticWord):
        __category_weights__ = ((('ab', 'abcd'), 1.0),)

    self.assertIn('none of length 3.', str(context.exception))
    StochasticWord._refuseGaps(2, 3, 4)
    with self.assertRaises(ValueError) as context:
      StochasticWord._refuseGaps(2, 4)
    self.assertIn("'StochasticWord' has words of lengths from 2 to 4, but "
                  "none of length 3.", str(context.exception))

  def test_random_lengths(self) -> None:
    self.randomInteger = IntSampler(4, 12, seed=self.__sampler_seed__)
    self.randomInteger.size = 10
    word = StochasticWord()
    for length in self.randomInteger.row:
      with self.subTest(length=length):
        self.assertEqual(len(word[length]), length)

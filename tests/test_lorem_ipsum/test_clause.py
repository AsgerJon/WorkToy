"""
TestClause tests 'Clause' from 'worktoy.lorem_ipsum'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.lorem_ipsum import Clause, StochasticWord
from worktoy.work_test.samplers import IntSampler
from . import LoremTest, Narrow, NarrowClause, Hailed


class TestClause(LoremTest):
  """
  A clause is words joined by single spaces at exactly the requested
  count, with a lead-in when first and a placeholder when too short for
  it. The tests pin the layout and its caches, the first clause and its
  short form, the refusals, the edits the sentence makes, the copy
  constructor, the renderings, and a word list and a lead-in of a
  project's own.
  """

  def test_layout(self) -> None:
    clause = Clause(30)
    words = clause.wordsArray
    lengths = clause.wordsLengths
    self.assertEqual(len(clause), 30)
    self.assertEqual(str(clause), ' '.join(words))
    self.assertEqual(repr(clause), ' '.join(words))
    self.assertEqual(clause.realize(), str(clause))
    self.assertEqual([*clause], words)
    self.assertEqual(lengths, [len(word) for word in words])
    self.assertEqual(sum(lengths) + len(lengths) - 1, 30)
    self.assertNotIn('  ', str(clause))
    every = {w for ws in StochasticWord().byLengths.values() for w in ws}
    self.assertTrue(all(word in every for word in words))
    self.assertFalse(clause.isFirst)
    self.assertEqual(Clause(4).wordsLengths, [4])
    self.assertEqual(len(Clause(4).wordsArray[0]), 4)

  def test_caches(self) -> None:
    clause = Clause(30)
    self.assertIsNone(clause.__words_lengths__)
    self.assertIsNone(clause.__words_array__)
    with self.assertRaises(RecursionError) as context:
      clause._getWordsLengths(_recursion=True)
    self.assertEqual(context.exception.args, ())
    with self.assertRaises(RecursionError) as context:
      clause._getWordsArray(_recursion=True)
    self.assertEqual(context.exception.args, ())
    words = clause.wordsArray
    self.assertIs(clause.wordsArray, words)
    self.assertIs(clause.wordsLengths, clause.wordsLengths)
    clause.clear()
    self.assertIsNone(clause.__words_lengths__)
    self.assertIsNone(clause.__words_array__)
    clause.reset()
    self.assertIsNotNone(clause.__words_array__)
    self.assertIsNot(clause.wordsArray, words)
    self.assertEqual(len(clause), 30)
    clause.charCount = 50
    self.assertIsNone(clause.__words_array__)
    self.assertEqual(len(clause), 50)
    clause.isFirst = True
    self.assertIsNone(clause.__words_lengths__)
    self.assertEqual(clause.wordsArray[:2], ['Lorem', 'ipsum'])

  def test_first(self) -> None:
    clause = Clause.first(16)
    self.assertEqual(clause.wordsArray[:2], ['Lorem', 'ipsum'])
    self.assertEqual(len(clause.wordsArray), 3)
    self.assertEqual(clause.wordsLengths, [5, 5, 4])
    self.assertEqual(len(clause), 16)
    self.assertFalse(clause._isShortFirst())
    long = Clause.first(40)
    self.assertTrue(str(long).startswith('Lorem ipsum '))
    self.assertEqual(len(long), 40)
    self.assertFalse(Clause(40)._isShortFirst())

  def test_short_first(self) -> None:
    clause = Clause.first(15)
    self.assertTrue(clause._isShortFirst())
    self.assertEqual(clause.wordsArray, ['Lorem', 'ipsum....'])
    self.assertEqual(clause.wordsLengths, [5, 9])
    self.assertEqual(str(clause), 'Lorem ipsum....')
    self.assertEqual(len(clause), 15)
    self.assertEqual(Clause.first(5).wordsArray, ['Lo...'])
    self.assertEqual(Clause.first(3).wordsArray, ['...'])
    self.assertEqual(Clause.first(0).wordsArray, [''])
    self.assertEqual(Clause.first(0).wordsLengths, [0])
    self.assertEqual(str(Clause.first(0)), '')
    self.assertEqual(len(Clause.first(0)), 0)
    self.assertEqual(Clause.first(11).wordsArray, ['Lorem', 'ip...'])
    self.assertEqual(Clause.first(15)._placeholderWords(),
                     ['Lorem', 'ipsum....'])

  def test_too_short_refused(self) -> None:
    for count in (0, 3):
      with self.subTest(count=count):
        with self.assertRaises(ValueError) as context:
          _ = Clause(count).wordsArray
        self.assertIn("cannot realize fewer than 4 characters, but received "
                      "a character count of %d" % count,
                      str(context.exception))
    with self.assertRaises(ValueError) as context:
      str(Clause(2))
    self.assertIn("A 'Clause' that is not a first clause cannot realize "
                  "fewer than 4 characters, but received a character "
                  "count of 2", str(context.exception))

  def test_unreachable_count_refused(self) -> None:
    with self.assertRaises(ValueError) as context:
      _ = NarrowClause(7).wordsArray
    self.assertIn("A 'Narrow' cannot cut 8 into values from 5 to 6, each "
                  "with 1 more for its separator", str(context.exception))
    self.assertEqual(NarrowClause(11).wordsLengths, [5, 5])
    self.assertEqual(len(NarrowClause(11)), 11)
    self.assertIsInstance(NarrowClause(11).stochWord, Narrow)
    self.assertIsInstance(Clause().stochWord, StochasticWord)
    self.assertEqual(NarrowClause(5).wordsLengths, [5])

  def test_lead_in_of_a_subclass(self) -> None:
    clause = Hailed.first(14)
    self.assertEqual(clause.wordsArray[:2], ['Ave', 'mundi'])
    self.assertEqual(clause.wordsLengths[:2], [3, 5])
    self.assertEqual(len(clause), 14)
    short = Hailed.first(13)
    self.assertEqual(short.wordsArray, ['Ave', 'mundi....'])
    self.assertEqual(short.wordsLengths, [3, 9])
    self.assertEqual(Clause.__lead_in__, ('Lorem', 'ipsum'))

  def test_edits_for_the_sentence(self) -> None:
    clause = Clause(30)
    words = clause.wordsArray
    first = words[0]
    clause.capitalizeLead()
    self.assertIs(clause.wordsArray, words)
    self.assertEqual(words[0], first.capitalize())
    last = words[-1]
    clause.terminate(',')
    self.assertEqual(words[-1], last + ',')
    self.assertEqual(len(clause), 31)
    self.assertTrue(str(clause).endswith(','))

  def test_copy_constructor(self) -> None:
    blank = Clause.first(30)
    copy = Clause(blank)
    self.assertEqual(copy.charCount, 30)
    self.assertTrue(copy.isFirst)
    self.assertIsNone(copy.__words_lengths__)
    self.assertIsNone(copy.__words_array__)
    built = Clause(25)
    words = built.wordsArray
    copy = Clause(built)
    self.assertEqual(copy.wordsArray, words)
    self.assertIsNot(copy.wordsArray, words)
    self.assertEqual(copy.wordsLengths, built.wordsLengths)
    self.assertIsNot(copy.wordsLengths, built.wordsLengths)
    self.assertFalse(copy.isFirst)
    self.assertEqual(str(copy), str(built))

  def test_random_counts(self) -> None:
    self.randomInteger = IntSampler(4, 120, seed=self.__sampler_seed__)
    self.randomInteger.size = 12
    for count in self.randomInteger.row:
      with self.subTest(count=count):
        self.assertEqual(len(Clause(count)), count)
        first = Clause.first(count + 12)
        self.assertEqual(len(first), count + 12)
        self.assertTrue(str(first).startswith('Lorem ipsum '))

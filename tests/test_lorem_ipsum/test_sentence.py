"""
TestSentence tests 'Sentence' from 'worktoy.lorem_ipsum'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.lorem_ipsum import Sentence, Clause, GaussianLengths
from worktoy.work_test.samplers import IntSampler
from . import LoremTest


class TestSentence(LoremTest):
  """
  A sentence is clauses joined by ', ' and closed by a period at exactly
  the requested count, its first word capitalized. The tests pin the
  layout and its arithmetic, the lead-in through 'first', the short
  sentence and its placeholder clause, the caches, the copy constructor
  and the renderings.
  """

  def test_layout(self) -> None:
    sentence = Sentence(90)
    clauses = sentence.clausesArray
    lengths = sentence.clausesLengths
    text = str(sentence)
    self.assertEqual(len(text), 90)
    self.assertEqual(len(sentence), 90)
    self.assertTrue(text.endswith('.'))
    self.assertTrue(text[0].isupper())
    self.assertEqual(text, ', '.join(str(c) for c in clauses))
    self.assertEqual(sum(lengths) + 2 * len(lengths), 91)
    self.assertEqual(sentence.realize(), text)
    self.assertEqual([*sentence], clauses)
    for clause, length in zip(clauses[:-1], lengths[:-1]):
      with self.subTest(length=length):
        self.assertIsInstance(clause, Clause)
        self.assertEqual(len(clause), length)
        self.assertNotIn(',', str(clause))
    self.assertEqual(len(clauses[-1]), lengths[-1] + 1)
    self.assertEqual(repr(sentence), '\n'.join(repr(c) for c in clauses))
    self.assertFalse(sentence.isFirst)

  def test_first(self) -> None:
    sentence = Sentence.first(90)
    self.assertTrue(str(sentence).startswith('Lorem ipsum '))
    self.assertTrue(sentence.clausesArray[0].isFirst)
    self.assertEqual(len(sentence), 90)
    plain = Sentence(90)
    plain.isFirst = True
    self.assertIsNone(plain.__clause_array__)
    self.assertTrue(str(plain).startswith('Lorem ipsum '))
    self.assertEqual(str(Sentence.first(15)), 'Lorem ipsum....')
    self.assertEqual(Sentence.first(15).clausesLengths, [14])

  def test_smallest_laid_out(self) -> None:
    sentence = Sentence(15)
    self.assertEqual(sentence.clausesLengths, [14])
    self.assertEqual(len(sentence), 15)
    self.assertTrue(str(sentence).endswith('.'))
    self.assertEqual(len(sentence.clausesArray), 1)
    self.assertNotEqual(str(sentence), 'Lorem Ipsum....')

  def test_short(self) -> None:
    sentence = Sentence(10)
    self.assertEqual(str(sentence), 'Lorem I...')
    self.assertEqual(sentence.clausesLengths, [10])
    clause = sentence.clausesArray[0]
    self.assertEqual(len(sentence.clausesArray), 1)
    self.assertEqual(clause.wordsArray, ['Lorem', 'I...'])
    self.assertEqual(clause.wordsLengths, [5, 4])
    self.assertEqual(clause.charCount, 10)
    self.assertEqual(len(sentence), 10)
    self.assertEqual(repr(sentence), 'Lorem I...')
    self.assertEqual(str(Sentence(14)), 'Lorem Ipsum...')
    self.assertEqual(str(Sentence(0)), '')
    self.assertEqual(len(Sentence(0)), 0)
    self.assertEqual(Sentence(0).clausesArray[0].wordsArray, [''])
    self.assertEqual(str(Sentence(3)), '...')

  def test_clause_distribution(self) -> None:
    sentence = Sentence()
    dist = sentence.clauseDist
    self.assertIsInstance(dist, GaussianLengths)
    self.assertEqual((dist.mean, dist.var, dist.minVal, dist.maxVal),
                     (40.0, 15.0, 12, 70))
    self.assertIs(sentence.clauseDist, dist)
    self.assertIsNot(Sentence().clauseDist, dist)

  def test_caches(self) -> None:
    sentence = Sentence(60)
    self.assertIsNone(sentence.__clause_lengths__)
    self.assertIsNone(sentence.__clause_array__)
    with self.assertRaises(RecursionError) as context:
      sentence._getClauseLengths(_recursion=True)
    self.assertEqual(context.exception.args, ())
    with self.assertRaises(RecursionError) as context:
      sentence._getClausesArray(_recursion=True)
    self.assertEqual(context.exception.args, ())
    clauses = sentence.clausesArray
    self.assertIs(sentence.clausesArray, clauses)
    sentence.clear()
    self.assertIsNone(sentence.__clause_lengths__)
    self.assertIsNone(sentence.__clause_array__)
    sentence.reset()
    self.assertIsNotNone(sentence.__clause_array__)
    self.assertIsNot(sentence.clausesArray, clauses)
    self.assertEqual(len(sentence), 60)
    sentence.charCount = 80
    self.assertIsNone(sentence.__clause_array__)
    self.assertEqual(len(sentence), 80)

  def test_copy_constructor(self) -> None:
    blank = Sentence.first(60)
    copy = Sentence(blank)
    self.assertEqual(copy.charCount, 60)
    self.assertTrue(copy.isFirst)
    self.assertIsNone(copy.__clause_lengths__)
    self.assertIsNone(copy.__clause_array__)
    built = Sentence(70)
    text = str(built)
    copy = Sentence(built)
    self.assertEqual(str(copy), text)
    self.assertEqual(copy.clausesLengths, built.clausesLengths)
    self.assertIsNot(copy.clausesLengths, built.clausesLengths)
    for mine, theirs in zip(copy.clausesArray, built.clausesArray):
      with self.subTest(text=str(theirs)):
        self.assertIsNot(mine, theirs)
        self.assertIsNot(mine.wordsArray, theirs.wordsArray)
        self.assertEqual(mine.wordsArray, theirs.wordsArray)

  def test_random_counts(self) -> None:
    self.randomInteger = IntSampler(15, 300, seed=self.__sampler_seed__)
    self.randomInteger.size = 12
    for count in self.randomInteger.row:
      with self.subTest(count=count):
        sentence = Sentence(count)
        self.assertEqual(len(sentence), count)
        self.assertEqual(len(str(sentence)), count)
        self.assertTrue(str(sentence).endswith('.'))
        self.assertEqual(len(Sentence.first(count)), count)

  def test_lead_in_only_on_a_first_sentence(self) -> None:
    plain = Sentence(120)
    first = Sentence.first(120)
    self.assertFalse(str(plain).startswith('Lorem ipsum'))
    self.assertTrue(str(first).startswith('Lorem ipsum'))
    self.assertEqual(str(first).count('Lorem ipsum'), 1)

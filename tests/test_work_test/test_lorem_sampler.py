"""
TestLoremSampler tests 'LoremSampler' from 'worktoy.work_test.samplers'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.waitaminute import TypeException
from worktoy.work_test.samplers import LoremSampler, LOREM_WORDS
from . import WorkTestTest


class TestLoremSampler(WorkTestTest):
  """
  'LoremSampler' draws sentences of exactly 'charCount' characters, forty
  unless set otherwise, each sampler holding its own count. The tests
  pin the default, the count by keyword under both spellings and by
  assignment, the refusals, the sentences drawn, the independence of two
  samplers, and the repeat of a seeded sampler.
  """

  def test_defaults(self) -> None:
    sampler = LoremSampler()
    self.assertEqual(sampler.charCount, 40)
    self.assertIs(sampler.valueType, str)
    self.assertEqual(repr(sampler), 'LoremSampler(charCount=40, '
                                    'colCount=1, rowCount=1, seed=None)')
    self.assertEqual(str(sampler), "<LoremSampler: 'str' (1, 1)>")
    sentence = sampler()
    self.assertEqual(len(sentence), 40)
    self.assertTrue(sentence.endswith('.'))

  def test_char_count(self) -> None:
    self.assertEqual(LoremSampler(chars=12).charCount, 12)
    self.assertEqual(LoremSampler(chars=1)(), '.')
    sampler = LoremSampler()
    sampler.charCount = 1
    self.assertEqual(sampler(), '.')
    self.assertEqual(LoremSampler(charCount=7).charCount, 7)
    self.assertEqual(LoremSampler(charCount=8.0).charCount, 8)
    self.assertEqual(len(LoremSampler(chars=12)()), 12)
    sampler = LoremSampler()
    sampler.charCount = 5
    self.assertEqual(len(sampler()), 5)
    other = LoremSampler()
    self.assertEqual(other.charCount, 40)
    self.assertEqual(sampler.charCount, 5)

  def test_refusals(self) -> None:
    sampler = LoremSampler()
    for value in (0, -1, 0.5):
      with self.subTest(value=value):
        with self.assertRaises(ValueError) as context:
          LoremSampler(charCount=value)
        self.assertEqual(str(context.exception), 'Character count must '
                                                 'be a positive integer, '
                                                 'not %r!' % (value,))
        with self.assertRaises(ValueError) as context:
          sampler.charCount = value
        self.assertIn('not %r!' % (value,), str(context.exception))
    with self.assertRaises(TypeException) as context:
      sampler.charCount = '9'
    self.assertTypeRefused(context.exception, 'charCount', '9', int)
    self.assertEqual(sampler.charCount, 40)

  def test_sentences(self) -> None:
    sampler = LoremSampler(chars=25, seed=1, size=4)
    row = sampler.row
    self.assertEqual(row, LoremSampler(chars=25, size=4, seed=1).row)
    for sentence in row:
      with self.subTest(sentence=sentence):
        self.assertEqual(len(sentence), 25)
        self.assertTrue(sentence.endswith('.'))
        for word in sentence[:-1].lower().split():
          self.assertIn(word, LOREM_WORDS)
    self.assertEqual(LoremSampler(seed=1)(),
                     'Enim eum velit amet aspernatur pariatur.')

  def test_random_sentences(self) -> None:
    self.randomLorem.size = 5
    for sentence in self.randomLorem.row:
      with self.subTest(sentence=sentence):
        self.assertEqual(len(sentence), 40)
    self.assertEqual(self.randomLorem.seed, self.__sampler_seed__)

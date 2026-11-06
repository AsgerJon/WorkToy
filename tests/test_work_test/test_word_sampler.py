"""
TestWordSampler tests 'WordSampler' from 'worktoy.work_test.samplers'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.work_test.samplers import WordSampler, LOREM_WORDS
from . import WorkTestTest


class TestWordSampler(WorkTestTest):
  """
  'WordSampler' draws single words of the vocabulary and has no setting
  of its own. The tests pin the value type, the words drawn, the
  repeat of a seeded sampler, and the sampler every test holds.
  """

  def test_words(self) -> None:
    sampler = WordSampler(seed=4, size=6)
    self.assertIs(sampler.valueType, str)
    self.assertEqual(sampler.row, WordSampler(size=6, randomSeed=4).row)
    for word in sampler.row:
      with self.subTest(word=word):
        self.assertIn(word, LOREM_WORDS)
    self.assertIn(sampler(), LOREM_WORDS)
    self.assertIn(sampler.item, LOREM_WORDS)
    self.assertEqual(WordSampler(seed=1)(), 'enim')

  def test_random_words(self) -> None:
    self.randomWord.size = 8
    row = self.randomWord.row
    self.assertEqual(len(row), 8)
    for word in row:
      with self.subTest(word=word):
        self.assertIn(word, LOREM_WORDS)
    self.assertEqual(self.randomWord.seed, self.__sampler_seed__)

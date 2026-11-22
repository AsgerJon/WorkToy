"""
PromisePublicNames promises the names 'worktoy.lorem_ipsum' exports.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

import worktoy.lorem_ipsum


class PromisePublicNames(TestCase):
  """
  The generators 'Clause', 'Sentence' and 'Paragraph', the distributions
  'StochasticVariable', 'GaussianLengths' and 'StochasticWord', their
  base 'BaseGenerator', and the word lists 'COMMON_WORDS',
  'UNCOMMON_WORDS' and 'RARE_WORDS', tuples of words, import from
  'worktoy.lorem_ipsum'. Source: '__all__' of the package.
  """

  def test_names(self) -> None:
    names = ('StochasticVariable', 'GaussianLengths', 'StochasticWord',
             'BaseGenerator', 'Clause', 'Sentence', 'Paragraph')
    for name in names:
      with self.subTest(name=name):
        self.assertTrue(hasattr(worktoy.lorem_ipsum, name))

  def test_word_lists(self) -> None:
    for name in ('COMMON_WORDS', 'UNCOMMON_WORDS', 'RARE_WORDS'):
      with self.subTest(name=name):
        words = getattr(worktoy.lorem_ipsum, name)
        self.assertIsInstance(words, tuple)
        for word in words:
          self.assertIsInstance(word, str)

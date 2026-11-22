"""
RefusedWords holds the refusals that belong with
'design.promises.lorem_ipsum.promise_words'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.lorem_ipsum import StochasticWord


class RefusedWords(TestCase):
  """
  Each of the following is refused, and the exception named is the one raised
  as of 1.2.3. A length no word has raises 'IndexError'. A list of words
  missing a length between its shortest and longest raises 'ValueError' at
  the class statement. Source: the docstrings of 'StochasticWord' and
  'Clause'.
  """

  def test_default_words(self) -> None:
    words = StochasticWord()
    for length in range(words.minVal, words.maxVal + 1):
      with self.subTest(length=length):
        self.assertEqual(len(words.realizeLength(length)), length)
        self.assertEqual(len(words[length]), length)
    with self.assertRaises(Exception) as refused:
      words.realizeLength(words.maxVal + 1)
    self.assertIsInstance(refused.exception, IndexError)

  def test_gap_refused(self) -> None:
    with self.assertRaises(Exception) as refused:
      class Gappy(StochasticWord):
        __category_weights__ = ((('fig', 'banana'), 1.0),)
    self.assertIsInstance(refused.exception, ValueError)

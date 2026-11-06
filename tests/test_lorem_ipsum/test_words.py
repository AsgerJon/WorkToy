"""
TestWords tests the word lists of 'worktoy.lorem_ipsum'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.lorem_ipsum import COMMON_WORDS, UNCOMMON_WORDS, RARE_WORDS
from worktoy.lorem_ipsum import _words
from . import LoremTest


class TestWords(LoremTest):
  """
  The three word lists feed 'StochasticWord', which groups them by
  length and must find a word of every length between the shortest and
  the longest. The tests pin the size and the shape of the lists, that
  no word repeats, and that no length in the range is missing.
  """

  def test_sizes(self) -> None:
    for words in (COMMON_WORDS, UNCOMMON_WORDS, RARE_WORDS):
      with self.subTest(first=words[0]):
        self.assertIsInstance(words, tuple)
        self.assertEqual(len(words), 40)
        self.assertEqual(len(set(words)), 40)

  def test_shape(self) -> None:
    for word in (*COMMON_WORDS, *UNCOMMON_WORDS, *RARE_WORDS):
      with self.subTest(word=word):
        self.assertTrue(word.isalpha())
        self.assertTrue(word.islower())
        self.assertTrue(word.isascii())

  def test_no_word_repeats_across_lists(self) -> None:
    every = (*COMMON_WORDS, *UNCOMMON_WORDS, *RARE_WORDS)
    self.assertEqual(len(set(every)), 120)

  def test_every_length_present(self) -> None:
    every = (*COMMON_WORDS, *UNCOMMON_WORDS, *RARE_WORDS)
    lengths = {len(word) for word in every}
    self.assertEqual(min(lengths), 4)
    self.assertEqual(max(lengths), 12)
    self.assertEqual(lengths, set(range(4, 13)))

  def test_exports(self) -> None:
    self.assertEqual(_words.__all__,
                     ('COMMON_WORDS', 'UNCOMMON_WORDS', 'RARE_WORDS'))
    self.assertIs(_words.COMMON_WORDS, COMMON_WORDS)

  def test_random_words_are_not_lorem(self) -> None:
    self.randomWord.size = 8
    every = {*COMMON_WORDS, *UNCOMMON_WORDS, *RARE_WORDS}
    for word in self.randomWord.row:
      with self.subTest(word=word):
        self.assertTrue(word.isalpha())
        self.assertIsInstance(word in every, bool)

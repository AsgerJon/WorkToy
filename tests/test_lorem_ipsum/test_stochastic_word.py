"""
TestStochasticWord tests the 'StochasticWord' class from the
'worktoy.lorem_ipsum' package.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.lorem_ipsum import StochasticWord
from . import LoremIpsumTest


class TestStochasticWord(LoremIpsumTest):
  """
  TestStochasticWord provides tests for the 'StochasticWord' class from
  the 'worktoy.lorem_ipsum' package.
  """

  def setUp(self) -> None:
    super().setUp()
    self.stochasticWord: StochasticWord = StochasticWord()
    self.stochasticWord.realize()  # Preload the data

  def test_realize(self) -> None:
    """
    Testing that 'realize' draws words as 'str' objects.
    """
    for _ in range(10):
      word = self.stochasticWord.realize()
      self.assertIsInstance(word, str)

  def test_realize_length(self) -> None:
    """
    Testing that 'realizeLength' draws a word of exactly the requested
    length for every available length.
    """
    for length, words in self.stochasticWord.byLengths.items():
      for _ in range(10):
        word = self.stochasticWord.realizeLength(length)
        self.assertIsInstance(word, str)
        self.assertEqual(len(word), length)

  def test_index_error_guard(self, ) -> None:
    """
    Testing the index error raised when asking for unavailable lengths.
    """
    with self.assertRaises(IndexError):
      _ = self.stochasticWord.realizeLength(69)

    with self.assertRaises(IndexError):
      _ = self.stochasticWord.realizeLength(420)

  def test_getitem(self, ) -> None:
    """
    Testing that indexing by a length realizes a word of that length, the
    same as 'realizeLength'.
    """
    for length in self.stochasticWord.byLengths:
      word = self.stochasticWord[length]
      self.assertIsInstance(word, str)
      self.assertEqual(len(word), length)

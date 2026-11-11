"""
PromiseWords promises 'StochasticWord' and word lists of a project's
own, from 'worktoy.lorem_ipsum'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.desc import AttriBox
from worktoy.lorem_ipsum import StochasticWord, Clause


class PromiseWords(TestCase):
  """
  A 'StochasticWord' draws words from its lists: 'realizeLength(n)', or
  'word[n]', gives a word of length 'n', and a length no word has raises
  'IndexError'; 'realize()' gives a word of any length. 'minVal' and
  'maxVal' are the shortest and longest lengths. A project brings words
  of its own with a subclass setting '__category_weights__' to pairs of
  a tuple of words and the weight of each word in it; a list missing a
  length between its shortest and longest raises 'ValueError' at the
  class statement. A clause draws from its own list when 'stochWord' is
  redeclared as a box of such a subclass. Source: the docstrings of
  'StochasticWord' and 'Clause'.
  """

  def test_default_words(self) -> None:
    words = StochasticWord()
    for length in range(words.minVal, words.maxVal + 1):
      with self.subTest(length=length):
        self.assertEqual(len(words.realizeLength(length)), length)
        self.assertEqual(len(words[length]), length)
    self.assertIsInstance(words.realize(), str)
    with self.assertRaises(IndexError):
      words.realizeLength(words.maxVal + 1)

  def test_own_words(self) -> None:
    class Fruit(StochasticWord):
      __category_weights__ = ((('fig', 'kiwi', 'apple', 'banana'), 1.0),)

    class FruitClause(Clause):
      stochWord = AttriBox[Fruit]()

    self.assertEqual((Fruit.minVal, Fruit.maxVal), (3, 6))
    self.assertEqual(Fruit().realizeLength(4), 'kiwi')
    for _ in range(20):
      text = str(FruitClause(20))
      self.assertEqual(len(text), 20)
      for word in text.split(' '):
        self.assertIn(word, ('fig', 'kiwi', 'apple', 'banana'))

  def test_gap_refused(self) -> None:
    with self.assertRaises(ValueError):
      class Gappy(StochasticWord):
        __category_weights__ = ((('fig', 'banana'), 1.0),)

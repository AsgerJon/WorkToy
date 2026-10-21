"""
TestLoremSentence subclasses 'SamplerTest' from 'tests.test_work_test' and
pins the text source of the samplers: 'LOREM_WORDS', a vocabulary with a
word of every length from one letter to the longest, 'randomWord', one
word drawn from it, and 'loremSentence', a sentence of exactly the
requested number of characters built from those words, the first
capitalised, the last followed by a period. The exact fit rests on the
vocabulary covering every length, which the tests pin as well.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.work_test.samplers import LOREM_WORDS, randomWord, loremSentence

from . import SamplerTest


class TestLoremSentence(SamplerTest):
  """
  TestLoremSentence provides tests for the lorem text source of the
  samplers.
  """

  def test_vocabulary(self) -> None:
    """The vocabulary holds lower-case alphabetic words, no word twice,
    and a word of every length from one to the longest."""
    for word in LOREM_WORDS:
      self.assertTrue(word.isalpha() and word.islower(), word)
    self.assertEqual(len(set(LOREM_WORDS)), len(LOREM_WORDS))
    lengths = {len(word) for word in LOREM_WORDS}
    self.assertEqual(lengths, set(range(1, max(lengths) + 1)))

  def test_random_word(self) -> None:
    """'randomWord' answers a word of the vocabulary."""
    for _ in range(32):
      self.assertIn(randomWord(), LOREM_WORDS)

  def test_exact_length(self) -> None:
    """A sentence of 'charCount' characters has exactly that many, for
    every count from one up and for repeated draws."""
    for charCount in range(1, 121):
      for _ in range(3):
        self.assertEqual(len(loremSentence(charCount)), charCount)

  def test_shape(self) -> None:
    """A sentence starts with a capital, ends with a period, and holds
    single spaces between words only."""
    for charCount in (2, 11, 40, 97):
      sentence = loremSentence(charCount)
      self.assertTrue(sentence[0].isupper(), sentence)
      self.assertTrue(sentence.endswith('.'), sentence)
      self.assertNotIn('  ', sentence)
      self.assertFalse(sentence[:-1].endswith(' '), sentence)
    self.assertEqual(loremSentence(1), '.')

  def test_words_from_vocabulary(self) -> None:
    """Every word of a sentence is a word of the vocabulary, the first
    read back in lower case."""
    for charCount in (2, 7, 40, 97):
      words = loremSentence(charCount)[:-1].split(' ')
      words[0] = '%s%s' % (words[0][:1].lower(), words[0][1:])
      for word in words:
        self.assertIn(word, LOREM_WORDS)

  def test_refuses_non_positive(self) -> None:
    """A count below one is refused with 'ValueError'."""
    for charCount in (0, -1, -40):
      with self.assertRaises(ValueError):
        loremSentence(charCount)

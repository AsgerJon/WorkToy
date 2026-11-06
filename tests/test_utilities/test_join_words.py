"""
TestJoinWords tests 'joinWords' from 'worktoy.utilities'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.utilities import joinWords
from worktoy.work_test.samplers import WordSampler
from . import UtilitiesTest


class TestJoinWords(UtilitiesTest):
  """
  'joinWords' turns words into the phrase a message would use, 'a, b
  and c', with the connector before the last word replaceable and any
  lists or tuples among the arguments flattened first. The tests pin
  the four lengths the phrase can have, the connector, the flattening
  and that words which are no strings are rendered with 'str'.
  """

  def test_no_words(self) -> None:
    self.assertEqual(joinWords(), '')
    self.assertEqual(joinWords([]), '')

  def test_one_word(self) -> None:
    self.assertEqual(joinWords('apples'), 'apples')

  def test_two_words(self) -> None:
    self.assertEqual(joinWords('apples', 'pears'), 'apples and pears')

  def test_three_words(self) -> None:
    self.assertEqual(joinWords('red', 'green', 'blue'),
                     'red, green and blue')

  def test_connector(self) -> None:
    self.assertEqual(joinWords('tea', 'coffee', sep='or'), 'tea or coffee')
    self.assertEqual(joinWords('a', 'b', 'c', sep='or'), 'a, b or c')

  def test_nested_arguments_flattened(self) -> None:
    self.assertEqual(joinWords('Tom', ['Dick', 'Harry']),
                     'Tom, Dick and Harry')
    self.assertEqual(joinWords([['a', ['b']], ('c',)]), 'a, b and c')

  def test_non_string_words(self) -> None:
    self.assertEqual(joinWords(7), '7')
    self.assertEqual(joinWords(1, 2), '1 and 2')
    self.assertEqual(joinWords(1, 2, 3), '1, 2 and 3')

  def test_bytes_kept_whole(self) -> None:
    self.assertEqual(joinWords(b'ab', 'c'), "b'ab' and c")

  def test_random_word_counts(self) -> None:
    self.randomWord = WordSampler(seed=5)
    for n in range(3, 9):
      self.randomWord.size = n
      words = self.randomWord.row
      phrase = joinWords(*words)
      with self.subTest(n=n):
        self.assertEqual(phrase.count(', '), n - 2)
        self.assertTrue(phrase.endswith(' and %s' % words[-1]))
        self.assertTrue(phrase.startswith('%s, ' % words[0]))

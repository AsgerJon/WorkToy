"""
PromiseJoinWords promises 'joinWords' from 'worktoy.utilities'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.utilities import joinWords


class PromiseJoinWords(TestCase):
  """
  'joinWords' joins words into a phrase as a person writes a list:
  commas between them and 'and' before the last, or the connector given
  as 'sep'. Lists and tuples among the words are flattened, and a
  string is one word. No words give an empty string. Source: the
  'joinWords' docstring and its examples.
  """

  def test_phrases(self) -> None:
    self.assertEqual(joinWords('apples', 'pears'), 'apples and pears')
    self.assertEqual(joinWords('red', 'green', 'blue'),
                     'red, green and blue')

  def test_connector(self) -> None:
    self.assertEqual(joinWords('tea', 'coffee', sep='or'), 'tea or coffee')

  def test_flattens(self) -> None:
    self.assertEqual(joinWords('Tom', ['Dick', 'Harry']),
                     'Tom, Dick and Harry')
    self.assertEqual(joinWords(['Tom', ('Dick', ['Harry'])]),
                     'Tom, Dick and Harry')

  def test_one_and_none(self) -> None:
    self.assertEqual(joinWords('alone'), 'alone')
    self.assertEqual(joinWords(), '')

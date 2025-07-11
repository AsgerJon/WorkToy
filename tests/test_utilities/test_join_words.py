"""TestJoinWords tests the joinWords function"""
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from . import UtilitiesTest
from worktoy.utilities import joinWords


class TestJoinWords(UtilitiesTest):
  """TestJoinWords tests the joinWords function"""

  def test_empty(self) -> None:
    """Tests if joinWords correctly returns an empty string when
    receiving no arguments"""
    self.assertIsInstance(joinWords(), str)
    self.assertFalse(joinWords())

  def test_single(self) -> None:
    """Tests if joinWords correctly returns the single string as is"""
    self.assertEqual(joinWords('hello'), 'hello')

  def test_double(self) -> None:
    """Tests if joinWords correctly joins two strings"""
    self.assertEqual(joinWords('hello', 'world'), 'hello and world')

  def test_many(self, ) -> None:
    """Tests if joinWords correctly joins many strings"""
    sample = 'Tom', 'Dick', 'Harry'
    expected = 'Tom, Dick and Harry'
    self.assertEqual(joinWords(*sample), expected)

  def test_list(self) -> None:
    """Tests a list"""
    sampleTuple = 'Tom', 'Dick', 'Harry'
    sampleList = [*sampleTuple, ]
    tupleRes = joinWords(sampleTuple, )
    listRes = joinWords(sampleList, )
    self.assertEqual(tupleRes, listRes)

  def test_not_str(self, ) -> None:
    """Tests passing an object not of str and not of tuple or list"""
    intWord = 80085
    floatWord = .1337
    complexWord = 69 + 420j
    for word in [intWord, floatWord, complexWord]:
      self.assertEqual(str(word), joinWords(word))

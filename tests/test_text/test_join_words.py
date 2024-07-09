"""TestJoinWords tests the joinWords function"""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.text import joinWords
from worktoy.worktest import WorkTest


class TestJoinWords(WorkTest):
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
    sample = 'hello', 'world', 'universe'
    expected = 'hello, world and universe'
    self.assertEqual(joinWords(*sample), expected)

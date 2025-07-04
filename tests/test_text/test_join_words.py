"""TestJoinWords tests the joinWords function"""
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.utilities import joinWords
from worktoy.waitaminute import TypeException


class TestJoinWords(TestCase):
  """TestJoinWords tests the joinWords function"""

  @classmethod
  def tearDownClass(cls) -> None:
    import sys
    import gc
    sys.modules.pop(__name__, None)
    gc.collect()

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

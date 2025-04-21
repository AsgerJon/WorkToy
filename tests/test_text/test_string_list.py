"""TestStringList tests the stringList function."""
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.text import stringList


class TestStringList(TestCase):
  """TestStringList tests the StringList class."""

  def test_stringList(self) -> None:
    """Test the stringList function."""
    items = 'a, b, c, d'
    expected = ['a', 'b', 'c', 'd']
    actual = stringList(items)
    self.assertEqual(expected, actual)

    items = 'a, b, c, d'
    expected = ['a', 'b', 'c', 'd']
    actual = stringList(items, separator=',')
    self.assertEqual(expected, actual)

    items = 'a, b, c, d'
    expected = ['a', 'b', 'c', 'd']
    actual = stringList(items, separator='LOL')
    self.assertNotEqual(expected, actual)

    items = '/usr/bin:/usr/local/bin:/usr/sbin'
    expected = ['/usr/bin', '/usr/local/bin', '/usr/sbin']
    actual = stringList(items, separator=':')
    self.assertEqual(expected, actual)

  def test_stringList_empty(self) -> None:
    """Test the stringList function with empty string."""
    items = ''
    expected = []
    actual = stringList(items)
    self.assertEqual(expected, actual)

  def test_custom_separator(self) -> None:
    """Test the stringList function with custom separator."""
    sample = """1, 2, fizz, 4, buzz, 6, 7, 8, 9, 10"""
    sep = 'fizz'
    expected = ['1, 2,', ', 4, buzz, 6, 7, 8, 9, 10']
    actual = stringList(sample, separator=sep)
    self.assertEqual(expected, actual)
    sep = 'buzz'
    expected = ['1, 2, fizz, 4,', ', 6, 7, 8, 9, 10']
    actual = stringList(sample, separator=sep)
    self.assertEqual(expected, actual)

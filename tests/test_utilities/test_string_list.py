"""TestStringList tests the stringList function."""
#  AGPL-3.0 license
#  Copyright (c) 2024-2026 Asger Jon Vistisen
from __future__ import annotations

from . import UtilitiesTest
from worktoy.utilities import stringList
from worktoy.waitaminute import TypeException


class TestStringList(UtilitiesTest):
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

  def test_multiple_separators(self) -> None:
    """Test the stringList function with multiple separators."""
    sample = 'a, b; c, d'
    expected = ['a', 'b', 'c', 'd']
    actual = stringList(sample, separator=[', ', '; '])
    self.assertEqual(len(expected), len(actual))
    for e, a in zip(expected, actual):
      self.assertEqual(e, a)

  def test_invalid_separator(self) -> None:
    with self.assertRaises(TypeException) as context:
      stringList('a, b, c', separator=80085)
    e = context.exception
    self.assertEqual(e.varName, 'separator')
    self.assertEqual(e.actualObject, 80085)
    self.assertEqual(e.actualType, int)
    for type_ in [str, list, tuple]:
      self.assertIn(type_, e.expectedTypes)

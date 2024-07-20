"""TestStringList tests the stringList function."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
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

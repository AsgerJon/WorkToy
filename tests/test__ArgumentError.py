"""Testing Argument error"""
#  MIT License
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import unittest

from worktoy.sharperexceptions import ArgumentError


class MyClass:
  def __init__(self, value):
    if not value:
      raise ArgumentError(self, 'value')
    self.value = value


class ArgumentErrorTestCase(unittest.TestCase):
  """Test case for the ArgumentError exception."""

  def test_argument_error(self):
    """Test that an ArgumentError is raised correctly."""
    with self.assertRaises(ArgumentError):
      MyClass('')


if __name__ == '__main__':
  unittest.main()

"""TestWordWrap tests the wordWrap function."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.text import wordWrap, monoSpace


class TestWordWrap(TestCase):
  """TestWordWrap tests the wordWrap function."""

  def setUp(self) -> None:
    """Set up the test case."""
    self.paragraph = monoSpace("""Lorem ipsum dolor sit amet, adipiscing 
    elit. Sed do eiusmod tempor incididunt ut labore et dolore magna 
    aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco. <br>
    laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor 
    in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla 
    pariatur. Excepteur sint occaecat cupidatat non proident, sunt in 
    culpa qui officia deserunt mollit anim id est laborum.""")
    self.sentence = """Never gonna give you up, never gonna let you down, 
    never gonna run"""

  def test_wordWrap(self) -> None:
    """Test the wordWrap function."""
    for width in range(25, 100):
      actual = wordWrap(width, self.paragraph)
      lines = actual.split('\n')
      for line in lines:
        self.assertLessEqual(len(line), width)

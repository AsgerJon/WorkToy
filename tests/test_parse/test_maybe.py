"""TestMaybe tests the maybe function"""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from random import shuffle
from unittest import TestCase

from worktoy.parse import maybe


class TestMaybe(TestCase):
  """TestMaybe tests the maybe function"""

  def test_maybe(self) -> None:
    """Test the maybe function."""
    someFalse = [0, '', dict(), set(), list(), 0j, .0, ]
    for false in someFalse:
      sample = [*([None, ] * 69), false]
      shuffle(sample)
      parsed = maybe(*sample)
      self.assertIs(parsed, false)
      self.assertFalse(parsed)
      self.assertIsNotNone(parsed)

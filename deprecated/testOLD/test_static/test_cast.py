"""TestCast tests the casting system. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase
from worktoy.static.casting import FloatCast, ComplexCast
from worktoy.static.casting import IntCast, AutoCast, Cast


class TestCast(TestCase):
  """Test the casting system."""

  def test_cast(self) -> None:
    """Test the casting system."""
    # Test the basic functionality of the cast system
    self.assertIsInstance(Cast(int), IntCast)
    self.assertIsInstance(Cast(float), FloatCast)
    self.assertIsInstance(Cast(complex), ComplexCast)
    self.assertIsInstance(Cast(str), AutoCast)

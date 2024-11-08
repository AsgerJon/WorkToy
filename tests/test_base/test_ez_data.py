"""TestEZData tests the EZData inline data class"""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.ezdata import EZData


class TestEZData(TestCase):
  """TestEZData tests the EZData inline data class"""

  def setUp(self, ) -> None:
    """The 'setUp' method prepares the test fixture. """
    self.pointClass = EZData(__name__='Point', x=(69, int), y=(420, int))

  def test_base(self, ) -> None:
    """Testing base functionality. """
    self.assertTrue(self.pointClass)

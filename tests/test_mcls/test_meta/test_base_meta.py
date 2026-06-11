"""
TestBaseMeta subclasses 'MCLSTest' and provides tests for the 'BaseMeta'
metaclass from the 'worktoy.mcls' package.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from .. import MCLSTest


class TestBaseMeta(MCLSTest):
  """
  TestBaseMeta subclasses 'MCLSTest' and provides tests for the 'BaseMeta'
  metaclass from the 'worktoy.mcls' package.
  """

  def test_dev_null(self) -> None:
    """
    This method tests that the test framework is working.
    """
    self.assertTrue(True)

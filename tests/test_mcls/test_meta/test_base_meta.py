"""
TestBaseMeta subclasses 'MCLSTest' and provides tests for the 'BaseMeta'
metaclass from the 'worktoy.mcls' package.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from .. import MCLSTest

if TYPE_CHECKING:  # pragma: no cover
  pass


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

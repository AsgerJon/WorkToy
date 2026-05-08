"""Tests for 'EZDeleteException' message rendering."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.waitaminute.ez import EZDeleteException
from . import WaitAMinuteTest


class _Sample:
  pass


class TestEZDeleteException(WaitAMinuteTest):

  def test_str_contains_class_and_field(self) -> None:
    exc = EZDeleteException(_Sample, 'value')
    message = str(exc)
    self.assertIn('_Sample', message)
    self.assertIn('value', message)

"""Tests for 'FrozenEZException' message rendering."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.waitaminute.ez import FrozenEZException
from . import WaitAMinuteTest


class TestFrozenEZException(WaitAMinuteTest):

  def test_str_contains_all_fields(self) -> None:
    exc = FrozenEZException('value', 'Sample', 1, 2)
    message = str(exc)
    self.assertIn('value', message)
    self.assertIn('Sample', message)
    self.assertIn('1', message)
    self.assertIn('2', message)

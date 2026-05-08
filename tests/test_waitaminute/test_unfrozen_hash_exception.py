"""Tests for 'UnfrozenHashException' message rendering."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.waitaminute.ez import UnfrozenHashException
from . import WaitAMinuteTest


class TestUnfrozenHashException(WaitAMinuteTest):

  def test_str_contains_class_name(self) -> None:
    exc = UnfrozenHashException('Sample')
    message = str(exc)
    self.assertIn('Sample', message)
    self.assertIn('frozen', message)

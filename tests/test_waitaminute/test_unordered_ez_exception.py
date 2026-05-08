"""Tests for 'UnorderedEZException' message rendering."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.waitaminute.ez import UnorderedEZException
from . import WaitAMinuteTest


class TestUnorderedEZException(WaitAMinuteTest):

  def test_str_without_field_info(self) -> None:
    exc = UnorderedEZException('Sample')
    message = str(exc)
    self.assertIn('Sample', message)
    self.assertIn('order', message)

  def test_str_with_field_info(self) -> None:
    exc = UnorderedEZException('Sample', 'value', complex)
    message = str(exc)
    self.assertIn('Sample', message)
    self.assertIn('value', message)
    self.assertIn('complex', message)

"""Tests for 'TypeException' message rendering."""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.waitaminute import TypeException
from . import WaitAMinuteTest


class TestTypeException(WaitAMinuteTest):

  def test_str_short_object(self) -> None:
    exc = TypeException('var', 7, str)
    message = str(exc)
    self.assertIn('var', message)
    self.assertIn('7', message)
    self.assertIn('str', message)

  def test_str_truncates_long_object_repr(self) -> None:
    longValue = 'x' * 200
    exc = TypeException('var', longValue, int)
    message = str(exc)
    self.assertIn('...', message)

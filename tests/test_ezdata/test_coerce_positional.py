"""Tests for ``coercePositional``."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.ezdata import coercePositional
from worktoy.waitaminute import TypeException
from . import EZTest


class TestCoercePositional(EZTest):

  def test_isinstance_match(self) -> None:
    self.assertEqual(coercePositional(5, int), 5)

  def test_str_target_non_str_raises(self) -> None:
    with self.assertRaises(TypeException):
      coercePositional(5, str)

  def test_coerce_success(self) -> None:
    self.assertEqual(coercePositional('5', int), 5)

  def test_coerce_failure_wraps(self) -> None:
    with self.assertRaises(TypeException):
      coercePositional('not an int', int)

"""Tests for ``coerceAttr``."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.ezdata import coerceAttr
from . import EZTest


class TestCoerceAttr(EZTest):

  def test_isinstance_match(self) -> None:
    self.assertEqual(coerceAttr(5, int), 5)

  def test_propagates_like_kwarg(self) -> None:
    with self.assertRaises(ValueError):
      coerceAttr('not an int', int)

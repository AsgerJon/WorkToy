"""Tests for ``makeLen``."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from . import EZTest
from ._factory_helpers import build, slot


class TestMakeLen(EZTest):

  def test_len(self) -> None:
    cls = build([slot('x', int, 0), slot('y', int, 0)])
    self.assertEqual(len(cls()), 2)

  def test_len_empty(self) -> None:
    cls = build([])
    self.assertEqual(len(cls()), 0)

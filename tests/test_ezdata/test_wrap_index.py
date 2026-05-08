"""Tests for ``wrapIndex``."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.ezdata import wrapIndex
from . import EZTest


class TestWrapIndex(EZTest):

  def test_zero_length_raises(self) -> None:
    with self.assertRaises(IndexError):
      wrapIndex(0, 0)

  def test_in_range_positive(self) -> None:
    self.assertEqual(wrapIndex(0, 3), 0)
    self.assertEqual(wrapIndex(2, 3), 2)

  def test_negative_small_wraps(self) -> None:
    self.assertEqual(wrapIndex(-1, 3), 2)

  def test_negative_large_wraps(self) -> None:
    self.assertEqual(wrapIndex(-1261, 3), 2)

  def test_positive_overflow_raises(self) -> None:
    with self.assertRaises(IndexError):
      wrapIndex(3, 3)

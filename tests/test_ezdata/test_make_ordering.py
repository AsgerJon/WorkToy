"""Tests for ``makeOrderingOp``."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.waitaminute.ez import UnorderedEZException
from . import EZTest
from ._factory_helpers import build, slot


class TestMakeOrdering(EZTest):

  def test_unordered_raises(self) -> None:
    cls = build([slot('a', int, 0)], ordered=False)
    with self.assertRaises(UnorderedEZException):
      _ = cls(1) < cls(2)
    with self.assertRaises(UnorderedEZException):
      _ = cls(1) <= cls(2)
    with self.assertRaises(UnorderedEZException):
      _ = cls(1) > cls(2)
    with self.assertRaises(UnorderedEZException):
      _ = cls(1) >= cls(2)

  def test_ordered_diff_type_raises(self) -> None:
    cls = build([slot('a', int, 0)], ordered=True)
    with self.assertRaises(UnorderedEZException):
      _ = cls(1) < object()

  def test_ordered_lt_first_diff_decides(self) -> None:
    cls = build([slot('a', int, 0), slot('b', int, 0)], ordered=True)
    self.assertTrue(cls(1, 5) < cls(2, 0))
    self.assertFalse(cls(2, 0) < cls(1, 5))

  def test_ordered_lt_lex_within_field(self) -> None:
    cls = build([slot('a', int, 0), slot('b', int, 0)], ordered=True)
    self.assertTrue(cls(1, 5) < cls(1, 6))
    self.assertFalse(cls(1, 6) < cls(1, 5))

  def test_ordered_gt(self) -> None:
    cls = build([slot('a', int, 0)], ordered=True)
    self.assertTrue(cls(2) > cls(1))
    self.assertFalse(cls(1) > cls(2))

  def test_ordered_strict_equal(self) -> None:
    cls = build([slot('a', int, 0)], ordered=True)
    self.assertFalse(cls(1) < cls(1))
    self.assertFalse(cls(1) > cls(1))

  def test_ordered_non_strict_equal(self) -> None:
    cls = build([slot('a', int, 0)], ordered=True)
    self.assertTrue(cls(1) <= cls(1))
    self.assertTrue(cls(1) >= cls(1))

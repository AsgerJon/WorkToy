"""Tests for ``worktoy.ezdata._trust``."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.ezdata import trust
from . import EZTest


class TestTrust(EZTest):

  def test_sets_marker_attribute(self) -> None:
    def fn() -> None:
      pass

    decorated = trust(fn)
    self.assertTrue(getattr(decorated, '__is_root__', False))
    self.assertIsNone(decorated())

  def test_returns_same_callable(self) -> None:
    def fn() -> None:
      pass

    decorated = trust(fn)
    self.assertIs(decorated, fn)
    self.assertIsNone(decorated())

  def test_works_on_lambda(self) -> None:
    fn = trust(lambda x: x)
    self.assertTrue(getattr(fn, '__is_root__', False))
    self.assertEqual(fn(42), 42)

  def test_does_not_change_call_behavior(self) -> None:
    @trust
    def add(a: int, b: int) -> int:
      return a + b

    self.assertEqual(add(2, 3), 5)

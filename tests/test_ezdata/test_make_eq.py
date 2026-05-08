"""Tests for ``makeEq``."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from . import EZTest
from ._factory_helpers import build, slot


class TestMakeEq(EZTest):

  def test_same_type_same_values(self) -> None:
    cls = build([slot('x', int, 0)])
    self.assertEqual(cls(1), cls(1))

  def test_same_type_different_values(self) -> None:
    cls = build([slot('x', int, 0)])
    self.assertNotEqual(cls(1), cls(2))

  def test_different_types_returns_notimplemented(self) -> None:
    cls = build([slot('x', int, 0)])
    other = build([slot('x', int, 0)])
    self.assertNotEqual(cls(1), other(1))

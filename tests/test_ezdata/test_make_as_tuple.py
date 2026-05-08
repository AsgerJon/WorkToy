"""Tests for ``makeAsTuple``."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from . import EZTest
from ._factory_helpers import build, slot


class TestMakeAsTuple(EZTest):

  def test_as_tuple(self) -> None:
    cls = build([slot('a', int, 0), slot('b', int, 0)])
    self.assertEqual(cls(1, 2).asTuple(), (1, 2))

  def test_as_tuple_empty(self) -> None:
    cls = build([])
    self.assertEqual(cls().asTuple(), ())

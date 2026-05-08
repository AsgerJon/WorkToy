"""Tests for ``makeIter``."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from . import EZTest
from ._factory_helpers import build, slot


class TestMakeIter(EZTest):

  def test_iter_yields_values(self) -> None:
    cls = build([slot('x', int, 0), slot('y', int, 0)])
    obj = cls(1, 2)
    self.assertEqual(list(obj), [1, 2])

  def test_iter_empty_class(self) -> None:
    cls = build([])
    self.assertEqual(list(cls()), [])

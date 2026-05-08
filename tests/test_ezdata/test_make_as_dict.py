"""Tests for ``makeAsDict``."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from . import EZTest
from ._factory_helpers import build, slot


class TestMakeAsDict(EZTest):

  def test_as_dict(self) -> None:
    cls = build([slot('a', int, 0), slot('b', int, 0)])
    self.assertEqual(cls(1, 2).asDict(), {'a': 1, 'b': 2})

  def test_as_dict_empty(self) -> None:
    cls = build([])
    self.assertEqual(cls().asDict(), {})

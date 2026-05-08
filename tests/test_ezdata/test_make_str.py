"""Tests for ``makeStr``."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from . import EZTest
from ._factory_helpers import build, slot


class TestMakeStr(EZTest):

  def test_str_positional(self) -> None:
    cls = build([slot('x', int, 0)])
    obj = cls(7)
    self.assertEqual(str(obj), 'Synthetic(7)')

  def test_str_uses_str_format(self) -> None:
    cls = build([slot('x', str, '')])
    obj = cls('hi')
    self.assertEqual(str(obj), 'Synthetic(hi)')

  def test_str_empty(self) -> None:
    cls = build([])
    obj = cls()
    self.assertEqual(str(obj), 'Synthetic()')

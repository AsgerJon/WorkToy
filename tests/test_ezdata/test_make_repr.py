"""Tests for ``makeRepr``."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from . import EZTest
from ._factory_helpers import build, slot


class TestMakeRepr(EZTest):

  def test_repr_positional(self) -> None:
    cls = build([slot('x', int, 0), slot('y', int, 0)])
    obj = cls(1, 2)
    self.assertEqual(repr(obj), 'Synthetic(1, 2)')

  def test_repr_empty(self) -> None:
    cls = build([])
    obj = cls()
    self.assertEqual(repr(obj), 'Synthetic()')

  def test_repr_strings_quoted(self) -> None:
    cls = build([slot('s', str, '')])
    self.assertEqual(repr(cls('hi')), "Synthetic('hi')")

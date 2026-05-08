"""Tests for ``makeHash``."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.waitaminute.ez import UnfrozenHashException
from . import EZTest
from ._factory_helpers import build, slot


class TestMakeHash(EZTest):

  def test_frozen_hashes_value_tuple(self) -> None:
    cls = build([slot('x', int, 0), slot('y', int, 0)], frozen=True)
    self.assertEqual(hash(cls(1, 2)), hash((1, 2)))

  def test_unfrozen_raises(self) -> None:
    cls = build([slot('x', int, 0)], frozen=False)
    with self.assertRaises(UnfrozenHashException):
      hash(cls(1))

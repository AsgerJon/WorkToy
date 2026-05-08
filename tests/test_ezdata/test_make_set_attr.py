"""Tests for ``makeSetAttr``."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.waitaminute.ez import FrozenEZException
from . import EZTest
from ._factory_helpers import build, slot


class TestMakeSetAttr(EZTest):

  def test_unknown_key_raises(self) -> None:
    cls = build([slot('x', int, 0)])
    obj = cls()
    with self.assertRaises(AttributeError):
      obj.unknown = 1

  def test_known_key_coerces(self) -> None:
    cls = build([slot('x', int, 0)])
    obj = cls()
    obj.x = '42'
    self.assertEqual(obj.x, 42)

  def test_frozen_post_init_raises(self) -> None:
    cls = build([slot('x', int, 0)], frozen=True)
    obj = cls(1)
    with self.assertRaises(FrozenEZException):
      obj.x = 2

  def test_frozen_init_marker_passes_through(self) -> None:
    cls = build([slot('x', int, 0)], frozen=True)
    obj = cls(1)
    object.__setattr__(obj, '__ez_initialized__', False)
    obj.x = 2
    self.assertEqual(obj.x, 2)

  def test_frozen_unknown_key_raises(self) -> None:
    cls = build([slot('x', int, 0)], frozen=True)
    obj = cls(1)
    with self.assertRaises(AttributeError):
      obj.unknown = 1

  def test_frozen_setting_init_marker_via_setattr(self) -> None:
    cls = build([slot('x', int, 0)], frozen=True)
    obj = cls(1)
    obj.__ez_initialized__ = False
    obj.x = 2
    self.assertEqual(obj.x, 2)

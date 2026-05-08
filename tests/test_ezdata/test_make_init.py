"""Tests for ``makeInit``."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.waitaminute import TypeException
from . import EZTest
from ._factory_helpers import build, slot


class TestMakeInit(EZTest):

  def test_defaults(self) -> None:
    cls = build([slot('x', int, 7), slot('y', int, 9)])
    obj = cls()
    self.assertEqual(obj.x, 7)
    self.assertEqual(obj.y, 9)

  def test_positional_overrides_default(self) -> None:
    cls = build([slot('x', int, 0), slot('y', int, 0)])
    obj = cls(1, 2)
    self.assertEqual(obj.x, 1)
    self.assertEqual(obj.y, 2)

  def test_none_positional_skipped(self) -> None:
    cls = build([slot('x', int, 7)])
    obj = cls(None)
    self.assertEqual(obj.x, 7)

  def test_extra_positional_silently_dropped(self) -> None:
    cls = build([slot('x', int, 0)])
    obj = cls(1, 2, 3)
    self.assertEqual(obj.x, 1)

  def test_kwarg_overrides_positional(self) -> None:
    cls = build([slot('x', int, 0), slot('y', int, 0)])
    obj = cls(1, 2, x=99)
    self.assertEqual(obj.x, 99)
    self.assertEqual(obj.y, 2)

  def test_unknown_kwarg_silently_dropped(self) -> None:
    cls = build([slot('x', int, 0)])
    obj = cls(breh=42)
    self.assertEqual(obj.x, 0)

  def test_positional_coerce(self) -> None:
    cls = build([slot('x', int, 0)])
    obj = cls('5')
    self.assertEqual(obj.x, 5)

  def test_positional_coerce_failure_wraps(self) -> None:
    cls = build([slot('x', int, 0)])
    with self.assertRaises(TypeException):
      cls('not an int')

  def test_kwarg_coerce_failure_propagates(self) -> None:
    cls = build([slot('x', int, 0)])
    with self.assertRaises(ValueError):
      cls(x='not an int')

  def test_str_slot_rejects_non_str_positional(self) -> None:
    cls = build([slot('x', str, 'hi')])
    with self.assertRaises(TypeException):
      cls(42)

  def test_str_slot_rejects_non_str_kwarg(self) -> None:
    cls = build([slot('x', str, 'hi')])
    with self.assertRaises(TypeException):
      cls(x=42)

  def test_frozen_sets_init_marker(self) -> None:
    cls = build([slot('x', int, 0)], frozen=True)
    obj = cls(1)
    self.assertTrue(getattr(obj, '__ez_initialized__'))

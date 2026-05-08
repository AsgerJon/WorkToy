"""Tests for ``worktoy.ezdata._ez_slot.EZSlot``."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.ezdata import EZSlot
from . import EZTest


class TestEZSlot(EZTest):

  def test_init_single_arg(self) -> None:
    s = EZSlot('foo')
    self.assertEqual(s.name, 'foo')
    self.assertIsNone(s.typeValue)
    self.assertIsNone(s.defaultValue)
    self.assertEqual(s.ownerName, '')

  def test_setattr_legacy_dunder_names(self) -> None:
    s = EZSlot('foo')
    object.__setattr__(s, '__type_value__', int)
    object.__setattr__(s, '__default_value__', 42)
    object.__setattr__(s, '__owner_name__', 'Owner')
    self.assertEqual(s.typeValue, int)
    self.assertEqual(s.defaultValue, 42)
    self.assertEqual(s.ownerName, 'Owner')

  def test_eq_same_name(self) -> None:
    a = EZSlot('foo')
    b = EZSlot('foo')
    self.assertEqual(a, b)

  def test_eq_different_name(self) -> None:
    a = EZSlot('foo')
    b = EZSlot('bar')
    self.assertNotEqual(a, b)

  def test_eq_non_ez_slot(self) -> None:
    a = EZSlot('foo')
    #  __eq__ returns NotImplemented for non-EZSlot, which Python
    #  translates to "not equal" via fallback identity check.
    self.assertNotEqual(a, 'foo')
    self.assertNotEqual(a, object)

  def test_hash_stable(self) -> None:
    a = EZSlot('foo')
    b = EZSlot('foo')
    self.assertEqual(hash(a), hash(b))

  def test_hash_set_membership(self) -> None:
    a = EZSlot('foo')
    b = EZSlot('foo')
    s = {a}
    self.assertIn(b, s)

  def test_str_default_state(self) -> None:
    s = EZSlot('foo')
    text = str(s)
    self.assertIn('foo', text)
    self.assertIn('?', text)
    self.assertIn('[NONE]', text)

  def test_str_with_type_and_value(self) -> None:
    s = EZSlot('foo')
    object.__setattr__(s, '__type_value__', int)
    object.__setattr__(s, '__default_value__', 7)
    object.__setattr__(s, '__owner_name__', 'Bar')
    text = str(s)
    self.assertIn('int', text)
    self.assertIn('7', text)
    self.assertIn('Bar', text)
    self.assertIn('foo', text)

  def test_str_with_type_only(self) -> None:
    s = EZSlot('foo')
    object.__setattr__(s, '__type_value__', int)
    text = str(s)
    self.assertIn('int', text)
    self.assertIn('[NONE]', text)

  def test_str_with_value_only(self) -> None:
    s = EZSlot('foo')
    object.__setattr__(s, '__default_value__', 7)
    text = str(s)
    self.assertIn('?', text)
    self.assertIn('7', text)

  def test_repr_equals_str(self) -> None:
    s = EZSlot('foo')
    object.__setattr__(s, '__type_value__', int)
    object.__setattr__(s, '__default_value__', 7)
    self.assertEqual(repr(s), str(s))

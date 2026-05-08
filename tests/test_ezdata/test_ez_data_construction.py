"""Integration tests covering ``EZData`` construction."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.waitaminute import TypeException
from . import EZTest
from ._fixtures import Annotated, Mixed3, Point, Sub3D


class TestEZDataConstruction(EZTest):

  def test_defaults(self) -> None:
    p = Point()
    self.assertEqual(p.x, 0)
    self.assertEqual(p.y, 0)

  def test_positional(self) -> None:
    p = Point(3, 4)
    self.assertEqual(p.x, 3)
    self.assertEqual(p.y, 4)

  def test_kwargs(self) -> None:
    p = Point(x=3, y=4)
    self.assertEqual(p.x, 3)
    self.assertEqual(p.y, 4)

  def test_kwargs_override_positional(self) -> None:
    p = Point(1, 2, x=3)
    self.assertEqual(p.x, 3)
    self.assertEqual(p.y, 2)

  def test_none_positional_keeps_default(self) -> None:
    p = Point(None, 4)
    self.assertEqual(p.x, 0)
    self.assertEqual(p.y, 4)

  def test_extra_positional_ignored(self) -> None:
    p = Point(1, 2, 3, 4)
    self.assertEqual(p.x, 1)
    self.assertEqual(p.y, 2)

  def test_unknown_kwarg_ignored(self) -> None:
    p = Point(breh=99)
    self.assertEqual(p.x, 0)
    self.assertEqual(p.y, 0)

  def test_annotated_class(self) -> None:
    a = Annotated('Alice', 42)
    self.assertEqual(a.name, 'Alice')
    self.assertEqual(a.age, 42)

  def test_inheritance(self) -> None:
    s = Sub3D(1, 2, 3)
    self.assertEqual(s.x, 1)
    self.assertEqual(s.y, 2)
    self.assertEqual(s.z, 3)

  def test_inheritance_defaults(self) -> None:
    s = Sub3D()
    self.assertEqual(s.x, 0)
    self.assertEqual(s.y, 0)
    self.assertEqual(s.z, 0)

  def test_positional_coerce(self) -> None:
    p = Point('5', 6)
    self.assertEqual(p.x, 5)

  def test_kwarg_coerce(self) -> None:
    a = Annotated('Alice', age='42')
    self.assertEqual(a.age, 42)

  def test_positional_type_error_wraps(self) -> None:
    with self.assertRaises(TypeException):
      Point('not an int', 0)

  def test_kwarg_type_error_propagates(self) -> None:
    with self.assertRaises(ValueError):
      Point(x='not an int')

  def test_str_slot_rejects_non_str_positional(self) -> None:
    with self.assertRaises(TypeException):
      Mixed3(0, 0, 42)

  def test_str_slot_rejects_non_str_kwarg(self) -> None:
    with self.assertRaises(TypeException):
      Mixed3(0, 0, note=42)

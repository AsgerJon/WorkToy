"""Integration tests for the auto-generated equality, repr, iter,
len, asTuple, and asDict dunders on ``EZData`` subclasses."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from . import EZTest
from ._fixtures import Annotated, Point, Sub3D

 
class TestEZDataDunders(EZTest):

  def test_eq_same_values(self) -> None:
    self.assertEqual(Point(1, 2), Point(1, 2))

  def test_eq_different_values(self) -> None:
    self.assertNotEqual(Point(1, 2), Point(3, 4))

  def test_eq_different_types(self) -> None:
    self.assertNotEqual(Point(1, 2), Annotated('a', 1))

  def test_repr_positional(self) -> None:
    self.assertEqual(repr(Point(7, 9)), 'Point(7, 9)')

  def test_repr_strings_quoted(self) -> None:
    r = repr(Annotated('Alice', 42))
    self.assertIn("'Alice'", r)
    self.assertIn('42', r)

  def test_iter(self) -> None:
    self.assertEqual(list(Point(1, 2)), [1, 2])

  def test_len(self) -> None:
    self.assertEqual(len(Point()), 2)
    self.assertEqual(len(Sub3D()), 3)

  def test_as_tuple(self) -> None:
    self.assertEqual(Point(1, 2).asTuple(), (1, 2))

  def test_as_dict(self) -> None:
    self.assertEqual(Point(1, 2).asDict(), {'x': 1, 'y': 2})

"""Integration tests for ``order=True`` comparison operators and
the class-creation orderability check."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.ezdata import EZData
from worktoy.waitaminute.ez import UnorderedEZException
from . import EZTest
from ._fixtures import FrozenOrdered, Ordered, Point

if TYPE_CHECKING:  # pragma: no cover
  from typing import Never


class TestEZDataOrdering(EZTest):

  def test_lt(self) -> None:
    self.assertLess(Ordered(1, 2, 3), Ordered(2, 0, 0))

  def test_le_equal(self) -> None:
    self.assertLessEqual(Ordered(1, 2, 3), Ordered(1, 2, 3))

  def test_gt(self) -> None:
    self.assertGreater(Ordered(2, 0, 0), Ordered(1, 9, 9))

  def test_ge_equal(self) -> None:
    self.assertGreaterEqual(Ordered(1, 2, 3), Ordered(1, 2, 3))

  def test_lt_strict_equal_false(self) -> None:
    self.assertFalse(Ordered(1, 2, 3) < Ordered(1, 2, 3))

  def test_unordered_raises(self) -> None:
    with self.assertRaises(UnorderedEZException) as ctx:
      _ = Point(1, 2) < Point(3, 4)
    self.assertEqual(ctx.exception.className, 'Point')

  def test_ordered_diff_type_raises(self) -> None:
    with self.assertRaises(UnorderedEZException):
      _ = Ordered(1, 2, 3) < object()

  def test_class_creation_non_orderable_raises(self) -> None:
    with self.assertRaises(UnorderedEZException) as ctx:
      # noinspection PyUnusedLocal
      class Bad(EZData, order=True):
        a: complex = 1 + 2j
    self.assertEqual(ctx.exception.fieldName, 'a')
    self.assertEqual(ctx.exception.fieldType, complex)

  def test_class_creation_propagates_non_typeerror(self) -> None:
    class Boom(Exception):
      pass

    class Bomb:
      def __lt__(self, other) -> Never:
        raise Boom

    with self.assertRaises(Boom):
      # noinspection PyUnusedLocal
      class BadCustom(EZData, order=True):
        x = Bomb()

  def test_frozen_ordered_combo(self) -> None:
    a = FrozenOrdered(1, 2)
    b = FrozenOrdered(1, 3)
    self.assertLess(a, b)
    self.assertEqual(hash(a), hash(FrozenOrdered(1, 2)))

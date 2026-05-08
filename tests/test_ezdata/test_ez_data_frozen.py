"""Integration tests for ``frozen=True`` ``EZData`` subclasses
(post-construction immutability and hashability)."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.waitaminute.ez import FrozenEZException, UnfrozenHashException
from . import EZTest
from ._fixtures import Frozen, Point


class TestEZDataFrozen(EZTest):

  def test_construction(self) -> None:
    f = Frozen(255, 0, 0)
    self.assertEqual(f.r, 255)
    self.assertEqual(f.g, 0)
    self.assertEqual(f.b, 0)

  def test_setattr_raises(self) -> None:
    f = Frozen(255, 0, 0)
    with self.assertRaises(FrozenEZException) as ctx:
      f.r = 100
    e = ctx.exception
    self.assertEqual(e.fieldName, 'r')
    self.assertEqual(e.className, 'Frozen')
    self.assertEqual(e.oldValue, 255)
    self.assertEqual(e.newValue, 100)

  def test_setitem_raises(self) -> None:
    f = Frozen(255, 0, 0)
    with self.assertRaises(FrozenEZException):
      f['r'] = 100

  def test_hash_works(self) -> None:
    a = Frozen(255, 0, 0)
    b = Frozen(255, 0, 0)
    self.assertEqual(hash(a), hash(b))
    s = {a, b, Frozen(0, 255, 0)}
    self.assertEqual(len(s), 2)

  def test_unfrozen_hash_raises(self) -> None:
    with self.assertRaises(UnfrozenHashException) as ctx:
      hash(Point(1, 2))
    self.assertEqual(ctx.exception.className, 'Point')

  def test_unfrozen_setattr_works(self) -> None:
    p = Point(1, 2)
    p.x = 99
    self.assertEqual(p.x, 99)

  def test_unfrozen_setattr_coerces(self) -> None:
    p = Point(1, 2)
    p.x = '42'
    self.assertEqual(p.x, 42)

  def test_unfrozen_setattr_unknown_key(self) -> None:
    p = Point(1, 2)
    with self.assertRaises(AttributeError):
      p.zzz = 0

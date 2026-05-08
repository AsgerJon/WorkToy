"""Integration tests for ``__getitem__``, ``__setitem__``,
``__delitem__``, and ``__delattr__`` on ``EZData`` subclasses."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.waitaminute import TypeException
from worktoy.waitaminute.ez import EZDeleteException
from . import EZTest
from ._fixtures import Point, Sub3D


class TestEZDataIndexing(EZTest):

  def test_get_int(self) -> None:
    self.assertEqual(Point(1, 2)[0], 1)
    self.assertEqual(Point(1, 2)[1], 2)

  def test_get_int_negative_wrap(self) -> None:
    self.assertEqual(Sub3D(1, 2, 3)[-1 - 420 * 3], 3)

  def test_get_int_overflow(self) -> None:
    with self.assertRaises(IndexError):
      _ = Point(1, 2)[2]

  def test_get_str_hit(self) -> None:
    self.assertEqual(Point(1, 2)['x'], 1)

  def test_get_str_miss(self) -> None:
    with self.assertRaises(KeyError):
      _ = Point(1, 2)['nope']

  def test_get_slice(self) -> None:
    self.assertEqual(Sub3D(1, 2, 3)[0:2], (1, 2))

  def test_get_bad_key(self) -> None:
    with self.assertRaises(TypeException):
      _ = Point(1, 2)[1.5]

  def test_set_int(self) -> None:
    p = Point(1, 2)
    p[0] = 99
    self.assertEqual(p.x, 99)

  def test_set_int_negative_wrap(self) -> None:
    p = Sub3D(0, 0, 0)
    p[-1 - 3 * 420] = 7
    self.assertEqual(p.z, 7)

  def test_set_int_overflow(self) -> None:
    with self.assertRaises(IndexError):
      Point(1, 2)[2] = 99

  def test_set_str_hit(self) -> None:
    p = Point(1, 2)
    p['x'] = 5
    self.assertEqual(p.x, 5)

  def test_set_str_miss(self) -> None:
    with self.assertRaises(KeyError):
      Point(1, 2)['nope'] = 5

  def test_set_slice_iterable(self) -> None:
    p = Sub3D(0, 0, 0)
    p[0:2] = (7, 8)
    self.assertEqual(p.x, 7)
    self.assertEqual(p.y, 8)

  def test_set_slice_str_rejected(self) -> None:
    p = Sub3D(0, 0, 0)
    with self.assertRaises(TypeError) as ctx:
      p[0:2] = 'ab'
    self.assertIn("only to 'str'", str(ctx.exception))

  def test_set_slice_length_mismatch(self) -> None:
    p = Sub3D(0, 0, 0)
    with self.assertRaises(IndexError) as ctx:
      p[0:3] = (1, 2)
    self.assertIn('slots cannot be set to', str(ctx.exception))

  def test_set_bad_key(self) -> None:
    with self.assertRaises(TypeException):
      Point(1, 2)[1.5] = 0

  def test_del_item_raises(self) -> None:
    with self.assertRaises(TypeError):
      del Point(1, 2)[0]

  def test_del_attr_raises(self) -> None:
    with self.assertRaises(EZDeleteException):
      del Point(1, 2).x

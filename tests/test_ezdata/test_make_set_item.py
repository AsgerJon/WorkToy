"""Tests for ``makeSetItem``."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.waitaminute import TypeException
from . import EZTest
from ._factory_helpers import build, slot


class TestMakeSetItem(EZTest):

  def setUp(self) -> None:
    self.cls = build(
      [
        slot('a', int, 0),
        slot('b', int, 0),
        slot('c', int, 0),
      ]
    )

  def test_int_in_range(self) -> None:
    obj = self.cls()
    obj[0] = 99
    self.assertEqual(obj.a, 99)

  def test_int_negative_wrap(self) -> None:
    obj = self.cls()
    obj[-1 - 3 * 420] = 7
    self.assertEqual(obj.c, 7)

  def test_int_positive_overflow(self) -> None:
    obj = self.cls()
    with self.assertRaises(IndexError):
      obj[3] = 99

  def test_str_hit(self) -> None:
    obj = self.cls()
    obj['b'] = 5
    self.assertEqual(obj.b, 5)

  def test_str_miss(self) -> None:
    obj = self.cls()
    with self.assertRaises(KeyError):
      obj['nope'] = 1

  def test_slice_iterable(self) -> None:
    obj = self.cls()
    obj[0:2] = (7, 8)
    self.assertEqual(obj.a, 7)
    self.assertEqual(obj.b, 8)

  def test_slice_str_rejected(self) -> None:
    obj = self.cls()
    with self.assertRaises(TypeError) as ctx:
      obj[0:2] = 'lol'
    self.assertIn("only to 'str' not to 'bytes' or 'bytearray'",
                  str(ctx.exception)
                  )

  def test_slice_length_mismatch(self) -> None:
    obj = self.cls()
    with self.assertRaises(IndexError) as ctx:
      obj[0:3] = (1, 2)
    self.assertIn('slots cannot be set to', str(ctx.exception))

  def test_bad_key_type(self) -> None:
    obj = self.cls()
    with self.assertRaises(TypeException):
      obj[3.14] = 1

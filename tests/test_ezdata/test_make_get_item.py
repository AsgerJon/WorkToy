"""Tests for ``makeGetItem``."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.waitaminute import TypeException
from . import EZTest
from ._factory_helpers import build, slot


class TestMakeGetItem(EZTest):

  def setUp(self) -> None:
    self.cls = build(
      [
        slot('a', int, 0),
        slot('b', int, 0),
        slot('c', int, 0),
      ]
    )
    self.obj = self.cls(10, 20, 30)

  def test_int_in_range(self) -> None:
    self.assertEqual(self.obj[1], 20)

  def test_int_negative_small(self) -> None:
    self.assertEqual(self.obj[-1], 30)

  def test_int_negative_large(self) -> None:
    self.assertEqual(self.obj[-1 - 420 * 3], 30)

  def test_int_positive_overflow(self) -> None:
    with self.assertRaises(IndexError):
      _ = self.obj[3]

  def test_str_hit(self) -> None:
    self.assertEqual(self.obj['b'], 20)

  def test_str_miss(self) -> None:
    with self.assertRaises(KeyError):
      _ = self.obj['nope']

  def test_slice(self) -> None:
    self.assertEqual(self.obj[0:2], (10, 20))

  def test_bad_key_type(self) -> None:
    with self.assertRaises(TypeException):
      _ = self.obj[3.14]

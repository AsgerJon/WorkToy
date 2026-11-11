"""
PromiseUnpack promises 'unpack' from 'worktoy.utilities'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.mcls import BaseObject
from worktoy.utilities import unpack
from worktoy.waitaminute import UnpackException


class PromiseUnpack(TestCase):
  """
  'unpack' flattens the iterables among its arguments into one tuple,
  all the way down, or one level with 'shallow=True'; with
  'strict=False', a function taking '*args' accepts its values loose or
  in one list alike. Text, 'str',
  'bytes' and 'bytearray', is never split, and an object that claims to
  iterate but refuses, as a worktoy class does, is kept whole. By
  default a call with nothing iterable raises 'UnpackException';
  'strict=False' passes the arguments through instead. Source: the
  'unpack' docstring and its examples.
  """

  def test_flattens(self) -> None:
    self.assertEqual(unpack([1, 2], (3, [4, 5])), (1, 2, 3, 4, 5))
    squares = (n * n for n in (1, 2, 3))
    self.assertEqual(unpack(squares, [16]), (1, 4, 9, 16))

  def test_both_spellings(self) -> None:
    def total(*numbers: int) -> int:
      return sum(unpack(*numbers, strict=False))

    self.assertEqual(total(1, 2, 3), 6)
    self.assertEqual(total([1, 2, 3]), 6)

  def test_shallow(self) -> None:
    self.assertEqual(unpack([1, [2, 3]], shallow=True), (1, [2, 3]))

  def test_text_kept_whole(self) -> None:
    self.assertEqual(unpack('abc', [1, 2]), ('abc', 1, 2))
    self.assertEqual(unpack(b'de', bytearray(b'fg'), [3]),
                     (b'de', bytearray(b'fg'), 3))

  def test_refusing_iterable_kept_whole(self) -> None:
    class Plain(BaseObject):
      pass

    self.assertEqual(unpack(Plain, [1]), (Plain, 1))

  def test_nothing_iterable(self) -> None:
    with self.assertRaises(UnpackException) as context:
      unpack(1, 2)
    self.assertIsInstance(context.exception, ValueError)
    self.assertEqual(context.exception.posArgs, (1, 2))
    with self.assertRaises(UnpackException) as context:
      unpack()
    self.assertEqual(context.exception.posArgs, ())

  def test_not_strict(self) -> None:
    self.assertEqual(unpack(1, 2, strict=False), (1, 2))
    self.assertEqual(unpack(strict=False), ())

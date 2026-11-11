"""
PromiseReplaceFlex promises 'replaceFlex' from 'worktoy.utilities'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.utilities import replaceFlex


class PromiseReplaceFlex(TestCase):
  """
  'replaceFlex' replaces the 'n'-th occurrence of a substring, counted
  from one, the first by default, and overlapping occurrences count. A
  text with fewer occurrences comes back unchanged, and an 'n' below
  one raises 'ValueError'. Source: the 'replaceFlex' docstring and its
  examples.
  """

  def test_nth(self) -> None:
    self.assertEqual(replaceFlex('foo bar foo baz foo', 'foo', 'X', 2),
                     'foo bar X baz foo')

  def test_first_by_default(self) -> None:
    self.assertEqual(replaceFlex('foo foo', 'foo', 'X'), 'X foo')

  def test_overlapping(self) -> None:
    self.assertEqual(replaceFlex('aaa', 'aa', 'X', 2), 'aX')

  def test_too_few(self) -> None:
    self.assertEqual(replaceFlex('abc', 'x', 'y'), 'abc')
    self.assertEqual(replaceFlex('foo', 'foo', 'X', 2), 'foo')

  def test_n_below_one(self) -> None:
    with self.assertRaises(ValueError):
      replaceFlex('foo', 'foo', 'X', 0)
    with self.assertRaises(ValueError):
      replaceFlex('foo', 'foo', 'X', -1)

"""
PromiseSliceLen promises 'sliceLen' from 'worktoy.utilities'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.utilities import sliceLen


class PromiseSliceLen(TestCase):
  """
  'sliceLen' gives how many elements a slice selects from a sequence of
  the given length, as 'len(sequence[sliceObj])' would. A step of zero
  raises 'ValueError'. Source: the 'sliceLen' docstring and its
  examples.
  """

  def test_counts(self) -> None:
    self.assertEqual(sliceLen(slice(0, 10, 2), 10), 5)
    self.assertEqual(sliceLen(slice(None, None, -1), 4), 4)
    self.assertEqual(sliceLen(slice(5, 100), 10), 5)

  def test_agrees_with_slicing(self) -> None:
    sequence = 'abcdefghij'
    for sliceObj in (slice(1, -1, 3), slice(-3, None), slice(8, 2, -2)):
      with self.subTest(sliceObj=sliceObj):
        self.assertEqual(sliceLen(sliceObj, 10), len(sequence[sliceObj]))

  def test_zero_step(self) -> None:
    with self.assertRaises(ValueError):
      sliceLen(slice(0, 10, 0), 10)

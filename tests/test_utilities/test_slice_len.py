"""
TestSliceLen tests 'sliceLen' from 'worktoy.utilities'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.utilities import sliceLen
from worktoy.work_test.samplers import IntSampler
from . import UtilitiesTest


class TestSliceLen(UtilitiesTest):
  """
  'sliceLen' answers how many elements a slice selects from a sequence
  of a given length, which a sequence must know before it can refuse an
  assignment of the wrong size. The tests pin the docstring examples
  and that the count agrees with the length of the actual slice of a
  range for random bounds and every usual step.
  """

  def test_docstring_examples(self) -> None:
    self.assertEqual(sliceLen(slice(0, 10, 2), 10), 5)
    self.assertEqual(sliceLen(slice(None, None, -1), 4), 4)
    self.assertEqual(sliceLen(slice(5, 100), 10), 5)

  def test_empty_selections(self) -> None:
    self.assertEqual(sliceLen(slice(5, 2), 10), 0)
    self.assertEqual(sliceLen(slice(None), 0), 0)
    self.assertEqual(sliceLen(slice(20, 30), 10), 0)

  def test_zero_step_refused(self) -> None:
    with self.assertRaises(ValueError):
      sliceLen(slice(0, 10, 0), 10)

  def test_agrees_with_range(self) -> None:
    self.randomInteger = IntSampler(-12, 12, seed=8, size=2)
    for step in (-3, -2, -1, 1, 2, 3):
      for _ in range(10):
        start, stop = self.randomInteger.row
        sliceObj = slice(start, stop, step)
        with self.subTest(sliceObj=sliceObj):
          self.assertEqual(sliceLen(sliceObj, 10), len(range(10)[sliceObj]))

  def test_open_bounds_agree_with_range(self) -> None:
    for step in (-2, -1, 1, 2):
      for length in range(0, 7):
        sliceObj = slice(None, None, step)
        with self.subTest(step=step, length=length):
          expected = len(range(length)[sliceObj])
          self.assertEqual(sliceLen(sliceObj, length), expected)

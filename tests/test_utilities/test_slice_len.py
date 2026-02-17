"""
TestSliceLen tests the 'sliceLen' function from the 'worktoy.utilities'
module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import UtilitiesTest
from worktoy.utilities import sliceLen

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestSliceLen(UtilitiesTest):
  """
  TestSliceLen tests the 'sliceLen' function from the 'worktoy.utilities'
  module.
  """

  def testFullSlice(self) -> None:
    """Tests that a full slice includes the whole sequence."""
    for length in [0, 1, 10, 42]:
      self.assertEqual(sliceLen(slice(None, None), length), length)

  def testSimpleForwardSlice(self) -> None:
    """Tests simple forward slices with positive step."""
    self.assertEqual(sliceLen(slice(1, 4), 10), 3)
    self.assertEqual(sliceLen(slice(0, 10), 10), 10)
    self.assertEqual(sliceLen(slice(3, 3), 10), 0)
    self.assertEqual(sliceLen(slice(7, 20), 10), 3)
    self.assertEqual(sliceLen(slice(0, 100), 4), 4)

  def testNegativeIndices(self) -> None:
    """Tests slices using negative start or stop."""
    self.assertEqual(sliceLen(slice(-3, None), 10), 3)
    self.assertEqual(sliceLen(slice(None, -2), 10), 8)
    self.assertEqual(sliceLen(slice(-5, -2), 10), 3)
    self.assertEqual(sliceLen(slice(-100, 100), 10), 10)

  def testStepSlices(self) -> None:
    """Tests slices with various step values."""
    self.assertEqual(sliceLen(slice(None, None, 2), 6), 3)
    self.assertEqual(sliceLen(slice(1, 10, 2), 10), 5)
    self.assertEqual(sliceLen(slice(1, 10, 3), 10), 3)
    self.assertEqual(sliceLen(slice(0, 10, 5), 10), 2)
    self.assertEqual(sliceLen(slice(0, 10, 100), 10), 1)

  def testReverseSlices(self) -> None:
    """Tests slices with negative steps."""
    self.assertEqual(sliceLen(slice(None, None, -1), 5), 5)
    self.assertEqual(sliceLen(slice(4, None, -1), 5), 5)
    self.assertEqual(sliceLen(slice(4, 1, -1), 5), 3)
    self.assertEqual(sliceLen(slice(3, -100, -1), 4), 4)
    self.assertEqual(sliceLen(slice(-1, -6, -1), 10), 5)

  def testEmptySlices(self) -> None:
    """Tests slices that should return zero length."""
    self.assertEqual(sliceLen(slice(10, 0), 4), 0)
    self.assertEqual(sliceLen(slice(3, 3), 4), 0)
    self.assertEqual(sliceLen(slice(0, 0, -1), 4), 0)
    self.assertEqual(sliceLen(slice(1, 5, -1), 4), 0)

  def testZeroStep(self) -> None:
    """Tests that step=0 raises ValueError, as in Python slice/range."""
    with self.assertRaises(ValueError):
      sliceLen(slice(None, None, 0), 10)

  def testZeroLength(self) -> None:
    """Tests with empty sequence."""
    self.assertEqual(sliceLen(slice(None, None), 0), 0)
    self.assertEqual(sliceLen(slice(1, 5), 0), 0)
    self.assertEqual(sliceLen(slice(-100, 100), 0), 0)

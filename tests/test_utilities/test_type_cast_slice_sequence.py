"""
TestTypeCastSliceSequence subclasses 'UtilitiesTest' and pins that
'typeCast' to 'slice' reads a sequence as the arguments of 'slice' do: a
single value is the stop, two are the start and the stop, and three add
the step. It used to read a single value as the start, so
'typeCast(slice, [5])' was 'slice(5, None, None)' where 'slice(*[5])' is
'slice(None, 5, None)'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.utilities import typeCast

from . import UtilitiesTest


class TestTypeCastSliceSequence(UtilitiesTest):
  """
  TestTypeCastSliceSequence provides tests for 'typeCast' to 'slice' from
  a sequence.
  """

  def test_lengths(self) -> None:
    """Each length reads as 'slice' reads its arguments."""
    for value in ([5], (1, 5), [1, 5, 2]):
      with self.subTest(value=value):
        self.assertEqual(typeCast(slice, value), slice(*value))

"""
TestArrangementPermutation subclasses 'UtilitiesTest' and pins that an
'Arrangement' refuses a 'forward' recipe that is not a permutation of the
positions of its items. Only the length used to be checked, so a recipe
repeating a position built a wrong inverse, and restoring an applied
tuple lost a value.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.utilities.combinatorics import Arrangement

from . import UtilitiesTest


class TestArrangementPermutation(UtilitiesTest):
  """
  TestArrangementPermutation provides tests for the 'forward' recipe of
  an 'Arrangement'.
  """

  def test_repeated_position_refused(self) -> None:
    """A recipe repeating a position raises 'ValueError'."""
    with self.assertRaises(ValueError) as context:
      Arrangement(('a', 'b', 'c'), (0, 0, 2))
    self.assertIn('permutation', str(context.exception))

  def test_position_out_of_range_refused(self) -> None:
    """A recipe naming a position past the items raises 'ValueError'."""
    with self.assertRaises(ValueError):
      Arrangement(('a', 'b'), (0, 2))

  def test_permutation_round_trip(self) -> None:
    """A permutation restores what it applies."""
    arrangement = Arrangement(('a', 'b', 'c'), (2, 0, 1))
    self.assertEqual(arrangement.restoreFrom(*arrangement.applyTo(1, 2, 3)),
                     (1, 2, 3))

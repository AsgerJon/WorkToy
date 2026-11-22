"""
RefusedArrangement holds the refusals that belong with
'design.promises.utilities.promise_arrangement'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.utilities.combinatorics import Arrangement


class RefusedArrangement(TestCase):
  """
  Each of the following is refused, and the exception named is the one raised
  as of 1.2.3. 'applyTo' and 'restoreFrom' raise 'ValueError' for the wrong
  number of values. Source: the 'Arrangement' docstring and the docstrings of
  'applyTo' and 'restoreFrom'.
  """

  def test_wrong_count_1(self) -> None:
    arrangement = Arrangement(('north', 'east', 'south'), (2, 0, 1))
    with self.assertRaises(Exception) as refused:
      arrangement.applyTo(0, 90)
    self.assertIsInstance(refused.exception, ValueError)

  def test_wrong_count_2(self) -> None:
    arrangement = Arrangement(('north', 'east', 'south'), (2, 0, 1))
    with self.assertRaises(Exception) as refused:
      arrangement.restoreFrom(0, 90, 180, 270)
    self.assertIsInstance(refused.exception, ValueError)

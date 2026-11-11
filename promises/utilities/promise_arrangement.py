"""
PromiseArrangement promises 'Arrangement' from
'worktoy.utilities.combinatorics'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.utilities.combinatorics import Arrangement


class PromiseArrangement(TestCase):
  """
  'Arrangement(items, forward)' is one ordering of 'items'. Slot 'k' of
  'values' holds 'items[forward[k]]', and 'inverse' tells, for each
  item, the slot it went to. 'applyTo' puts values given in the order
  of 'items' into the order of 'values', and 'restoreFrom' undoes it;
  either raises 'ValueError' for the wrong number of values. Source:
  the 'Arrangement' docstring and the docstrings of 'applyTo' and
  'restoreFrom'.
  """

  def test_recipes(self) -> None:
    items = ('north', 'east', 'south')
    arrangement = Arrangement(items, (2, 0, 1))
    self.assertEqual(arrangement.items, items)
    self.assertEqual(arrangement.forward, (2, 0, 1))
    self.assertEqual(arrangement.values, ('south', 'north', 'east'))
    for k in range(3):
      with self.subTest(k=k):
        values, inverse = arrangement.values, arrangement.inverse
        self.assertIs(values[k], items[arrangement.forward[k]])
        self.assertIs(values[inverse[k]], items[k])

  def test_apply_and_restore(self) -> None:
    arrangement = Arrangement(('north', 'east', 'south'), (2, 0, 1))
    applied = arrangement.applyTo(0, 90, 180)
    self.assertEqual(applied, (180, 0, 90))
    self.assertEqual(arrangement.restoreFrom(*applied), (0, 90, 180))

  def test_wrong_count(self) -> None:
    arrangement = Arrangement(('north', 'east', 'south'), (2, 0, 1))
    with self.assertRaises(ValueError):
      arrangement.applyTo(0, 90)
    with self.assertRaises(ValueError):
      arrangement.restoreFrom(0, 90, 180, 270)

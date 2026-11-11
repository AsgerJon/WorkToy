"""
DeprecatedMemberIndex holds the promise of 'index' on the members of
'KeeNum' and 'KeeFlags', which ends at the next major update.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import warnings
from unittest import TestCase

from worktoy.keenum import KeeNum, Kee

from ..keenum._file_access import FileAccess
from ..keenum._week_day import WeekDay


class DeprecatedMemberIndex(TestCase):
  """
  Deprecated in 1.2.0: 'index' on a member of an enumeration.

  Promised in 1.1.0 and owed through 1.x: the index of a 'KeeNum' member
  is the number of members declared before it, a base's members first,
  and the index of a 'KeeFlags' member is its bit mask, flag 'i' being
  bit 'i' in the order declared.

  Why it ends: an index is a position in a class, and its point is to
  be handed to the class to get the member. A member is one object
  shared by its enumeration and every subclass of it, and on its own it
  does not care where it lives. It can carry one index, where two
  classes may hold it at two positions, and a mask carried from one
  flags class to another names another member there. The position
  belongs to the class, which still answers a subscript by position:
  'promises/keenum/promise_resolution.py'.
  """

  def setUp(self) -> None:
    silenced = warnings.catch_warnings()
    silenced.__enter__()
    self.addCleanup(silenced.__exit__, None, None, None)
    warnings.simplefilter('ignore')

  def test_declared_order(self) -> None:
    class Size(KeeNum):
      SMALL = Kee[int](1)
      MEDIUM = Kee[int](2)
      LARGE = Kee[int](2)

    self.assertEqual([m.index for m in Size], [0, 1, 2])
    self.assertEqual(WeekDay.MONDAY.index, 0)

  def test_inherited_first(self) -> None:
    class Size(KeeNum):
      SMALL = Kee[int](1)

    class BigSize(Size):
      HUGE = Kee[int](9)

    self.assertEqual(BigSize.HUGE.index, 1)

  def test_flags_mask(self) -> None:
    self.assertEqual([m.index for m in FileAccess], list(range(8)))

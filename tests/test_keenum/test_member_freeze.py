"""
TestMemberFreeze tests that enumeration members are frozen once their
class exists: any attribute assignment or deletion on a member raises
'KeeWriteOnceError', for 'KeeNum' and 'KeeFlags' alike.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.keenum import Kee, KeeNum, KeeFlag, KeeFlags
from worktoy.waitaminute.keenum import KeeWriteOnceError

from . import KeeTest

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestMemberFreeze(KeeTest):
  """
  TestMemberFreeze tests the instance-level freeze on enumeration
  members. The 'KeeNum' side has carried this freeze through 'KeeBase'
  all along; these tests pin the 'KeeFlags' side to the same contract
  and cover the attribute-deletion guard on both.
  """

  def test_kee_flags_attribute_set(self) -> None:
    """
    Setting any attribute on a 'KeeFlags' member raises
    'KeeWriteOnceError', whether the attribute is an ad-hoc name, the
    member's bitmask identity, or the 'value' field.
    """

    class KeyMod(KeeFlags):
      CTRL = KeeFlag()
      SHIFT = KeeFlag()

    with self.assertRaises(KeeWriteOnceError) as context:
      KeyMod.CTRL.lmao = True
    e = context.exception
    self.assertIs(e.member, KeyMod.CTRL)
    self.assertEqual(e.attribute, 'lmao')

    with self.assertRaises(KeeWriteOnceError):
      KeyMod.CTRL.__member_index__ = 9
    self.assertEqual(KeyMod.CTRL.index, 1)

    with self.assertRaises(KeeWriteOnceError):
      KeyMod.CTRL.value = 9
    self.assertEqual(KeyMod.CTRL.value, 1)

  def test_kee_flags_attribute_delete(self) -> None:
    """
    Deleting any attribute on a 'KeeFlags' member raises
    'KeeWriteOnceError'.
    """

    class KeyMod(KeeFlags):
      CTRL = KeeFlag()
      SHIFT = KeeFlag()

    with self.assertRaises(KeeWriteOnceError) as context:
      del KeyMod.SHIFT.__member_index__
    e = context.exception
    self.assertIs(e.member, KeyMod.SHIFT)
    self.assertEqual(e.attribute, '__member_index__')
    self.assertEqual(KeyMod.SHIFT.index, 2)

  def test_kee_num_attribute_delete(self) -> None:
    """
    Deleting any attribute on a 'KeeNum' member raises
    'KeeWriteOnceError', matching the assignment guard 'KeeBase' has
    always had.
    """

    class WeekDay(KeeNum):
      MONDAY = Kee[str]('Mandag')

    with self.assertRaises(KeeWriteOnceError) as context:
      del WeekDay.MONDAY.__field_kee__
    e = context.exception
    self.assertIs(e.member, WeekDay.MONDAY)
    self.assertEqual(e.attribute, '__field_kee__')
    self.assertEqual(WeekDay.MONDAY.value, 'Mandag')

  def test_operators_unaffected(self) -> None:
    """
    The bitwise operators only read member state, so they keep working
    on frozen members.
    """

    class KeyMod(KeeFlags):
      CTRL = KeeFlag()
      SHIFT = KeeFlag()

    self.assertIs(KeyMod.CTRL | KeyMod.SHIFT, KeyMod.CTRL_SHIFT)
    self.assertIs(KeyMod.CTRL & KeyMod.CTRL_SHIFT, KeyMod.CTRL)
    self.assertIs(KeyMod.CTRL ^ KeyMod.CTRL_SHIFT, KeyMod.SHIFT)
    self.assertIs(~KeyMod.NULL, KeyMod.CTRL_SHIFT)

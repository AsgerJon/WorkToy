"""
TestMemberRebind tests that the class attribute names holding enumeration
members can neither be rebound nor deleted, for 'KeeNum' and 'KeeFlags'
alike, while ordinary class attributes remain writable and deletable.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import Kee, KeeNum, KeeFlag, KeeFlags
from worktoy.waitaminute.keenum import KeeWriteOnceError

from . import KeeTest


class TestMemberRebind(KeeTest):
  """
  TestMemberRebind tests the class-level write-once guard on the
  enumeration metaclasses: a name resolving to a member refuses both
  reassignment and deletion with 'KeeWriteOnceError', and an attempted
  reassignment leaves the member and the resolution caches untouched.
  """

  def test_kee_num_rebind(self) -> None:
    """
    Rebinding a 'KeeNum' member name raises 'KeeWriteOnceError' and
    leaves both the attribute and the resolution caches serving the
    original member.
    """

    class WeekDay(KeeNum):
      MONDAY = Kee[str]('Mandag')
      TUESDAY = Kee[str]('Tirsdag')

    monday = WeekDay.MONDAY
    with self.assertRaises(KeeWriteOnceError) as context:
      WeekDay.MONDAY = 'breh'
    e = context.exception
    self.assertIs(e.member, monday)
    self.assertEqual(e.attribute, 'MONDAY')
    self.assertIs(WeekDay.MONDAY, monday)
    self.assertIs(WeekDay('Mandag'), monday)
    self.assertIs(WeekDay('monday'), monday)

  def test_kee_num_delete(self) -> None:
    """
    Deleting a 'KeeNum' member name raises 'KeeWriteOnceError' and the
    enumeration keeps all of its members.
    """

    class WeekDay(KeeNum):
      MONDAY = Kee[str]('Mandag')
      TUESDAY = Kee[str]('Tirsdag')

    with self.assertRaises(KeeWriteOnceError) as context:
      del WeekDay.TUESDAY
    e = context.exception
    self.assertIs(e.member, WeekDay.TUESDAY)
    self.assertEqual(e.attribute, 'TUESDAY')
    self.assertEqual(len(WeekDay), 2)

  def test_kee_num_ordinary_attributes(self) -> None:
    """
    Ordinary class attributes on a 'KeeNum' class stay writable and
    deletable; only the member names are protected.
    """

    class WeekDay(KeeNum):
      MONDAY = Kee[str]('Mandag')
      helper = 'breh'

    WeekDay.helper = 'lmao'
    self.assertEqual(WeekDay.helper, 'lmao')
    del WeekDay.helper
    self.assertNotIn('helper', WeekDay.__dict__)

  def test_kee_flags_rebind(self) -> None:
    """
    Rebinding a 'KeeFlags' member name, single-flag or combined, raises
    'KeeWriteOnceError' and leaves the attribute serving the original
    member.
    """

    class KeyMod(KeeFlags):
      CTRL = KeeFlag()
      SHIFT = KeeFlag()

    ctrl = KeyMod.CTRL
    with self.assertRaises(KeeWriteOnceError) as context:
      KeyMod.CTRL = 'breh'
    e = context.exception
    self.assertIs(e.member, ctrl)
    self.assertEqual(e.attribute, 'CTRL')
    self.assertIs(KeyMod.CTRL, ctrl)

    combined = KeyMod.CTRL_SHIFT
    with self.assertRaises(KeeWriteOnceError) as context:
      KeyMod.CTRL_SHIFT = 'breh'
    e = context.exception
    self.assertIs(e.member, combined)
    self.assertEqual(e.attribute, 'CTRL_SHIFT')
    self.assertIs(KeyMod.CTRL_SHIFT, combined)

  def test_kee_flags_delete(self) -> None:
    """
    Deleting a 'KeeFlags' member name raises 'KeeWriteOnceError' and the
    enumeration keeps all of its members.
    """

    class KeyMod(KeeFlags):
      CTRL = KeeFlag()
      SHIFT = KeeFlag()

    with self.assertRaises(KeeWriteOnceError) as context:
      del KeyMod.SHIFT
    e = context.exception
    self.assertIs(e.member, KeyMod.SHIFT)
    self.assertEqual(e.attribute, 'SHIFT')
    self.assertEqual(len(KeyMod), 4)

  def test_kee_flags_ordinary_attributes(self) -> None:
    """
    Ordinary class attributes on a 'KeeFlags' class stay writable and
    deletable; only the member names are protected.
    """

    class KeyMod(KeeFlags):
      CTRL = KeeFlag()
      helper = 'breh'

    KeyMod.helper = 'lmao'
    self.assertEqual(KeyMod.helper, 'lmao')
    del KeyMod.helper
    self.assertNotIn('helper', KeyMod.__dict__)

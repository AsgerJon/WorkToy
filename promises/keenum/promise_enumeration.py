"""
PromiseEnumeration promises the enumeration class and its members, from
'worktoy.keenum'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import copy
import pickle
from unittest import TestCase

from worktoy.desc import AttriBox
from worktoy.keenum import KeeNum, Kee, KeeBase, KeeMeta, AccessNum
from worktoy.mcls import BaseObject
from worktoy.utilities import typeCast
from worktoy.waitaminute import TypeException
from worktoy.waitaminute.keenum import KeeWriteOnceError

from ._week_day import WeekDay


class PromiseEnumeration(TestCase):
  """
  An enumeration iterates its members, gives their count
  with 'len' and holds them in 'members'; 'bool' is True when it has
  any. 'x in Day' and 'isinstance(x, Day)' are True for its members and
  those of its subclasses, by identity, so a name is never 'in' it.
  'valueType' is the type of the values, an enumeration without members
  raising 'TypeError'. A member has 'name', 'value' and
  'valueType', is an instance of its enumeration and of 'KeeBase', is
  equal to itself alone and hashes where its value hashes; a copy, a deep
  copy and a pickle round trip give the member itself. Setting or
  deleting an attribute of a member, or rebinding a member's name on its
  class, raises 'KeeWriteOnceError', an 'AttributeError'. An 'AttriBox'
  over an enumeration and 'typeCast' take what a call takes. A subclass
  of 'KeeMeta' builds enumerations based on its own root, 'keeNum'.
  'AccessNum' enumerates 'GET', 'SET' and 'DELETE'. Source: the
  docstrings of 'KeeMeta', 'KeeBase', 'KeeMetaMeta' and 'AccessNum'.

  Taken back in 1.2.0, with its reason in 'promises/confessions':
  iteration in index order. Deprecated in 1.2.0, with its reason in
  'promises/deprecations': 'index' on a member.
  """

  def test_class(self) -> None:
    self.assertEqual(list(WeekDay), [WeekDay.MONDAY, WeekDay.TUESDAY,
                                     WeekDay.WEDNESDAY])
    self.assertEqual(len(WeekDay), 3)
    self.assertEqual(tuple(WeekDay.members), tuple(WeekDay))
    self.assertTrue(WeekDay)
    self.assertIn(WeekDay.MONDAY, WeekDay)
    self.assertNotIn('MONDAY', WeekDay)
    self.assertIsInstance(WeekDay.MONDAY, WeekDay)
    self.assertIs(WeekDay.valueType, str)

  def test_empty(self) -> None:
    class Nothing(KeeNum):
      pass

    self.assertFalse(Nothing)
    self.assertEqual(len(Nothing), 0)
    with self.assertRaises(TypeError):
      _ = Nothing.valueType

  def test_subclass_members(self) -> None:
    class LongWeek(WeekDay):
      THURSDAY = Kee[str]('Torsdag')

    self.assertIn(LongWeek.THURSDAY, WeekDay)
    self.assertIsInstance(LongWeek.THURSDAY, WeekDay)

  def test_member(self) -> None:
    monday = WeekDay.MONDAY
    self.assertEqual((monday.name, monday.value), ('MONDAY', 'Mandag'))
    self.assertIs(monday.valueType, str)
    self.assertIs(type(monday), WeekDay)
    self.assertIsInstance(monday, KeeBase)
    self.assertEqual(monday, WeekDay.MONDAY)
    self.assertNotEqual(monday, WeekDay.TUESDAY)
    self.assertNotEqual(monday, 'Mandag')
    self.assertEqual({monday: 'start'}[WeekDay.MONDAY], 'start')

  def test_unhashable_value(self) -> None:
    class Shopping(KeeNum):
      FRUIT = Kee[list](['apple'])

    with self.assertRaises(TypeError):
      hash(Shopping.FRUIT)

  def test_copies_are_the_member(self) -> None:
    monday = WeekDay.MONDAY
    self.assertIs(copy.copy(monday), monday)
    self.assertIs(copy.deepcopy(monday), monday)
    self.assertIs(pickle.loads(pickle.dumps(monday)), monday)

  def test_frozen(self) -> None:
    with self.assertRaises(KeeWriteOnceError) as context:
      WeekDay.MONDAY.value = 'Mon'
    e = context.exception
    self.assertIsInstance(e, AttributeError)
    self.assertIs(e.keeNum, WeekDay)
    self.assertIs(e.member, WeekDay.MONDAY)
    self.assertEqual(e.attribute, 'value')
    with self.assertRaises(KeeWriteOnceError):
      del WeekDay.MONDAY.value
    with self.assertRaises(KeeWriteOnceError):
      WeekDay.MONDAY = 'Mon'

  def test_conversion(self) -> None:
    class Calendar(BaseObject):
      day = AttriBox[WeekDay](WeekDay.MONDAY)

    calendar = Calendar()
    calendar.day = 'tuesday'
    self.assertIs(calendar.day, WeekDay.TUESDAY)
    calendar.day = 'Onsdag'
    self.assertIs(calendar.day, WeekDay.WEDNESDAY)
    with self.assertRaises(TypeException):
      calendar.day = 'Funday'
    self.assertIs(typeCast(WeekDay, 'monday'), WeekDay.MONDAY)

  def test_own_metaclass(self) -> None:
    class FontMeta(KeeMeta):
      pass

    class FontFamily(FontMeta.keeNum):
      ARIAL = Kee[int](1)
      TIMES = Kee[int](2)

    self.assertIsInstance(FontFamily, FontMeta)
    self.assertIs(FontMeta.keeNum, FontMeta.keeNum)
    self.assertIs(KeeMeta.keeNum, KeeNum)

  def test_access_num(self) -> None:
    self.assertEqual([m.value for m in AccessNum],
                     ['__get__', '__set__', '__delete__'])
    self.assertEqual([m.name for m in AccessNum], ['GET', 'SET', 'DELETE'])

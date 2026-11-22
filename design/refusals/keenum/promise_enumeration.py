"""
RefusedEnumeration holds the refusals that belong with
'design.promises.keenum.promise_enumeration'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.desc import AttriBox
from worktoy.keenum import KeeNum, Kee
from worktoy.mcls import BaseObject
from worktoy.waitaminute import TypeException
from worktoy.waitaminute.keenum import KeeWriteOnceError

from ...promises.keenum._week_day import WeekDay


class RefusedEnumeration(TestCase):
  """
  Each of the following is refused, and the exception named is the one raised
  as of 1.2.3. 'valueType' of an enumeration without members raises
  'TypeError'. Setting or deleting an attribute of a member, or rebinding a
  member's name on its class, raises 'KeeWriteOnceError', an
  'AttributeError'. Source: the docstrings of 'KeeMeta', 'KeeBase',
  'KeeMetaMeta' and 'AccessNum'.
  """

  def test_empty(self) -> None:
    class Nothing(KeeNum):
      pass

    with self.assertRaises(Exception) as refused:
      _ = Nothing.valueType
    self.assertIsInstance(refused.exception, TypeError)

  def test_unhashable_value(self) -> None:
    class Shopping(KeeNum):
      FRUIT = Kee[list](['apple'])

    with self.assertRaises(Exception) as refused:
      hash(Shopping.FRUIT)
    self.assertIsInstance(refused.exception, TypeError)

  def test_frozen_1(self) -> None:
    with self.assertRaises(Exception) as refused:
      WeekDay.MONDAY.value = 'Mon'
    self.assertIsInstance(refused.exception, KeeWriteOnceError)

  def test_frozen_2(self) -> None:
    with self.assertRaises(Exception) as refused:
      del WeekDay.MONDAY.value
    self.assertIsInstance(refused.exception, KeeWriteOnceError)

  def test_frozen_3(self) -> None:
    with self.assertRaises(Exception) as refused:
      WeekDay.MONDAY = 'Mon'
    self.assertIsInstance(refused.exception, KeeWriteOnceError)

  def test_conversion(self) -> None:
    class Calendar(BaseObject):
      day = AttriBox[WeekDay](WeekDay.MONDAY)

    calendar = Calendar()
    calendar.day = 'tuesday'
    calendar.day = 'Onsdag'
    with self.assertRaises(Exception) as refused:
      calendar.day = 'Funday'
    self.assertIsInstance(refused.exception, TypeException)

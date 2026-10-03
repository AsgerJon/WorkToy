"""
TestKeeMembership subclasses 'KeeTest' from the 'tests.test_keenum'
package and pins how an enumeration decides that an object is one of its
members. That decision lies behind 'isinstance', 'in', and the first step
of resolving a member by calling or subscripting the enumeration, and it
must not ask the object's own '__eq__'. A value class whose '__eq__' reads
the other operand, like 'RGB', otherwise raises before the lookup by value
is reached, while an object equal to everything, like 'unittest.mock.ANY',
counts as a member and comes back from the lookup as itself. The last
tests pin the membership that must stay as it is: the members themselves,
including those an enumeration shares with the enumerations derived from
it.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest.mock import ANY

from worktoy.desc import AttriBox
from worktoy.mcls import BaseObject
from worktoy.utilities import typeCast
from worktoy.waitaminute.keenum import KeeResolveError

from . import KeeTest
from .examples import ColorNum, RGB, RootRGB, MoreRGB, WeekDay


class TestKeeMembership(KeeTest):
  """
  TestKeeMembership provides tests for the membership decision of
  'KeeMeta', with objects whose '__eq__' raises on a member or answers
  'True' to anything.
  """

  def test_value_resolves(self) -> None:
    """
    Calling 'ColorNum' with an 'RGB' value finds the member holding an
    equal value. 'RGB.__eq__' reads the colour channels of the other
    operand, so asking it about a member raises, and the membership step
    ahead of the lookup by value must not ask it.
    """
    for member in ColorNum:
      with self.subTest(member=member.name):
        self.assertIs(ColorNum(RGB(*member.value)), member)

  def test_value_is_not_member(self) -> None:
    """
    An 'RGB' value is neither an instance of 'ColorNum' nor in it, and
    saying so does not raise.
    """
    red = RGB(255, 0, 0)
    self.assertNotIsInstance(red, ColorNum)
    self.assertNotIn(red, ColorNum)

  def test_equal_to_anything_is_not_member(self) -> None:
    """
    'unittest.mock.ANY' is equal to everything, and yet neither an
    instance of 'WeekDay' nor in it.
    """
    self.assertNotIsInstance(ANY, WeekDay)
    self.assertNotIn(ANY, WeekDay)

  def test_equal_to_anything_does_not_resolve(self) -> None:
    """
    Calling or subscripting 'WeekDay' with 'unittest.mock.ANY' raises
    'KeeResolveError', as any identifier matching no member does, rather
    than handing the object back as if it were a member.
    """
    with self.assertRaises(KeeResolveError):
      WeekDay(ANY)
    with self.assertRaises(KeeResolveError):
      _ = WeekDay[ANY]

  def test_cast_and_box_resolve_value(self) -> None:
    """
    'typeCast' and an 'AttriBox' over 'ColorNum' both ask 'isinstance'
    first. Once that answers without asking 'RGB', an 'RGB' value goes on
    to the constructor of the enumeration, which resolves it to the member
    holding it.
    """
    self.assertIs(typeCast(ColorNum, RGB(0, 255, 0)), ColorNum.GREEN)

    class Pen(BaseObject):
      color = AttriBox[ColorNum](ColorNum.RED)

    pen = Pen()
    pen.color = RGB(0, 0, 255)
    self.assertIs(pen.color, ColorNum.BLUE)

  def test_members(self) -> None:
    """
    Every member is an instance of its enumeration and is in it, and
    calling or subscripting the enumeration with the member returns the
    member itself.
    """
    for num in (ColorNum, WeekDay):
      for member in num:
        with self.subTest(member=str(member)):
          self.assertIsInstance(member, num)
          self.assertIn(member, num)
          self.assertIs(num(member), member)
          self.assertIs(num[member], member)

  def test_derived_enumeration(self) -> None:
    """
    'MoreRGB' derives from 'RootRGB' and shares its members, so every
    member of 'RootRGB' is a member of 'MoreRGB' as well. A member that
    'MoreRGB' adds counts as a member of 'RootRGB' too, and resolves to
    itself there.
    """
    self.assertIs(MoreRGB.RED, RootRGB.RED)
    self.assertIsInstance(RootRGB.RED, MoreRGB)
    self.assertIn(RootRGB.RED, MoreRGB)
    self.assertIsInstance(MoreRGB.CYAN, RootRGB)
    self.assertIn(MoreRGB.CYAN, RootRGB)
    self.assertIs(RootRGB(MoreRGB.CYAN), MoreRGB.CYAN)

  def test_foreign_member_and_value(self) -> None:
    """
    A member of an unrelated enumeration is not a member, and neither is
    the value of a member, which resolves to that member instead.
    """
    self.assertNotIsInstance(WeekDay.MONDAY, ColorNum)
    self.assertNotIn(WeekDay.MONDAY, ColorNum)
    self.assertNotIsInstance(WeekDay.MONDAY.value, WeekDay)
    self.assertIs(WeekDay(WeekDay.MONDAY.value), WeekDay.MONDAY)

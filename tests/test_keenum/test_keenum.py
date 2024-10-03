"""TestKeeNum tests the KeeNum class"""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Iterable, TYPE_CHECKING
from unittest import TestCase

from worktoy.text import stringList
from worktoy.desc import AttriBox
from worktoy.keenum import KeeNum, auto
from worktoy.base import BaseObject

try:
  from typing import Self
except ImportError:
  Self = object


class WeekDay(KeeNum):
  """Weekday enumeration"""
  MONDAY = auto()
  TUESDAY = auto()
  WEDNESDAY = auto()
  THURSDAY = auto()
  FRIDAY = auto()
  SATURDAY = auto()
  SUNDAY = auto()

  @classmethod
  def __class_call__(cls, *args, **kwargs) -> Self:
    """Returns the class item"""
    for arg in args:
      if isinstance(arg, str):
        return getattr(cls, arg)
      if isinstance(arg, int):
        for item in cls:
          if int(item) == arg:
            return item


class Ugedag(KeeNum):
  """Weekday enumeration, but with the public value in Danish."""
  MONDAY = auto('MANDAG')
  TUESDAY = auto('TIRSDAG')
  WEDNESDAY = auto('ONSDAG')
  THURSDAY = auto('TORSDAG')
  FRIDAY = auto('FREDAG')
  SATURDAY = auto('LORDAG')
  SUNDAY = auto('SONDAG')

  def __str__(self) -> str:
    """String representation of the Ugedag class"""
    clsName = self.__class__.__name__
    return """%s.%s('%s')""" % (clsName, self.name, str(self.value))


class Day(BaseObject):
  """Day owns a boxed WeekDay"""

  weekday = AttriBox[WeekDay](WeekDay.FRIDAY)


class TestKeeNum(TestCase):
  """TestKeeNum tests the KeeNum class"""

  def setUp(self) -> None:
    """Sets up each test"""
    self.day = Day()

  def test_setter(self, ) -> None:
    """Testing if the weekday AttriBox can manage a flexible '__set__'
    call."""
    self.assertIsInstance(self.day.weekday, WeekDay)
    self.day.weekday = 'TUESDAY'
    self.assertEqual(self.day.weekday, WeekDay.TUESDAY)
    self.day.weekday = 4
    self.assertIsInstance(self.day.weekday, WeekDay)
    self.assertEqual(self.day.weekday, WeekDay.FRIDAY)

  def test_iteration(self) -> None:
    """Tests if the KeeNum subclasses implement iteration"""
    if TYPE_CHECKING:
      self.assertIsInstance(WeekDay, Iterable)
      self.assertIsInstance(Ugedag, Iterable)

    for (i, weekday) in enumerate(WeekDay):
      self.assertEqual(weekday - i, 0)
      self.assertEqual(weekday.value, weekday.name)

  def test_value(self) -> None:
    """Tests if Ugedag correctly has the value attribute set to the Danish
    word for each weekday, rather than the English word."""
    dage = stringList(
        """MANDAG, TIRSDAG, ONSDAG, TORSDAG, FREDAG, LORDAG, SONDAG""")
    for (ugedag, weekday, dag) in zip(Ugedag, WeekDay, dage):
      self.assertEqual(ugedag.name, weekday.value)
      self.assertEqual(ugedag.value.lower(), dag.lower())

  def test_dict_key(self) -> None:
    """Tests if the KeeNum subclasses can be used as dictionary keys"""
    testDict = {weekDay: weekDay.name for weekDay in WeekDay}
    for (weekDay, name) in testDict.items():
      self.assertEqual(weekDay.name, name)

  def test_class_membership(self) -> None:
    """Tests if the KeeNum subclass instances correctly identifies
    themselves as members of the class"""
    for weekDay in WeekDay:
      self.assertIsInstance(weekDay, WeekDay)

  def test_class_instance(self) -> None:
    """Tests if objects returned by the KeeNum class object are correctly
    identified as instances of the class. """
    for weekDay in WeekDay:
      name = weekDay.name
      self.assertIsInstance(WeekDay(name), WeekDay)
      item = getattr(WeekDay, name)
      self.assertIsInstance(item, WeekDay)

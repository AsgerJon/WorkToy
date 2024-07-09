"""TestKeeNum tests the KeeNum class"""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Iterable, TYPE_CHECKING

from worktoy.keenum import KeeNum, auto
from worktoy.text import stringList
from worktoy.worktest import WorkTest


class WeekDay(KeeNum):
  """Weekday enumeration"""
  MONDAY = auto()
  TUESDAY = auto()
  WEDNESDAY = auto()
  THURSDAY = auto()
  FRIDAY = auto()
  SATURDAY = auto()
  SUNDAY = auto()


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


class TestKeeNum(WorkTest):
  """TestKeeNum tests the KeeNum class"""

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

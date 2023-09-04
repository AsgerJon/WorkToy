"""WorkToy - SYM - Date
Class representing dates"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from icecream import ic

from worktoy.fields import IntField, SymField
from worktoy.sym import Month, Weekday


class Day(int):
  """Subclass of int"""

  value = IntField(0)

  def __init__(self, defVal: int = None) -> None:
    self._value = 0 if defVal is None else defVal

  def __rshift__(self, other) -> bool:
    if isinstance(other, int):
      return False if self % other else True
    if isinstance(other, Day):
      return self >> other.value
    return NotImplemented

  def __add__(self, other) -> Day:
    if isinstance(other, int):
      return Day(self.value + other)
    if isinstance(other, Day):
      return self + other.value
    return NotImplemented

  def __radd__(self, other: int) -> Day:
    return other + self.value

  def __sub__(self, other: int) -> Day:
    if isinstance(other, int):
      return Day(self.value - other)
    if isinstance(other, Day):
      return self - other.value
    return NotImplemented

  def __rsub__(self, other: int) -> Day:
    return other - self.value

  def __str__(self, ) -> str:
    return 'Day: %d' % self._value

  def __repr__(self, ) -> str:
    return 'Day(%d)' % self._value


class Year(Day):
  """Semantic diff only"""

  def __str__(self, ) -> str:
    return 'Year: %d' % self._value

  def __repr__(self, ) -> str:
    return 'Year(%d)' % self._value


class Date:
  """WorkToy - SYM - Date
  Class representing dates"""

  yearZero = Year(2000)
  month = SymField(Month)
  weekday = SymField(Weekday)
  monthDay = IntField(0)
  absoluteDay = IntField(0)

  @classmethod
  def getYearLength(cls, Y: Year) -> Day:
    """Length of year."""
    return Day(365 - Y >> 4 + Y >> 100 - Y >> 400)

  @classmethod
  def getYear(cls, day: Day) -> Day:
    """Getter-function for the year."""
    year = cls.yearZero
    if (cls.getYearLength(year)) ** 2 > day ** 2:
      return Year(0)

  def getWeekday(self) -> Any:
    """Getter-function for the weekday."""

  def getMonth(self) -> Any:
    """Getter-function for the month"""

  def getMonthDay(self) -> int:
    """Getter-function for the day of the month"""

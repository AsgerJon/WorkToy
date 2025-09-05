"""
Dato encapsulates dates.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from datetime import date, timedelta
from typing import TYPE_CHECKING

from worktoy.mcls import BaseObject
from worktoy.desc import Field
from . import Month, WeekDay

if TYPE_CHECKING:  # pragma: no cover
  from typing import Self


class Dato(BaseObject):
  """
  Weekdays and months are painful to implement.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables

  #  Fallback Variables

  #  Private Variables
  __date_object__ = None
  __private_year__ = None
  __private_month__ = None
  __private_day__ = None

  #  Public Variables

  #  Virtual Variables
  datetimeDate = Field()
  year = Field()
  month = Field()
  day = Field()
  weekDay = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @datetimeDate.GET
  def _getDateObject(self) -> date:
    return self.__date_object__

  @year.GET
  def _getYear(self) -> int:
    return self.datetimeDate.year

  @month.GET
  def _getMonth(self) -> Month:
    return Month(self.datetimeDate.month - 1)

  @day.GET
  def _getDay(self) -> int:
    return self.datetimeDate.day

  @weekDay.GET
  def _getWeekDay(self) -> WeekDay:
    return WeekDay[self.datetimeDate.weekday()]

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __str__(self, ) -> str:
    infoSpec = """%s d. %d. %s, %d"""
    wd = self.weekDay.value
    m = self.month.value
    d = self.day
    y = self.year
    info = infoSpec % (wd, d, m, y)
    return info

  def __repr__(self, ) -> str:
    infoSpec = """%s(%d, %s, %d)"""
    clsName = type(self).__name__
    y = self.year
    m = str(self.month)
    d = self.day
    info = infoSpec % (clsName, y, m, d)
    return info

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __new__(cls, *args, **kwargs) -> Self:
    self = object.__new__(cls)
    if isinstance((args or [None])[0], date):
      self.__date_object__ = args[0]
    else:
      self.__date_object__ = date(*args, **kwargs)
    return self

  @classmethod
  def rightNow(cls, ) -> Self:
    """Returns a 'Dato' object representing today's date."""
    return cls(date.today())

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def tomorrow(self) -> Self:
    """
    Returns the 'Dato' object one day after this one.
    """
    return type(self)(self.datetimeDate + timedelta(days=1))

  def yesterday(self) -> Self:
    """
    Returns the 'Dato' object one day before this one.
    """
    return type(self)(self.datetimeDate - timedelta(days=1))

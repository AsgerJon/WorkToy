"""
The NumLoad provides a class that uses KeeNum classes in the overloads.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import Field
from worktoy.dispatch import Dispatcher, overload
from worktoy.mcls import BaseObject

from . import FlagRoll, WeekNum
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class NumLoad(BaseObject):
  """
  NumLoad provides a class that uses KeeNum classes in the overloads.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __loaded_object__ = None

  #  Public Variables
  loaded = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @loaded.GET
  def _getLoaded(self, ) -> str:
    """
    Get the loaded object.
    """
    return self.__loaded_object__

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @loaded.SET
  def _setLoaded(self, value: Any) -> None:
    """
    Set the loaded object.
    """
    self.__loaded_object__ = str(value)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(FlagRoll)
  def __init__(self, flag: FlagRoll) -> None:
    """Initialize the NumLoad with a FlagRoll instance."""
    self.loaded = flag

  @overload(str)
  def __init__(self, flag: str) -> None:
    """Initialize the NumLoad with a string representation of a FlagRoll."""
    self.loaded = flag

  @overload(WeekNum)
  def __init__(self, week: WeekNum) -> None:
    """Initialize the NumLoad with a WeekNum instance."""
    self.loaded = week

  @overload(WeekNum, FlagRoll)
  @overload(FlagRoll, WeekNum)
  def __init__(self, *args) -> None:
    """Initialize the NumLoad with both a FlagRoll and a WeekNum."""
    self.loaded = str(args)

  @overload(FlagRoll, str)
  def __init__(self, *args) -> None:
    """Initialize the NumLoad with a FlagRoll and a string."""
    self.loaded = str(args)

  @overload(WeekNum, str)
  def __init__(self, *args) -> None:
    """Initialize the NumLoad with a WeekNum and a string."""
    self.loaded = str(args)

  @overload(str, WeekNum)
  @overload(str, FlagRoll)
  @overload(FlagRoll, WeekNum, str)
  @overload(WeekNum, FlagRoll, str)
  @overload(str, FlagRoll, WeekNum)
  @overload(str, WeekNum, FlagRoll)
  def __init__(self, *args) -> None:
    """Initialize the NumLoad with a FlagRoll, a WeekNum, and a string."""
    self.loaded = str(args)

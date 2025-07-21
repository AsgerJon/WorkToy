"""
DescNumLoad provides a descriptor based implementation of the same
scenario as the 'NumLoad' class.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.desc import Field
from worktoy.dispatch import Dispatcher
from . import FlagRoll, WeekNum

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class DescNumLoad:
  """
  DescNumLoad provides a descriptor based implementation of the same
  scenario as the 'NumLoad' class.
  """

  #  Private Variables
  __loaded_object__ = None

  #  Public Variables
  loaded = Field()

  #  Overload Functions
  __init__ = Dispatcher()

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

  @__init__.overload(FlagRoll)
  def __init__(self, flag: FlagRoll) -> None:
    """Initialize the NumLoad with a FlagRoll instance."""
    self.loaded = flag

  @__init__.overload(str)
  def __init__(self, flag: str) -> None:
    """Initialize the NumLoad with a string representation of a FlagRoll."""
    self.loaded = flag

  @__init__.overload(WeekNum)
  def __init__(self, week: WeekNum) -> None:
    """Initialize the NumLoad with a WeekNum instance."""
    self.loaded = week

  @__init__.overload(WeekNum, FlagRoll)
  @__init__.overload(FlagRoll, WeekNum)
  def __init__(self, *args) -> None:
    """Initialize the NumLoad with both a FlagRoll and a WeekNum."""
    self.loaded = str(args)

  @__init__.overload(FlagRoll, str)
  def __init__(self, *args) -> None:
    """Initialize the NumLoad with a FlagRoll and a string."""
    self.loaded = str(args)

  @__init__.overload(WeekNum, str)
  def __init__(self, *args) -> None:
    """Initialize the NumLoad with a WeekNum and a string."""
    self.loaded = str(args)

  @__init__.overload(str, WeekNum)
  @__init__.overload(str, FlagRoll)
  @__init__.overload(FlagRoll, WeekNum, str)
  @__init__.overload(WeekNum, FlagRoll, str)
  @__init__.overload(str, FlagRoll, WeekNum)
  @__init__.overload(str, WeekNum, FlagRoll)
  def __init__(self, *args) -> None:
    """Initialize the NumLoad with a FlagRoll, a WeekNum, and a string."""
    self.loaded = str(args)

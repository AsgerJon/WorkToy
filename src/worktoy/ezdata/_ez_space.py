"""EZSpace provides the namespace for the EZData class. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from icecream import ic

from . import EZSpaceHook, EZSlot
from ..mcls import BaseSpace
from ..utilities import maybe

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Optional, Self

ic.configureOutput(includeContext=True)


class EZSpace(BaseSpace):
  """
  EZSpace provides the namespace for the EZData class.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __ez_slots__ = None

  #  Public Variables
  ezHook = EZSpaceHook()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def getEZSlots(self) -> list[EZSlot]:
    """Get the data fields."""
    return maybe(self.__ez_slots__, [])

  def getDeepEZSlots(self) -> list[EZSlot]:
    """Get the data fields, including those from the EZHook."""

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def addSlot(self, ezSlot: EZSlot) -> None:
    """Adds the EZSlot to the data fields. """
    existing = self.getEZSlots()
    ezSlot.__owner_name__ = self.getClassName()
    self.__ez_slots__ = [*existing, ezSlot]

  def addRegularSlot(self, key: str, val: object) -> None:
    """Add a key-value pair to the data fields. Called by the EZHook from
    inside the '__setitem__'. """
    ezSlot = EZSlot(key, )
    ezSlot.__type_value__ = type(val)
    ezSlot.__default_value__ = val
    self.addSlot(ezSlot)

  def addTypeOnlySlot(self, key: str, type_: type) -> None:
    """Add a key-value pair to the data fields with a specific type. Called
    by the EZHook from inside the '__setitem__'. """
    ezSlot = EZSlot(key, )
    ezSlot.__type_value__ = type_
    ezSlot.__default_value__ = type_()
    existing = self.getEZSlots()
    self.__ez_slots__ = [*existing, ezSlot]
    self.addSlot(ezSlot)

  def addTypeDeferredSlot(self, key: str, deferredType: str) -> None:
    """Add a deferred field to the data fields. Called by the EZHook from
    inside the '__setitem__'. """
    ezSlot = EZSlot(key)
    ezSlot.__deferred_type__ = deferredType
    self.addSlot(ezSlot)

"""
SubDescNumLoad extends the scenario of DescNumLoad and NumLoad to cover
the case of a descriptor-based overload implementation being subclassed.
Specifically, such that the subclass extends the supported type signatures.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import Field
from . import DescNumLoad, FlagRoll

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class SubDescNumLoad(DescNumLoad):
  """
  SubDescNumLoad extends the scenario of DescNumLoad and NumLoad to cover
  the case of a descriptor-based overload implementation being subclassed.
  Specifically, such that the subclass extends the supported type signatures.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables

  #  Fallback Variables

  #  Private Variables
  __sub_loaded_object__ = None

  #  Public Variables
  subLoaded = Field()

  #  Overload Functions
  __init__ = DescNumLoad.__init__.clone()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @subLoaded.GET
  def _getSubLoaded(self) -> str:
    return str(self.__sub_loaded_object__)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @subLoaded.SET
  def _setSubLoaded(self, value: Any) -> None:
    self.__sub_loaded_object__ = str(value)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @__init__.overload(FlagRoll, FlagRoll, FlagRoll)
  def __init__(self, *args) -> None:
    self.loaded = str(args)
    self.subLoaded = str(args)

  @__init__.fallback
  def __init__(self, *args) -> None:
    self.loaded = str(args)
    self.subLoaded = str(args)

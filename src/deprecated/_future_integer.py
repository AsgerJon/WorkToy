"""FutureInteger provides a class that the 'FutureNotation' class annotate
to by name only. The class merely wraps 'int'. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.core import Object
from worktoy.utilities import maybe

if TYPE_CHECKING:  # pragma: no cover
  from typing import Self, Any


class FutureInteger(Object):
  """
  FutureInteger provides a class that the 'FutureNotation' class annotate
  to by name only. The class merely wraps 'int'.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Fallback Variables
  __fallback_value__ = 0

  #  Private Variables
  __inner_value__ = None

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _getInnerValue(self) -> int:
    """Get the inner value of the FutureInteger."""
    return maybe(self.__inner_value__, self.__fallback_value__)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _setInnerValue(self, value: int) -> None:
    """Set the inner value of the FutureInteger."""
    self.__inner_value__ = int(value)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __getattr__(self, name: str, ) -> Any:
    """Falls back to the int class"""
    func = object.__getattribute__(int, name)
    if not callable(func):
      return func
    this = self.__getInnerValue()

    def wrapper(*args: Any, **kwargs: Any) -> Any:
      """
      Wraps the int method to call it on the inner value.
      """
      inner_value = self._getInnerValue()
      return func(this, *args, **kwargs)

    return wrapper

  def __str__(self, ) -> str:
    """
    Returns the string representation of the FutureInteger.
    """
    return str(self._getInnerValue())

  __repr__ = __str__

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, value: int = 0) -> None:
    """
    Initialize the FutureInteger with an integer value.
    If no value is provided, it defaults to 0.
    """
    self.__inner_value__ = int(value)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

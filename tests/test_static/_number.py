"""
Number provides a single numeric value descriptor.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from random import random
from math import atan2

from worktoy.parse import maybe
from worktoy.waitaminute import DispatchException

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

from worktoy.mcls import BaseMeta
from worktoy.static import overload
from worktoy.static.zeroton import THIS

if TYPE_CHECKING:
  from typing import Any, Self


class Number:
  """
  Number provides a single numeric value descriptor.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Fallback variables
  __fallback_value__ = 0

  #  Private variables
  __field_name__ = None
  __field_owner__ = None
  __default_value__ = None

  #  Public variables

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def getPrivateName(self, ) -> str:
    """Getter-function for the private name."""
    return '__pvt_%s' % self.__field_name__

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, *args) -> None:
    """Initialize the Number object."""
    for arg in args:
      if isinstance(arg, (int, float, complex)):
        self.__default_value__ = arg
        break

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __set_name__(self, owner: type, name: str) -> None:
    """Set the name of the field and the owner of the field."""
    self.__field_name__ = name
    self.__field_owner__ = owner

  def __get__(self, instance: object, owner: type) -> Any:
    """Get the value of the field."""
    if instance is None:
      return self
    pvtName = self.getPrivateName()
    defVal = maybe(self.__default_value__, self.__fallback_value__)
    return getattr(instance, pvtName, defVal)

  def __set__(self, instance: object, value: Any) -> None:
    """Set the value of the field."""
    if instance is None:
      raise TypeError('Cannot set attribute on class')
    pvtName = self.getPrivateName()
    setattr(instance, pvtName, value)

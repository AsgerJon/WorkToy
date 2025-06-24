"""_Attribute provides a primitive descriptor protocol implementation. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

import re

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:  # pragma: no cover
  pass


class _Attribute:
  """
  _Attribute provides a primitive descriptor protocol implementation.
  This is a base class for all attributes. It provides the basic
  functionality
  for getting and setting values, as well as the ability to define custom
  behavior for getting and setting values.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __field_name__ = None
  __field_owner__ = None
  __default_value__ = None

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _getPrivateName(self) -> str:
    """Get the private name of the attribute."""
    pattern = re.compile(r'(?<!^)(?=[A-Z])')
    return '__%s__' % pattern.sub('_', self.__field_name__).lower()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __set_name__(self, owner: type, name: str) -> None:
    """Set the name of the attribute."""
    self.__field_name__ = name
    self.__field_owner__ = owner

  def __get__(self, instance: object, owner: type) -> object:
    """Get the value of the attribute."""
    if instance is None:
      return self
    privateName = self._getPrivateName()
    return getattr(instance, privateName, self.__default_value__)

  def __set__(self, instance: object, value: object) -> None:
    """Set the value of the attribute."""
    privateName = self._getPrivateName()
    setattr(instance, privateName, value)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, defVal: Any = None) -> None:
    self.__default_value__ = defVal

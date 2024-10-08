"""InfoField provides a primitive implementation of the descriptor
protocol used by the rest of the 'worktoy.info' package. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.text import monoSpace
from typing import Any

try:
  from typing import Callable
except ImportError:
  Callable = object


class InfoField:
  """Descriptor for the info"""

  __field_name__ = None
  __field_owner__ = None
  __pvt_name__ = None
  __default_value__ = None

  def _getPrivateName(self) -> str:
    """Getter-function for the private name"""
    if self.__pvt_name__ is None:
      e = """The field name is not set!"""
      raise ValueError(monoSpace(e))
    return self.__pvt_name__

  def _getDefaultValue(self) -> str:
    """Getter-function for the default value!"""
    if self.__default_value__ is None:
      e = """The default value is not set!"""
      raise ValueError(monoSpace(e))
    return self.__default_value__

  def __set_name__(self, owner: type, name: str) -> None:
    """Set the name of the field and the owner of the field."""
    self.__field_name__ = name
    self.__field_owner__ = owner
    if self.__pvt_name__ is None:
      self.__pvt_name__ = '_%s' % self.__field_name__

  def __init__(self, *args, **kwargs) -> None:
    """The '__init__' method initializes the descriptor."""
    posArgs = [*args, None, None][:2]
    self.__default_value__, self.__pvt_name__ = posArgs

  def __get__(self, instance: object, owner: type, **kwargs) -> Any:
    """Getter-function"""
    if instance is None:
      return self
    pvtName = self._getPrivateName()
    value = getattr(instance, pvtName, None)
    if value is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self.__set__(instance, self._getDefaultValue())
      return self.__get__(instance, owner, _recursion=True)
    return value

  def __set__(self, instance: object, value: object) -> None:
    """Setter-function"""
    setattr(instance, self._getPrivateName(), value)

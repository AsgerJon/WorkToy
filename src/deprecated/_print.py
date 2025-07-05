"""
Print provides a write-once descriptor implementation. This allows owning
classes to provide immutable instances, once these descriptor object
values are set. Please note that the '__get__' method will raise
'AccessError' if accessed before a value is set.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from ..core import Object
from . import AttriBox

from typing import TYPE_CHECKING

from ..core.sentinels import DELETED
from ..waitaminute import WriteOnceError

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Callable, TypeVar, Generic, Optional


class Print(AttriBox):
  """
  Print provides a write-once descriptor implementation. This allows owning
  classes to provide immutable instances, once these descriptor object
  values are set. Please note that the '__get__' method will raise
  'AccessError' if accessed before a value is set.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __instance_set__(self, value: Any, *args, **kwargs) -> None:
    """
    Sets the value of the descriptor. This method can only be called once.
    """
    pvtName = self.getPrivateName()
    instance = self.getContextInstance()
    fieldType = self.getFieldType()
    try:
      existing = getattr(instance, pvtName)
    except AttributeError as attributeError:
      if isinstance(value, fieldType):
        return setattr(instance, pvtName, value)
      if kwargs.get('_recursion', False):
        raise RecursionError from attributeError
      try:
        value = fieldType(value)
      except (ValueError, TypeError) as error:
        raise error from attributeError
      else:
        return self.__instance_set__(value, *args, _recursion=True)
    if existing is not None:
      raise WriteOnceError(self, existing, value)
    if kwargs.get('_recursion2', False):
      raise RecursionError
    setattr(instance, pvtName, DELETED)
    return self.__instance_set__(value, *args, _recursion2=True)

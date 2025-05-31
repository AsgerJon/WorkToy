"""
TypedAttr subclasses Attr adding strong types.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from ..parse import maybe
from ..waitaminute import MissingVariable, TypeException
from . import Attr

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, Self


class TypedAttr(Attr):
  """Creates a deferred function that is called when the __get__ is first
  called. """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Fallback variables
  __abstract_type__ = object

  #  Private variables
  __field_type__ = None

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _getFieldType(self, **kwargs) -> type:
    """
    Getter-function for the field type.
    """
    return maybe(self.__field_type__, self.__abstract_type__, )

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _setFieldType(self, fieldType: type) -> Self:
    """
    Setter-function for the field type.
    """
    if self.__field_type__ is not None:
      raise MissingVariable('__field_type__', type)
    if not isinstance(fieldType, type):
      name, value = '__field_type__', fieldType
      raise TypeException(name, value, type)
    self.__field_type__ = fieldType
    return self

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, *args, ) -> None:
    name, type_ = None, None
    for arg in args:
      if isinstance(arg, str) and name is None:
        name = arg
        continue
      elif isinstance(arg, type) and type_ is None:
        type_ = arg
        continue
      if all([i is not None for i in (name, type_)]):
        break
    else:
      if name is None:
        name = self._getPrivateName()
      type_ = maybe(type_, self.__abstract_type__, )
    Attr.__init__(self, name)
    self._setFieldType(type_)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _typeGuard(self, value: Any) -> Any:
    """
    Type guard for the value.
    """
    fieldType = self._getFieldType()
    if not isinstance(value, fieldType):
      name, value = '_typeGuard', value
      raise TypeException(name, value, fieldType)
    return value

  def __instance_get__(self, **kwargs) -> Any:
    """
    Getter-function for the instance.
    """
    return self._typeGuard(super().__instance_get__(**kwargs))

  def __instance_set__(self, value: Any, **kwargs) -> Self:
    """
    Setter-function for the instance.
    """
    return super().__instance_set__(self._typeGuard(value), **kwargs)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

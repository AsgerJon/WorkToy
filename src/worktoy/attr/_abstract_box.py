"""AttriBox provides a descriptor with lazy instantiation of the
underlying object. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
import re

from ..static import THIS
from ..text import typeMsg
from ..waitaminute import VariableNotNone, MissingVariable
from . import AbstractDescriptor

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  pass


class AbstractBox(AbstractDescriptor):
  """AttriBox provides a descriptor with lazy instantiation of the
  underlying object. """

  __field_type__ = None
  __pos_args__ = None
  __key_args__ = None

  def _getFieldType(self) -> type:
    """Get the field type."""
    if self.__field_type__ is None:
      raise MissingVariable('__field_type__', type)
    return self.__field_type__

  def _setFieldType(self, fieldType: type) -> None:
    """Set the field type."""
    if not isinstance(fieldType, type):
      raise VariableNotNone('__field_type__', )
    self.__field_type__ = fieldType

  def _getPosArgs(self, instance: object = None) -> tuple:
    """Get the positional arguments."""
    posArgs = getattr(self, '__pos_args__', None)
    if posArgs is None:
      raise MissingVariable('__pos_args__', tuple)
    if not isinstance(posArgs, tuple):
      e = typeMsg('__pos_args__', posArgs, tuple)
      raise TypeError(e)
    if instance is None:
      return posArgs
    out = []
    for arg in posArgs:
      if arg is THIS:
        out.append(instance)
      else:
        out.append(arg)
    return (*out,)

  def _setPosArgs(self, *args) -> None:
    """Set the positional arguments."""
    self.__pos_args__ = (*args,)

  def _getKeyArgs(self, instance: object = None) -> dict:
    """Get the keyword arguments."""
    keyArgs = getattr(self, '__key_args__', None)
    if keyArgs is None:
      raise MissingVariable('__key_args__', dict)
    if not isinstance(keyArgs, dict):
      e = typeMsg('__key_args__', keyArgs, dict)
      raise TypeError(e)
    if instance is None:
      return keyArgs
    out = {}
    for key, value in keyArgs.items():
      if value is THIS:
        out[key] = instance
      else:
        out[key] = value
    return out

  def _setKeyArgs(self, **kwargs) -> None:
    """Set the keyword arguments."""
    self.__key_args__ = {**kwargs, }

  def getPrivateName(self, ) -> str:
    """Getter-function for the private name of the field."""
    fieldName = self.getFieldName()
    pattern = re.compile(r'(?<!^)(?=[A-Z])')
    return '__%s__' % pattern.sub('_', fieldName).lower()

  @abstractmethod
  def _instanceGet(self, instance: object, **kwargs) -> object:
    """Get the instance of the descriptor."""

  @abstractmethod
  def _instanceSet(self, instance: object, value: object, **kwargs) -> None:
    """Set the instance of the descriptor."""

  @abstractmethod
  def _instanceDelete(self, instance: object, **kwargs) -> None:
    """Delete the instance of the descriptor."""

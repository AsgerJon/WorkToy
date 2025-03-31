"""AbstractDescriptorClass provides the common base class for all other
implementations of the descriptor protocol. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from worktoy.abstract import abstract
from worktoy.text import monoSpace, typeMsg


class AbstractDescriptorClass:
  """AbstractDescriptorClass provides the common base class for all other
  implementations of the descriptor protocol. """

  __field_name__ = None
  __field_owner__ = None

  def getFieldName(self) -> str:
    """Getter-function for the field name."""
    if self.__field_name__ is None:
      e = """Instance of 'AttriBox' does not belong to class. This 
      typically indicates that the owning class is still being created."""
      raise RuntimeError(monoSpace(e))
    if isinstance(self.__field_name__, str):
      return self.__field_name__
    e = typeMsg('__field_name__', self.__field_name__, str)
    raise TypeError(monoSpace(e))

  def getFieldOwner(self) -> type:
    """Getter-function for the field owner."""
    if self.__field_owner__ is None:
      e = """Instance of 'AttriBox' does not belong to class. This 
      typically indicates that the owning class is still being created. """
      raise RuntimeError(monoSpace(e))
    if isinstance(self.__field_owner__, type):
      return self.__field_owner__
    e = typeMsg('__field_owner__', self.__field_owner__, type)
    raise TypeError(monoSpace(e))

  @abstract
  def __instance_get__(self, instance: object) -> Any:
    """Getter-function for the inner object."""

  def __instance_set__(self, instance: object, value: Any) -> None:
    """Setter-function for the inner object."""
    e = """The attribute '%s' is read-only!""" % self.getFieldName()
    raise AttributeError

  def __instance_del__(self, instance: object) -> None:
    """Deleter-function for the inner object."""
    e = """The attribute '%s' is read-only!""" % self.getFieldName()
    raise AttributeError

  def __set_name__(self, owner: type, name: str) -> None:
    """Set the name of the field and the owner of the field."""
    self.__field_name__ = name
    self.__field_owner__ = owner

  def __get__(self, instance: object, owner: type) -> Any:
    if instance is None:
      return self
    return self.__instance_get__(instance)

  def __set__(self, instance: object, value: Any) -> None:
    self.__instance_set__(instance, value)

  def __delete__(self, instance: object) -> None:
    self.__instance_del__(instance)

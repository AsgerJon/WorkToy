"""MissingValueException provides a subclass of Exception that subclasses
of AbstractDescriptor should raise to indicate a missing value. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, Any
from worktoy.text import monoSpace, typeMsg

if TYPE_CHECKING:
  from worktoy.desc import AbstractDescriptor


class MissingValueException(Exception):
  """MissingValueException provides a subclass of Exception that subclasses
  of AbstractDescriptor should raise to indicate a missing value. """

  __instance_object__ = None
  __descriptor_object__ = None

  def __init__(self,
               instance: object,
               descriptor: AbstractDescriptor) -> None:
    owner = descriptor.getFieldOwner()
    fieldName = descriptor.getFieldName()
    descType = type(descriptor).__name__
    msg = """The field '%s' of owning class '%s' managed by descriptor of 
    type '%s' received a call to '__get__' but no value
    was found!""" % (fieldName, owner.__name__, descType,)
    Exception.__init__(self, monoSpace(msg))

  def getInstanceObject(self, ) -> object:
    """Getter-function for the instance object. """
    return self.__instance_object__

  def getDescriptorObject(self, ) -> AbstractDescriptor:
    """Getter-function for the descriptor object. """
    if self.__descriptor_object__ is None:
      e = """The descriptor object has not been assigned!"""
      raise AttributeError(e)
    if isinstance(self.__descriptor_object__, AbstractDescriptor):
      return self.__descriptor_object__
    e = typeMsg('descriptorObject', self.__descriptor_object__,
                AbstractDescriptor)
    raise TypeError(e)

  def _setInstanceObject(self, instance: object) -> None:
    """Setter-function for the instance object. """
    self.__instance_object__ = instance

  def _setDescriptorObject(self, descriptor: AbstractDescriptor) -> None:
    """Setter-function for the descriptor object. """
    self.__descriptor_object__ = descriptor

  def __eq__(self, other: Any) -> bool:
    """The equality operator compares against a tuple to confirm that the
    exception involved the same instance and descriptor. """
    if self is other:
      return True
    if not isinstance(other, tuple):
      return NotImplemented
    if self.getInstanceObject() not in other:
      return False
    if self.getDescriptorObject() not in other:
      return False
    return True

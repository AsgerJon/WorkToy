"""CurrentDescriptor provides a baseclass for descriptor classes that keep
track of the currently active descriptor. It returns a copy of itself for
each instance of the descriptor class and each subclass of the baseclass
that first introduced the descriptor. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

import os
from abc import abstractmethod

from ..attr import WaitForIt, Field
from ..mcls import BaseObject
from ..parse import maybe
from ..static import overload, THIS, OWNER, ATTR
from ..text import stringList
from ..waitaminute import TypeException, MissingVariable, ReadOnlyError, \
  ProtectedError
from ..work_io import validateExistingDirectory

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, Optional, Self


class CurrentDescriptor(BaseObject):
  """
  CurrentDescriptor provides a baseclass for descriptor classes that keep
  track of the currently active descriptor. It returns a copy of itself for
  each instance of the descriptor class and each subclass of the baseclass
  that first introduced the descriptor.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  __pos_args__ = None
  __key_args__ = None

  __field_name__ = None
  __field_owner__ = None

  __current_owner__ = None
  __current_instance__ = None

  __owner_registry__ = None

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _getFieldName(self) -> str:
    """Get the field name."""
    if self.__field_name__ is None:
      raise MissingVariable('__field_name__', str)
    return self.__field_name__

  def _getFieldOwner(self) -> type:
    """Get the field owner."""
    if self.__field_owner__ is None:
      raise MissingVariable('__field_owner__', type)
    return self.__field_owner__

  def _getCurrentOwner(self) -> type:
    """Get the current owner."""
    if self.__current_owner__ is None:
      if self.__field_owner__ is None:
        raise MissingVariable('__current_owner__', type)
      return self.__field_owner__  # The original instance has only the owner
    return self.__current_owner__

  def _getCurrentInstance(self) -> Any:
    """Get the current instance, which may be None"""
    return self.__current_instance__

  def _getOwningObject(self, ) -> Any:
    """Get the owning object."""
    if self.__current_instance__ is None:
      if self.__current_owner__ is None:
        if self.__field_owner__ is None:
          raise MissingVariable('__field_owner__', type)
        return self.__field_owner__
      return self.__current_owner__
    return self.__current_instance__

  def _getOwnerRegistry(self, ) -> dict:
    """Get the owner registry."""
    return maybe(self.__owner_registry__, dict())

  def _getPositionalArgs(self) -> tuple:
    """Get the positional arguments."""
    if self.__pos_args__ is None:
      return ()
    if isinstance(self.__pos_args__, (tuple, list)):
      instance = maybe(self._getCurrentInstance(), THIS)
      owner = maybe(self._getCurrentOwner(), OWNER)
      posArgs = []
      for arg in self.__pos_args__:
        if arg is THIS:
          posArgs.append(instance)
        elif arg is OWNER:
          posArgs.append(owner)
        elif arg is ATTR:
          posArgs.append(self)
        else:
          posArgs.append(arg)
      return (*posArgs,)
    raise TypeException('__pos_args__', self.__pos_args__, (tuple, list))

  def _getKeywordArgs(self) -> dict:
    """Get the keyword arguments."""
    if self.__key_args__ is None:
      return {}
    if isinstance(self.__key_args__, dict):
      instance = maybe(self._getCurrentInstance(), THIS)
      owner = maybe(self._getCurrentOwner(), OWNER)
      keyArgs = {}
      for (key, val) in self.__key_args__.items():
        raise NotImplementedError

      return {**self.__key_args__, }
    raise TypeException('__key_args__', self.__key_args__, dict)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _setCurrentOwner(self, owner: type) -> None:
    """Set the current owner."""
    if not isinstance(owner, type):
      raise TypeException('__current_owner__', owner, type)
    if owner in [self.__field_owner__, self.__current_owner__]:
      return
    self.__current_owner__ = owner

  def _setCurrentInstance(self, instance: Any) -> None:
    """Set the current instance."""
    if instance is self.__current_instance__:
      return
    self.__current_instance__ = instance

  def _registerSelf(self, ) -> None:
    """Register the current descriptor"""
    existing = self._getOwnerRegistry()
    owningObject = self._getOwningObject()
    if owningObject in existing:
      if existing[owningObject] is self:
        return
      raise RuntimeError
    existing[owningObject] = self
    self.__owner_registry__ = existing

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __set_name__(self, owner: type, name: str) -> None:
    """Set the name of the field and the owner of the field."""
    self.__field_name__ = name
    self.__field_owner__ = owner
    existing = self._getOwnerRegistry()
    existing[owner] = self
    self.__owner_registry__ = existing

  def __get__(self, instance: Any, owner: type, **kwargs) -> Any:
    """Get the value of the field."""
    registry = self._getOwnerRegistry()
    owningObject = maybe(instance, owner, self._getFieldOwner())
    if owningObject in registry:
      self_ = registry[owningObject]
      if instance is None:
        return self_
    if kwargs.get('_recursion', False):
      raise RecursionError
    cls = type(self)
    args2 = self._getPositionalArgs()
    kwargs2 = self._getKeywordArgs()
    self_ = cls(*args2, **kwargs2)
    self_.__field_name__ = self.__field_name__
    self_.__field_owner__ = self.__field_owner__
    self_._setCurrentOwner(owner)
    self_._setCurrentInstance(instance)
    return cls.__get__(self_, instance, owner, _recursion=True)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, *args, **kwargs) -> None:
    """Subclasses may reimplement this method, but it is critically
    important that the parent method is called first! """
    self.__pos_args__ = (*args,)
    self.__key_args__ = {**kwargs, }

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __instance_get__(self, ) -> Any:
    """Subclasses may implement this method to specify the object to be
    returned from __get__. Since this method accepts only the self-argument,
    it should use the current instance and owner as appropriate to
    determine the return-object. By default, this method returns 'self'. """
    return self

  def __instance_set__(self, value: Any) -> None:
    """Subclasses may implement this method to enable setting of the
    descriptor. By default, this method raises 'ReadOnlyError'. """
    try:
      oldValue = self.__instance_get__()
    except Exception as exception:
      oldValue = exception
    instance = self._getCurrentInstance()
    raise ReadOnlyError(instance, self, oldValue, value)

  def __instance_delete__(self, ) -> None:
    """Subclasses may implement this method to enable deletion of the
    descriptor. By default, this method raises 'ProtectedError'. """
    try:
      oldValue = self.__instance_get__()
    except Exception as exception:
      oldValue = exception
    instance = self._getCurrentInstance()
    raise ProtectedError(instance, self, oldValue)

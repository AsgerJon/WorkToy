"""
CachingHook caches values on the descriptor side in a dictionary using the
memory addresses returned by 'id()' as keys to map specific instances to
dedicated values. This is in contrast the 'WeakBox' and 'StrongBox' which
both caches values as dynamic attributes on the instance side. CachingHook
is more performant as it may be used on classes that implement __slots__.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from . import AbstractDescriptorHook
from ...parse import maybe
from ...waitaminute import MissingVariable, VariableNotNone

#  Below provides compatibility back to Python 3.7
try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any


class _EmptyCache(MissingVariable):
  """
  Local custom exception raised to indicate absence of a cached value.
  Should not propagate outside the hook.
  """
  pass


class _EmptyDefault(MissingVariable):
  """
  Local custom exception raised to indicate absence of a default value.
  Should not propagate outside the hook.
  """
  pass


class CachingHook(AbstractDescriptorHook):
  """
  CachingHook caches the return value returned by '__instance_get__' and on
  the next '__get__' short-circuits the call to '__instance_get__' by
  returning the cached value.

  This is achieved by the following hooks:
  - Pre-get: If the hook has a cached value for the current instance,
  it returns the cached value before the call to '__instance_get__'.
  Please note that this value is set as a dynamic attribute on the instance.

  - Post-get: If the hook did not have a cached value, the value obtained
  from the __instance_get__, or from another hook, is cached for future use.

  - Post-set: Updates the cached value when the attribute is set on the
  instance.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables

  #  Fallback Variables

  #  Private Variables
  __default_value__ = None
  __cached_values__ = None

  #  Public Variables

  #  Virtual Variables

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def getDefaultValue(self) -> Any:
    """
    Returns the default value for the hook.
    """
    if self.__default_value__ is not None:
      return self.__default_value__
    raise MissingVariable('__default_value__', )

  def _getCachedValues(self) -> dict[Any, Any]:
    """
    Getter-function for dictionary mapping memory addresses of instances
    to cached values.
    """
    return maybe(self.__cached_values__, dict())

  def _getCachedValue(self, ) -> Any:
    """
    Returns the cached value for the current instance. If the current
    instance is None, raises 'MissingVariable' exception.
    """
    if self.instance is None:
      raise MissingVariable('instance', )
    values = self._getCachedValues()
    if self.instanceId in values:
      return values[self.instanceId]
    raise _EmptyCache('cachedValue')

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def setDefaultValue(self, value: Any) -> None:
    """
    Setter-function for the default value of the hook.
    """
    if self.__default_value__ is not None:
      raise VariableNotNone('__default_value__', self.__default_value__)
    self.__default_value__ = value

  def _setCachedValue(self, value: Any) -> None:
    """
    Caches the given value for the current instance. If the current
    instance is None, raises 'MissingVariable' exception.
    """
    if self.instance is None:
      raise MissingVariable('instance', )
    existingValues = self._getCachedValues()
    if self.instanceId in existingValues:
      cachedValue = existingValues[self.instanceId]
      if cachedValue is value:
        return  # No need to update if the value is the same
    self.__cached_values__[self.instanceId] = value

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def preGet(self, value: Any = None) -> Any:
    """
    Pre-get hook that checks if the cached value exists for the current
    instance. If it does, returns the cached value, otherwise returns None.
    """
    try:
      cachedValue = self._getCachedValue()
    except _EmptyCache:
      try:
        defaultValue = self.getDefaultValue()
      except _EmptyDefault:
        return value
      else:
        return defaultValue
    else:
      return cachedValue

  def postGet(self, value: Any) -> Any:
    """
    Updates the cached value with the value received.
    """
    self._setCachedValue(value)

  def postSet(self, value: Any, oldValue: Any = None) -> None:
    """
    Updates the cached value with the new value set.
    """
    self._setCachedValue(value)

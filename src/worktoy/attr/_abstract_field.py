"""AbstractField provides an abstract baseclass for descriptor protocol
implementations that delegate the accessor methods to the owner class
itself. It identifies the accessor methods by keys that should point to
the relevant methods on the owner class. This abstract class does not
provide any reasonable way to define those keys, which is left to
subclasses. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.static import maybe
from worktoy.text import typeMsg, monoSpace

from worktoy.attr import AbstractDescriptor
from worktoy.waitaminute.descriptor_exceptions import MissingGetterException

try:
  from typing import Any
except ImportError:
  Any = object

try:
  from typing import TYPE_CHECKING
except ImportError:
  TYPE_CHECKING = False

try:
  from typing import Never
except ImportError:
  try:
    from typing import NoReturn as Never
  except ImportError:
    Never = object

try:
  from typing import Callable
except ImportError:
  Callable = object


class AbstractField(AbstractDescriptor):
  """AbstractField provides an abstract baseclass for descriptor protocol
  implementations that delegate the accessor methods to the owner class
  itself. It identifies the accessor methods by keys that should point to
  the relevant methods on the owner class. """

  #  Accessor method keys
  __getter_key__ = None
  __setter_keys__ = None
  __deleter_keys__ = None

  #  Accessor method keys accessors

  def _getGetterKey(self, ) -> str:
    """This method returns the getter key. """
    if self.__getter_key__ is None:
      e = """The getter key has not been assigned!"""
      raise AttributeError(e)
    if isinstance(self.__getter_key__, str):
      return self.__getter_key__
    e = typeMsg('__getter_key__', self.__getter_key__, str)
    raise TypeError(e)

  def _getSetterKeys(self, ) -> list[str]:
    """This method returns the setter keys. """
    return maybe(self.__setter_keys__, [])

  def _getDeleterKeys(self, ) -> list[str]:
    """This method returns the deleter keys. """
    return maybe(self.__deleter_keys__, [])

  def setGetterKey(self, setterKey: str) -> None:
    """This method sets the getter key. """
    if self.__getter_key__ is not None:
      e = """The getter key has already been assigned!"""
      raise AttributeError(e)
    if not isinstance(setterKey, str):
      e = typeMsg('setterKey', setterKey, str)
      raise TypeError(e)
    self.__getter_key__ = setterKey

  def appendSetterKey(self, setterKey: str) -> None:
    """This method appends a setter key. """
    existing = self._getSetterKeys()
    self.__setter_keys__ = [*existing, setterKey]

  def appendDeleterKey(self, deleterKey: str) -> None:
    """This method appends a deleter key. """
    existing = self._getDeleterKeys()
    self.__deleter_keys__ = [*existing, deleterKey]

  # -----------------------------------------------------------------------
  #  Accessor method accessors

  def _getCurrentGetter(self) -> Callable:
    """Getter-function for the current getter. """
    getterKey = self._getGetterKey()
    currentOwner = self.getCurrentOwner()
    getter = getattr(currentOwner, getterKey, None)
    if callable(getter):
      return getter
    raise MissingGetterException(self)

  def _getCurrentSetters(self) -> list[Callable]:
    """Getter-function for the current setters. """
    currentOwner = self.getCurrentOwner()
    setterKeys = self._getSetterKeys()
    setterFunctions = []
    for setterKey in setterKeys:
      setterFunction = getattr(currentOwner, setterKey, None)
      if setterFunction is None:
        e1 = """Current owner: '%s' does not implement a setter method for 
        field: '%s', expected at name: '%s'!"""
        e2 = e1 % (currentOwner.__name__, self.getFieldName(), setterKey)
        raise AttributeError(monoSpace(e2))
      if not callable(setterFunction):
        e = typeMsg('setterFunction', setterFunction, Callable)
        raise TypeError(e)
      setterFunctions.append(setterFunction)
    return setterFunctions

  def _getCurrentDeleters(self) -> list[Callable]:
    """Getter-function for the current deleters. """
    currentOwner = self.getCurrentOwner()
    deleterKeys = self._getDeleterKeys()
    deleterFunctions = []
    for deleterKey in deleterKeys:
      deleterFunction = getattr(currentOwner, deleterKey, None)
      if deleterFunction is None:
        e1 = """Current owner: '%s' does not implement a deleter method for 
        field: '%s', expected at name: '%s'!"""
        e2 = e1 % (currentOwner.__name__, self.getFieldName(), deleterKey)
        raise AttributeError(monoSpace(e2))
      if not callable(deleterFunction):
        e = typeMsg('deleterFunction', deleterFunction, Callable)
        raise TypeError(e)
      deleterFunctions.append(deleterFunction)
    return deleterFunctions

  # -----------------------------------------------------------------------
  #  Instance specific methods

  def __instance_get__(self, instance: object) -> Any:
    """Getter-function for the inner object."""
    getterFunction = self._getCurrentGetter()
    return getterFunction(instance)

  def __instance_set__(self, instance: object, value: Any) -> None:
    """Setter-function for the inner object."""
    setterFunctions = self._getCurrentSetters()
    for setterFunction in setterFunctions:
      setterFunction(instance, value)

  def __instance_del__(self, instance: object) -> None:
    """Deleter-function for the inner object."""
    deleterFunctions = self._getCurrentDeleters()
    for deleterFunction in deleterFunctions:
      deleterFunction(instance)

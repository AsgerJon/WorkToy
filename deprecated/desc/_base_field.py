"""BaseField subclasses AbstractField implementing handling of inheritance
allowing a subclass to reimplement the accessor methods defined in the
parent class. It should be further subclassed to provide an interface for
setting the accessor method keys. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from depr.desc import AbstractField
from worktoy.static import maybe

try:
  from typing import Callable, Any
except ImportError:
  Callable = object
  Any = object

from worktoy.text import typeMsg, monoSpace


class BaseField(AbstractField):
  """Field provides a flexible implementation of the descriptor
  protocol allowing owning classes to decorate methods as accessor
  methods. """

  __current_owner__ = None
  #  Base accessor methods
  __base_getter__ = None
  __base_setters__ = None
  __base_deleters__ = None
  #  Current accessor methods
  __current_getter__ = None
  __current_setters__ = None
  __current_deleters__ = None

  def _getCurrentOwner(self, **kwargs) -> type:
    """Getter-function for the current owner. """
    if self.__current_owner__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._setCurrentOwner(self.__base_owner__)
      return self._getCurrentOwner(_recursion=True)
    if isinstance(self.__current_owner__, type):
      return self.__current_owner__
    e = typeMsg('__current_owner__', self.__current_owner__, type)
    raise TypeError(e)

  def _setCurrentOwner(self, currentOwner: type) -> None:
    """Setter-function for the current owner. """
    self.__current_owner__ = currentOwner
    self._updateAccessors()

  def _updateAccessors(self, ) -> None:
    """Updates the accessor methods. """
    self._updateGetterFunction()
    self._updateSetterFunctions()
    self._updateDeleterFunctions()

  def _updateGetterFunction(self, ) -> None:
    """Updates the getter method. """
    currentOwner = self._getCurrentOwner()
    getterKey = self._getGetterKey()
    getterFunction = getattr(currentOwner, getterKey, None)
    if getterFunction is None:
      curName = currentOwner.__name__
      fieldName = self.__field_name__
      e = """Current owner: '%s' does not implement a getter method for 
      field: '%s', expected at name: '%s'!"""
      raise AttributeError(monoSpace(e % (curName, fieldName, getterKey)))
    if not callable(getterFunction):
      e = typeMsg('getterFunction', getterFunction, Callable)
      raise TypeError(e)
    self.__current_getter__ = getterFunction

  def _updateSetterFunctions(self, ) -> None:
    """Updates the setter methods. """
    currentOwner = self._getCurrentOwner()
    setterKeys = self._getSetterKeys()
    setterFunctions = []
    for setterKey in setterKeys:
      setterFunction = getattr(currentOwner, setterKey, None)
      if setterFunction is None:
        curName = currentOwner.__name__
        fieldName = self.__field_name__
        e = """Current owner: '%s' does not implement a setter method for 
        field: '%s', expected at name: '%s'!"""
        raise AttributeError(monoSpace(e % (curName, fieldName, setterKey)))
      if not callable(setterFunction):
        e = typeMsg('setterFunction', setterFunction, Callable)
        raise TypeError(e)
      setterFunctions.append(setterFunction)
    self.__current_setters__ = setterFunctions

  def _updateDeleterFunctions(self, ) -> None:
    """Updates the deleter methods. """
    currentOwner = self._getCurrentOwner()
    deleterKeys = self._getDeleterKeys()
    deleterFunctions = []
    for deleterKey in deleterKeys:
      deleterFunction = getattr(currentOwner, deleterKey, None)
      if deleterFunction is None:
        curName = currentOwner.__name__
        fieldName = self.__field_name__
        e = """Current owner: '%s' does not implement a deleter method for 
        field: '%s', expected at name: '%s'!"""
        raise AttributeError(monoSpace(e % (curName, fieldName, deleterKey)))
      if not callable(deleterFunction):
        e = typeMsg('deleterFunction', deleterFunction, Callable)
        raise TypeError(e)
      deleterFunctions.append(deleterFunction)
    self.__current_deleters__ = deleterFunctions

  def _getCurrentGetter(self) -> Callable:
    """Getter-function for the current getter. """
    if self.__current_getter__ is None:
      e = """The getter method is not defined!"""
      raise AttributeError(e)
    if callable(self.__current_getter__):
      return self.__current_getter__
    e = typeMsg('__current_getter__', self.__current_getter__, Callable)
    raise TypeError(e)

  def _getCurrentSetters(self) -> list[Callable]:
    """Getter-function for the current setters. """
    return maybe(self.__current_setters__, [])

  def _getCurrentDeleters(self) -> list[Callable]:
    """Getter-function for the current deleters. """
    return maybe(self.__current_deleters__, [])

  def _validateOwner(self, owner: type, **kwargs) -> type:
    """Validates the owner type. """
    if not isinstance(owner, type):
      e = typeMsg('owner', owner, type)
      raise TypeError(e)
    currentOwner = self._getCurrentOwner()
    if currentOwner is owner:
      return owner
    if kwargs.get('_recursion', False):
      raise RecursionError
    if not issubclass(owner, self.__base_owner__):
      e = """The owner: '%s' is not a subclass of the base owner: '%s'!"""
      thisOwner = self.__base_owner__.__name__
      susOwner = owner.__name__
      raise TypeError(monoSpace(e % (susOwner, thisOwner)))
    self._setCurrentOwner(owner)
    return self._validateOwner(owner, _recursion=True)

  def __get__(self, instance: object, owner: type) -> Any:
    """Getter method for the descriptor. """
    if instance is None:
      return self
    owner = self._validateOwner(owner)
    getter = self._getCurrentGetter()
    return getter(instance)

  def __set__(self, instance: object, value: Any) -> None:
    """Setter method for the descriptor. """
    self._validateOwner(type(instance).__mro__[0])
    setters = self._getCurrentSetters()
    if not setters:
      fieldName = self.getFieldName()
      ownerName = self._getCurrentOwner().__name__
      e = """The descriptor: '%s' on class: '%s' does not implement 
      attribute setting, but an attempt at setting was made!"""
      raise AttributeError(monoSpace(e % (fieldName, ownerName)))
    for setter in setters:
      setter(instance, value)

  def __delete__(self, instance: object) -> None:
    """Deleter method for the descriptor. """
    self._validateOwner(type(instance).__mro__[0])
    deleters = self._getCurrentDeleters()
    if not deleters:
      fieldName = self.getFieldName()
      ownerName = self._getCurrentOwner().__name__
      e = """The descriptor: '%s' on class: '%s' does not implement 
      attribute deletion, but an attempt at deletion was made!"""
      raise AttributeError(monoSpace(e % (fieldName, ownerName)))
    for deleter in deleters:
      deleter(instance)

"""WorkToy - Descriptors - Field
Basic descriptor implementation."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from worktoy.worktoyclass import WorkToyClass
from worktoy.core import Function


class Field(WorkToyClass):
  """WorkToy - Fields - Field
  Basic descriptor implementation."""

  def __init__(self, *args, **kwargs) -> None:
    WorkToyClass.__init__(self, *args, **kwargs)
    self._defaultValue = (args or (None,))[0]
    self._fieldName = None
    self._fieldOwner = None
    self._getterFunction = None
    self._setterFunction = None
    self._deleterFunction = None

  def __matmul__(self, other: Any) -> Field:
    """Assigns the default value"""
    self._defaultValue = other
    return self

  def _getDefaultValue(self) -> Any:
    """Getter-function for the default value."""
    return self._defaultValue

  def setFieldName(self, fieldName: str) -> None:
    """Setter-function for the field name."""
    self._fieldName = fieldName

  def getFieldName(self, ) -> str:
    """Getter-function for the field name."""
    if self._fieldName is None:
      from worktoy.waitaminute import MissingArgumentException
      raise MissingArgumentException('_fieldName')
    return self._fieldName

  def getPrivateFieldName(self, ) -> str:
    """Getter-function for the private field name on the object. """
    return '_%s' % self.getFieldName()

  def setFieldOwner(self, cls: type) -> None:
    """Setter-function for the field owner."""
    cls = self.wrapFieldOwnerInit(cls)
    self._fieldOwner = cls

  def wrapFieldOwnerInit(self, cls: type) -> type:
    """Wraps the initiator of the field owner."""
    __original_init__ = getattr(cls, '__init__', None)

    if __original_init__ is object.__init__:
      __original_init__ = lambda *args, **kwargs: None

    def __new_init__(instance: object, *args, **kwargs) -> None:
      """Wrapper on the original init."""
      setattr(instance, self.getPrivateFieldName(), self._getDefaultValue())
      if __original_init__ is object.__init__:
        __original_init__(instance)
      else:
        __original_init__(instance, *args, **kwargs)

    setattr(cls, '__init__', __new_init__)
    return cls

  def getFieldOwner(self, ) -> type:
    """Getter-function for the field owner."""
    if self._fieldOwner is None:
      from worktoy.waitaminute import MissingArgumentException
      raise MissingArgumentException('fieldOwner')
    return self._fieldOwner

  def __set_name__(self, cls: type, name: str) -> None:
    """At creation of owner."""
    self.setFieldName(name)
    self.setFieldOwner(cls)

  def __get__(self, obj: object, cls: type) -> Any:
    """Getter descriptor."""
    return self.someGuard(self._getterFunction)(obj)

  def __set__(self, obj: object, newValue: Any) -> None:
    """Setter-descriptor."""
    self.someGuard(self._setterFunction)(obj, newValue)

  def __delete__(self, obj: object) -> None:
    """Deleter-descriptor"""
    self.someGuard(self._deleterFunction)(obj)

  def getter(self, getterFunction: Function) -> Function:
    """Sets the getter function to the decorated function before returning
    it."""
    self.overRideGuard(
      self._getterFunction, '_getterFunction', getterFunction)
    self._getterFunction = getterFunction
    return getterFunction

  def setter(self, setterFunction: Function) -> Function:
    """Sets the setter function to the decorated function before returning
    it."""
    self.overRideGuard(
      self._setterFunction, '_setterFunction', setterFunction)
    self._setterFunction = setterFunction
    return setterFunction

  def deleter(self, deleterFunction: Function) -> Function:
    """Sets the deleter function to the decorated function before returning
    it."""
    self.overRideGuard(
      self._deleterFunction, '_deleterFunction', deleterFunction)
    self._deleterFunction = deleterFunction
    return deleterFunction

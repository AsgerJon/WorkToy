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
      from worktoy.waitaminute import UnexpectedStateError
      raise UnexpectedStateError('_fieldName')
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
      __original_init__(instance, *args, **kwargs)
      setattr(instance, self.getPrivateFieldName(), self._getDefaultValue())

    setattr(cls, '__init__', __new_init__)
    return cls

  def getFieldOwner(self, ) -> type:
    """Getter-function for the field owner."""
    if self._fieldOwner is None:
      from worktoy.waitaminute import UnexpectedStateError
      raise UnexpectedStateError('fieldOwner')
    return self._fieldOwner

  def __set_name__(self, cls: type, name: str) -> None:
    """At creation of owner."""
    self.setFieldName(name)
    self.setFieldOwner(cls)

  def __get__(self, obj: object, cls: type) -> Any:
    """Getter descriptor."""
    if self._getterFunction is None:
      from worktoy.waitaminute import UnexpectedStateError
      raise UnexpectedStateError('_getterFunction')
    return self._getterFunction(obj, cls)

  def __set__(self, obj: object, newValue: Any) -> None:
    """Setter-descriptor."""
    if self._setterFunction is None:
      from worktoy.waitaminute import UnexpectedStateError
      raise UnexpectedStateError('_setterFunction')
    print('cunt', self.getFieldOwner(), obj, newValue, )
    self._setterFunction(obj, newValue)

  def __delete__(self, obj: object) -> None:
    """Deleter-descriptor"""
    if self._deleterFunction is None:
      from worktoy.waitaminute import UnexpectedStateError
      raise UnexpectedStateError('_deleterFunction')
    self._deleterFunction(obj)

  def getter(self, getterFunction: Function) -> Function:
    """Sets the getter function to the decorated function before returning
    it."""
    if self._getterFunction is not None:
      from worktoy.waitaminute import UnavailableNameException
      name = '_getterFunction'
      oldVal = self._getterFunction
      newVal = getterFunction
      raise UnavailableNameException(name, oldVal, newVal)
    self._getterFunction = getterFunction
    return getterFunction

  def setter(self, setterFunction: Function) -> Function:
    """Sets the setter function to the decorated function before returning
    it."""
    if self._setterFunction is not None:
      from worktoy.waitaminute import UnavailableNameException
      name = '_setterFunction'
      oldVal = self._setterFunction
      newVal = setterFunction
      raise UnavailableNameException(name, oldVal, newVal)
    self._setterFunction = setterFunction
    return setterFunction

  def deleter(self, deleterFunction: Function) -> Function:
    """Sets the deleter function to the decorated function before returning
    it."""
    if self._deleterFunction is not None:
      from worktoy.waitaminute import UnavailableNameException
      name = '_deleterFunction'
      oldVal = self._deleterFunction
      newVal = deleterFunction
      raise UnavailableNameException(name, oldVal, newVal)
    self._deleterFunction = deleterFunction
    return deleterFunction

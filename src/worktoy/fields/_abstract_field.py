"""WorkToy - Fields - AbstractField
Base class for descriptor implemented fields."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import Any

from icecream import ic

from worktoy.fields import AbstractDescriptor

ic.configureOutput(includeContext=True)


class _AbstractFieldProperties(AbstractDescriptor):
  """Properties class for field"""

  def __init__(self, *__, **_) -> None:
    AbstractDescriptor.__init__(self, *__, **_)
    self._fieldName = None
    self._fieldOwner = None
    self._fieldSource = None
    self._defaultValue = None

  def getFieldName(self, ) -> str:
    """Getter-function for field name"""
    if self._fieldName is None:
      from worktoy.waitaminute import UnexpectedStateError
      raise UnexpectedStateError('fieldName', self.getFieldName)
    return self._fieldName

  def getPrivateName(self, ) -> str:
    """Getter-function for the name of the private variable"""
    return '_%s' % (self._fieldName)

  def getGetterName(self, ) -> str:
    """Getter-function for the name of the getter function"""
    return '_get%s%s' % (self._fieldName[0].upper(), self._fieldName[1:])

  def getSetterName(self, ) -> str:
    """Getter-function for the name of the setter function"""
    return '_set%s%s' % (self._fieldName[0].upper(), self._fieldName[1:])

  def getDeleterName(self, ) -> str:
    """Getter-function for the name of the deleter function"""
    return '_del%s%s' % (self._fieldName[0].upper(), self._fieldName[1:])

  def getFieldOwner(self, ) -> type:
    """Getter-function for field owner class"""
    if self._fieldOwner is None:
      from worktoy.waitaminute import UnexpectedStateError
      raise UnexpectedStateError('_fieldOwner')
    return self._fieldOwner

  def setFieldOwner(self, owner: type) -> None:
    """Setter-function for field owner class"""
    self._fieldOwner = owner

  def setFieldName(self, fieldName: str, ) -> None:
    """Setter-function for field name"""
    self._fieldName = fieldName

  @abstractmethod
  def explicitGetter(self, obj: object, cls: type) -> object:
    """Explicit getter function. Subclasses must implement this method."""

  @abstractmethod
  def explicitSetter(self, obj: object, newValue: object) -> object:
    """Explicit setter function. Subclasses must implement this method."""

  @abstractmethod
  def explicitDeleter(self, obj: object, ) -> object:
    """Explicit deleter function. Subclasses must implement this method."""

  @abstractmethod
  def __set_name__(self, fieldOwner: type, fieldName: str) -> None:
    """The AbstractField method does provide does method."""


class AbstractField(_AbstractFieldProperties):
  """Field class"""

  def __init__(self, defVal: Any, *args, **kwargs) -> None:
    _AbstractFieldProperties.__init__(self, *args, **kwargs)
    self._defaultValue = defVal
    self._fieldSource = type(defVal)

  def explicitGetter(self, obj: object, cls: type) -> Any:
    """Explicit getter function. Tries to find the _get[NAME] method on
    the object."""
    return getattr(obj, self.getPrivateName(), self.getDefaultValue())

  def explicitSetter(self, obj: object, newValue: object) -> None:
    """Explicit setter function. Tries to find the _set[NAME] method on
    the object."""
    pvtName = self.getPrivateName()
    return setattr(obj, pvtName, newValue)

  def explicitDeleter(self, obj: object, ) -> None:
    """Explicit deleter function. Tries to find the _set[NAME] method on
    the object."""
    pvtName = self.getPrivateName()
    fieldName = self.getFieldName()
    delattr(obj, pvtName)
    delattr(obj, fieldName)

  def getFieldSource(self) -> type:
    """Subclasses must implement this method."""
    return self._fieldSource

  def getDefaultValue(self) -> Any:
    """Getter-function for the default value."""
    return self._defaultValue

  def __set_name__(self, cls: type, name: str) -> None:
    self.setFieldName(name)
    self.setFieldOwner(cls)

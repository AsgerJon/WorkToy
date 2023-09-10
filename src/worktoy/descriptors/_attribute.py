"""WorkToy - Descriptors - Attribute
Implementation of descriptor attribute."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import Any

from worktoy.worktoyclass import WorkToyClass


class AbstractAttribute(WorkToyClass):
  """WorkToy - Fields - IntAttribute
  Field implementation of integer valued descriptor."""

  @classmethod
  @abstractmethod
  def getClassDefaultValue(cls) -> Any:
    """Getter-function for default value."""

  @abstractmethod
  def getType(self) -> type:
    """Getter-function for value type."""

  def __init__(self, defVal: Any = None, *args, **kwargs) -> None:
    WorkToyClass.__init__(self, *args, **kwargs)
    self._defVal = self.maybe(defVal, self.getClassDefaultValue())
    self._fieldName = None
    self._fieldOwner = None

  def __set_name__(self, cls: type, name: str) -> None:
    """Setter for owner and name."""
    self.setFieldName(name)
    self.setFieldOwner(cls)

  def __get__(self, obj: Any, cls: type) -> Any:
    """Getter."""
    return self.explicitGetter(obj, cls)

  def __set__(self, obj: Any, newValue: Any) -> None:
    """Setter"""
    return self.explicitSetter(obj, newValue)

  def __delete__(self, obj: Any, ) -> None:
    """Setter"""
    return self.explicitDeleter(obj)

  def explicitSetter(self, obj: Any, newValue: Any) -> None:
    """Explicit setter function. """
    return setattr(obj, self.getPrivateName(), newValue)

  def explicitGetter(self, obj: Any, cls: type = None) -> Any:
    """Explicit getter function. """
    return getattr(obj, self.getPrivateName(), )

  def explicitDeleter(self, obj: Any, ) -> None:
    """Explicit deleter function. """
    return delattr(obj, self.getPrivateName(), )

  def getDefaultValue(self) -> Any:
    """Getter-function for instance default value."""
    return self._defVal

  def getPrivateName(self) -> str:
    """Getter-function for the private name"""
    return '_%s' % self.getFieldName()

  def extendInit(self, cls: type) -> type:
    """Extends the '__init__' method on the given class."""

    __original_init__ = getattr(cls, '__init__', None)

    def __new_init__(instance: Any, defVal: Any = None,
                     *args, **kwargs) -> None:
      """New initializer."""
      defVal = self.maybe(defVal, self.getDefaultValue())
      setattr(instance, self.getPrivateName(), defVal)

    if __original_init__ is object.__init__:
      setattr(cls, '__init__', __new_init__)
      return cls

    def __extended_init__(instance: Any, *args, **kwargs) -> None:
      """New initializer."""
      __original_init__(instance, *args, **kwargs)
      __new_init__(instance, *args, **kwargs)

    setattr(cls, '__init__', __extended_init__)
    return cls

  def getFieldName(self) -> str:
    """Getter-function for field name."""
    return self._fieldName

  def setFieldName(self, fieldName: str) -> None:
    """Setter-function for field name."""
    self._fieldName = fieldName

  def getFieldOwner(self) -> type:
    """Getter-function for field owner."""
    return self._fieldOwner

  def setFieldOwner(self, fieldOwner: type) -> None:
    """Setter-function for field owner."""
    self._fieldOwner = self.extendInit(fieldOwner)

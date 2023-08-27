"""WorkToy - Core - AbstractDescriptor
Provides an abstract descriptor class."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from icecream import ic

from worktoy.core import StringAware

ic.configureOutput(includeContext=True)


class _AbstractDescriptorProperties(StringAware):
  """Properties class for AbstractDescriptor"""

  def __init__(self,
               obj: object = None,
               cls: type = None,
               *args, **kwargs) -> None:
    StringAware.__init__(self, *args, **kwargs)
    self._defVal = None
    self._valueType = None
    self._fieldName = None
    self._fieldOwner = None

  def setFieldName(self, fieldName: str) -> bool:
    """Setter-function for the field name of this instance."""
    self._fieldName = fieldName
    return True if self.getFieldName() else False

  def getFieldName(self) -> str:
    """Getter-function for the field name of this instance. This is the
    name by which it appears in a class body. """
    return self._fieldName

  def setOwner(self, cls: type) -> bool:
    """Setter-function for the class where this instance was created."""
    self._fieldOwner = cls
    if self.getOwner() is cls:
      return True
    return False

  def getOwner(self) -> type:
    """Getter-function for the class where this instance was created."""
    return self._fieldOwner

  def setDefaultValue(self, defaultValue: object) -> None:
    """Setter-function for the default value"""
    self._defVal = defaultValue

  def getDefaultValue(self) -> object:
    """Getter-functino for the default value"""
    return self._defVal

  def setValueType(self, valueType: type) -> None:
    """Setter-function for the type of the underlying value."""
    self._valueType = valueType

  def getValueType(self, ) -> type:
    """Getter-function for the type of the underlying value."""
    return self._valueType

  def getPrivateVariableName(self) -> str:
    """Getter-function for private variable name"""
    return '%sPRIVATE' % self.getFieldName()


class AbstractDescriptor(_AbstractDescriptorProperties):
  """WorkToy - Core - AbstractDescriptor
  Provides an abstract descriptor class."""

  @classmethod
  def __class_getitem__(cls, argTuple: tuple = None) -> AbstractDescriptor:
    for arg in argTuple:
      key = '__special_descriptor__'
      specialConstructor = getattr(arg, key, None)
      if specialConstructor is not None:
        return specialConstructor(argTuple, cls)
    return cls(*argTuple)

  def __init__(self, *args, **kwargs) -> None:
    _AbstractDescriptorProperties.__init__(self, *args, **kwargs)

  def __set_name__(self, cls: type, name: str) -> bool:
    if self.setFieldName(name):
      if self.setOwner(cls):
        return True
    raise TypeError

  def __get__(self, obj: object, cls: type) -> object:
    return self.maybe(self.explicitGetter(obj, cls), self.getDefaultValue())

  def __set__(self, obj: object, newValue: object) -> None:
    self.explicitSetter(obj, newValue)

  def __delete__(self, obj: object) -> None:
    self.explicitDeleter(obj)

  def explicitGetter(self, obj: object, cls: type) -> object:
    """Explicit getter function. Subclasses can reimplement this and other
    accessor functions customising behaviour."""
    return getattr(obj, self.getPrivateVariableName(), None)

  def explicitSetter(self, obj: object, newValue: object) -> None:
    """Explicit setter function."""
    setattr(obj, self.getPrivateVariableName(), newValue)

  def explicitDeleter(self, obj: object) -> None:
    """Explicit deleter function."""
    delattr(obj, self.getPrivateVariableName(), )
    delattr(obj, self.getFieldName(), )

  def __str__(self, ) -> str:
    fieldName = self.getFieldName()
    fieldClassName = self.typeName(self.__class__)
    valueTypeName = self.typeName(self.getValueType())
    ownerName = self.typeName(self.getOwner())
    header = 'Instance of %s.' % fieldClassName
    msg = """Class %s owns field %s which points to values of type: %s"""
    body = msg % (ownerName, fieldName, valueTypeName)
    return '\n'.join([header, body])

  def __repr__(self) -> str:
    fieldName = self.getFieldName()
    fieldClassName = self.__class__.__qualname__
    valueTypeName = self.getValueType().__qualname__
    return '%s = %s[%s]' % (fieldName, fieldClassName, valueTypeName)

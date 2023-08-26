"""WorkToy - Attributes - ConstantAttribute
This descriptor class allows simple attributes."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Never, cast

from worktoy.attributes import ReadyTarget
from worktoy.core import DefaultClass


class ConstantAttribute(DefaultClass):
  """WorkToy - Attributes - ConstantAttribute
  This descriptor class allows simple attributes."""

  def __init__(self, value: object,
               type_: type = None, *args, **kwargs) -> None:
    DefaultClass.__init__(self, *args, **kwargs)
    self._readyTarget = ReadyTarget(self)
    self._fieldValue = value
    self._fieldType = self.maybe(type_, type(self._fieldValue))
    self._fieldName = None
    self._targetClass = None

  def getReadyTarget(self) -> ReadyTarget:
    """Getter-function for the instance of Ready Target belonging to this
    attribute. """
    return self._readyTarget

  def getFieldType(self) -> type:
    """Getter-function for the field type"""
    return cast(type, self._fieldType)

  def getDefaultFieldValue(self) -> object:
    """Getter-function for the field value"""
    return self._fieldValue

  def getFieldName(self) -> str:
    """Getter-function for field name"""
    return self._fieldName

  def setFieldName(self, fieldName: str) -> None:
    """Getter-function for field name"""
    self._fieldName = fieldName

  def getPrivateVariableName(self) -> str:
    """Name of the private variable"""
    startLetter = self.getFieldName()[0].lower()
    remaining = self.getFieldName()[1:]
    return '_%s%s' % (startLetter, remaining)

  def getGetterFunctionName(self) -> str:
    """Name of the getter function"""
    startLetter = self.getFieldName()[0].upper()
    remaining = self.getFieldName()[1:]
    return '_get%s%s' % (startLetter, remaining)

  def wrapInit(self, targetClass: type) -> type:
    """Wraps the __init__ on the target class to include private variable
    and getter. Please note that the method is set on the targetClass not
    the instance. """
    originalInit = getattr(targetClass, '__init__', lambda *__, **_: None)
    privateFieldName = self.getPrivateVariableName()
    fieldName = self.getFieldName()
    defaultValue = self.getDefaultFieldValue()

    def newInit(instance: object, *args, **kwargs) -> None:
      """Wrapped __init__ method"""
      fieldValue = kwargs.get(fieldName, defaultValue)
      originalInit(instance, *args, **kwargs)
      setattr(instance, privateFieldName, fieldValue)

    setattr(targetClass, '__init__', newInit, )

    return targetClass

  def getterFunctionFactory(self, targetClass: type) -> type:
    """Creates a getter function for target class"""
    getterFunctionName = self.getGetterFunctionName()
    privateFieldName = self.getPrivateVariableName()

    def getterFunction(cls: type, instance: object) -> object:
      """Getter-function"""
      return getattr(instance, privateFieldName, None)

    setattr(targetClass, getterFunctionName, classmethod(getterFunction))

    return targetClass

  def setTargetClass(self, targetClass: type) -> type:
    """Setter function for the target class"""
    if self._targetClass is not None:
      raise TypeError
    self._targetClass = targetClass
    targetClass = self.wrapInit(targetClass)
    targetClass = self.getterFunctionFactory(targetClass)
    ready = self.getReadyTarget()
    targetClass = ready(targetClass)
    return cast(type, targetClass)

  def __set_name__(self, targetClass: type, fieldName: str) -> None:
    """Sets name"""
    self.setFieldName(fieldName)
    self.setTargetClass(targetClass)

  def __get__(self, obj: object, cls: type) -> object:
    """Getter"""
    getter = getattr(cls, self.getGetterFunctionName(), None)
    if getter is None:
      raise TypeError
    return getter(obj)

  def __set__(self, *_) -> Never:
    """Illegal setter"""
    raise TypeError

  def __delete__(self, *_) -> Never:
    """Illegal deleter"""
    raise TypeError

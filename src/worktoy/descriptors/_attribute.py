"""WorkToy - Descriptors - Attribute
Basic descriptor implementation."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from icecream import ic

from worktoy.core import Function
from worktoy.worktoyclass import WorkToyClass

ic.configureOutput(includeContext=True)


class Attribute(WorkToyClass):
  """WorkToy - Fields - Field
  Basic descriptor implementation."""

  def __init__(self, defVal: Any = None, *args, **kwargs) -> None:
    WorkToyClass.__init__(self, *args, **kwargs)
    self._defaultValue = None
    self._defaultType = None
    #  case 1: Receives a default value that is not a type
    if defVal is not None and not isinstance(defVal, type):
      self._setDefaultValue(defVal)
      self._defaultType = type(self._defaultValue)
    #  case 2: Receives a default value that is a type. This is taken to
    #  mean that the attribute is to hold a value of that type. The type
    #  is then called without argument to attempt to create a default value.
    if isinstance(defVal, type):
      self._setDefaultValue(defVal)
      self._defaultValue = defVal()
    # case 3: Receives no argument. In this case, the instance is
    # responsible for providing a default value. For example in the
    # instance '__init__ method using the public setter.
    # Please note, that fields must do one of the following:
    #   1. Provide a default value in the Field creation call (RECOMMENDED)
    #   2. Define a Field type in the creation call. (NOT RECOMMENDED)
    #   3. Have the owning class defer default instance creation to the
    #   first call to the getter function. This advanced use case allows
    #   the owning class to control specifically when and how to create
    #   instances. This is supported and encouraged, for advanced owning
    #   classes. (ADVANCED USE CASE)
    #   4. Subclass attribute to the specific type. (ADVANCED USE CASE)

    #   ATTENTION!
    #   Doing none of the above leads to HIGHLY UNDEFINED BEHAVIOUR!
    #   The Attribute is intended to raise MissingArgumentException in such
    #   cases.
    self._fieldName = None
    self._fieldOwner = None
    self._getterFunctionName = None
    self._setterFunctionName = None
    self._deleterFunctionName = None

  def __set_name__(self, cls: type, name: str) -> None:
    self._setFieldName(name)
    self._setFieldOwner(cls)

  def _getDefaultValue(self, ) -> Any:
    """Getter-function for the default value"""
    return self.someGuard(self._defaultValue, self._fieldName)

  def _getDefaultType(self, ) -> Any:
    """Getter-function for the default type"""
    return self.maybe(self._defaultType, object)

  def _setDefaultValue(self, defaultValue: Any, ) -> Any:
    """Setter-function for the default value"""
    if defaultValue is not None:
      if self.noneGuard(self._defaultValue):
        self._defaultValue = defaultValue
        self._defaultType = type(defaultValue)

  def _getFieldName(self, ) -> str:
    """Getter-function for the field name."""
    if self._fieldName is None:
      from worktoy.waitaminute import MissingArgumentException
      raise MissingArgumentException('_fieldName')
    return '%s_attribute' % self._fieldName

  def _setFieldName(self, fieldName: str) -> None:
    """Setter-function for the field name."""
    if self._fieldName is None:
      self._fieldName = fieldName

  def _getFieldOwner(self, ) -> type:
    """Getter-function for field owner"""
    return self._fieldOwner

  def _setFieldOwner(self, cls: type) -> None:
    """Setter-function for field owner"""
    self._fieldOwner = cls

  def _getPrivateFieldName(self, ) -> str:
    """Getter-function for the private field name on the object. """
    name = self._getFieldName()
    if all([not c.isupper() for c in name]):
      name = '%sAttribute' % name
    chars = ['_%s' % c.lower() if c.isupper() else c for c in name]
    return '__%s__' % (''.join(chars))

  def _getCapName(self) -> str:
    """Getter-function for the capitalized name"""
    return '%s%s' % (self._fieldName[0].upper(), self._fieldName[1:])

  def _getGetterName(self, ) -> str:
    """Getter-function for the private field name on the object. """
    if self._getterFunctionName is None:
      return '_get%s' % self._getCapName()
    return self._getterFunctionName

  def _getSetterName(self, ) -> str:
    """Getter-function for the private field name on the object. """
    if self._setterFunctionName is None:
      return '_set%s' % self._getCapName()
    return self._setterFunctionName

  def _getDeleterName(self, ) -> str:
    """Getter-function for the private field name on the object. """
    if self._deleterFunctionName is None:
      return '_del%s' % self._getCapName()
    return self._deleterFunctionName

  def __get__(self, obj: Any, cls: type) -> Any:
    """Descriptor getter"""
    getter = getattr(cls, self._getGetterName(), None)
    if isinstance(getter, Function):
      return getter(obj)
    pvtName = self._getPrivateFieldName()
    value = getattr(obj, pvtName, None)
    if value is not None:
      return value
    return self._getDefaultValue()

  def __set__(self, obj: Any, newVal: Any) -> None:
    """Descriptor setter"""
    cls = obj.__class__
    setter = getattr(cls, self._getSetterName(), None)
    if setter is None:
      return setattr(obj, self._getPrivateFieldName(), newVal)
    return setter(obj, newVal)

  def __delete__(self, obj: Any) -> None:
    """Descriptor deleter"""
    cls = obj.__class__
    deleter = getattr(cls, self._getDeleterName(), None)
    if deleter is None:
      return delattr(cls, self._getFieldName())
    deleter(obj)

  def GET(self, getFunc: Function) -> Function:
    """Sets explicit getter function"""
    self._getterFunctionName = getFunc.__name__
    return getFunc

  def SET(self, setFunc: Function) -> Function:
    """Sets explicit setter function"""
    self._setterFunctionName = setFunc.__name__
    return setFunc

  def DEL(self, delFunc: Function) -> Function:
    """Sets explicit deleter function"""
    self._deleterFunctionName = delFunc.__name__
    return delFunc

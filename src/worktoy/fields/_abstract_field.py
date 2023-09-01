"""WorkToy - Fields - AbstractField
Base class for descriptor implemented fields."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import Any
from warnings import warn

from icecream import ic

from worktoy.core import Function
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
    self._promises = []
    self._newPromises = []
    self._busy = False

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

  def setFieldName(self, fieldName: str) -> None:
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

  def __init__(self, *args, **kwargs) -> None:
    _AbstractFieldProperties.__init__(self, *args, **kwargs)

  def explicitGetter(self, obj: object, cls: type) -> object:
    """Explicit getter function. Tries to find the _get[NAME] method on
    the object."""
    getterKey = self.getGetterName()
    getterFunc = getattr(obj, getterKey, None)
    if getterFunc is None:
      warn('Getter-function for obj %s not available!' % obj)
      return 'Missing Getter!'
    value = getterFunc(obj)
    return value

  def explicitSetter(self, obj: object, newValue: object) -> object:
    """Explicit setter function. Tries to find the _set[NAME] method on
    the object."""
    setterKey = self.getSetterName()
    setterFunc = getattr(obj, setterKey, None)
    if setterFunc is None:
      warn('Setter-function for obj %s not available!' % obj)
      return
    setterFunc(obj, newValue)

  def explicitDeleter(self, obj: object, ) -> object:
    """Explicit deleter function. Tries to find the _set[NAME] method on
    the object."""
    deleterKey = self.getDeleterName()
    deleterFunc = getattr(obj, deleterKey, None)
    if deleterFunc is None:
      warn('Deleter-function for obj %s not available!' % obj)
      return
    deleterFunc(obj)

  def parseInstanceFunctionFactory(self, ) -> Function:
    """Getter-function for instance parsing function."""

    def parseInstance(*args, **kwargs) -> object:
      """Returns the first positional argument of the type indicated by
      the 'type_' keyword."""
      type_ = kwargs.get('type_', None)
      instance = None
      for arg in args:
        if isinstance(arg, type_) and instance is None:
          return arg

    return parseInstance

  def deleterFunctionFactory(self, ) -> Function:
    """Factory for deleter function."""
    pvtName = self.getPrivateName()
    parseInstance = self.parseInstanceFunctionFactory()
    fieldOwner = self.getFieldOwner()

    def deleter(*args) -> None:
      """Deleter-function"""
      instance = parseInstance(*args, type_=fieldOwner)
      delattr(instance, pvtName)

    return deleter

  def setterFunctionFactory(self, ) -> Function:
    """Factory for setter function."""
    pvtName = self.getPrivateName()
    parseInstance = self.parseInstanceFunctionFactory()
    fieldSource = self.getFieldSource()
    fieldOwner = self.getFieldOwner()

    def setter(*args) -> None:
      """Setter-function."""
      instance = parseInstance(*args, type_=fieldOwner)
      newValue = parseInstance(*args, type_=fieldSource)
      setattr(instance, pvtName, newValue)

    return setter

  def getterFunctionFactory(self, ) -> Function:
    """Factory for getter function"""
    pvtName = self.getPrivateName()
    parseInstance = self.parseInstanceFunctionFactory()
    fieldOwner = self.getFieldOwner()

    def getter(*args) -> object:
      """Getter-function"""
      instance = parseInstance(*args, type_=fieldOwner)
      return getattr(instance, pvtName, )

    return getter

  def setFieldOwner(self, fieldOwner: type) -> None:
    """Installs in the field on the owner."""
    initName = '__init__'
    getName = self.getGetterName()
    setName = self.getSetterName()
    delName = self.getDeleterName()

    __wrapped_init__ = self.wrappedInitFactory()
    __getter_function__ = self.getterFunctionFactory()
    __setter_function__ = self.setterFunctionFactory()
    __deleter_function__ = self.deleterFunctionFactory()

    setattr(fieldOwner, initName, __wrapped_init__)
    setattr(fieldOwner, getName, __getter_function__)
    setattr(fieldOwner, setName, __setter_function__)
    setattr(fieldOwner, delName, __deleter_function__)

  def wrappedInitFactory(self, ) -> Function:
    """Creates a wrapped __init__ method."""
    source = self.getFieldSource()
    originalInit = getattr(self.getFieldOwner, '__init__')
    privateName = self.getPrivateName()
    defValFactory = self.maybe(self.getDefValFactory, lambda *__, **_: None)
    if not isinstance(defValFactory, Function):
      from worktoy.waitaminute import TypeSupportError
      raise TypeSupportError(Function, defValFactory, 'defValFactory')

    def __wrapped_init__(instance: object, *args, **kwargs) -> None:
      originalInit(instance, *args, **kwargs)
      defVal = defValFactory(instance, *args, **kwargs)
      defValArg = self.maybeType(source, *args)
      defVal = self.maybe(defValArg, defVal)
      setattr(instance, privateName, defVal)

    return __wrapped_init__

  def __set_name__(self, fieldOwner: type, fieldName: str) -> None:
    self.setFieldName(fieldName)
    self.setFieldOwner(fieldOwner)

  @abstractmethod
  def getFieldSource(self) -> type:
    """Subclasses must implement this method."""

  def getDefValFactory(self, ) -> Any:
    """This method provides a custom default value. If subclasses
    implement this method, it should return a function creating the
    default value.If a subclass does not implement this method, the field
    source class is expected to provide handling the default value. """

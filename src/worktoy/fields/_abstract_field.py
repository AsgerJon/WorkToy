"""WorkToy - Fields - AbstractField
Base class for descriptor implemented fields."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from warnings import warn

from icecream import ic

from worktoy.core import Function, Promise
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

  def getDefaultValue(self) -> object:
    """Getter-function for the default value. """
    if self._defaultValue is None:
      e = type('ChillOutException', (Exception,), {})
      raise e
    return self._defaultValue

  def setDefaultValue(self, defaultValue: object) -> None:
    """Setter-function for default value"""
    if self.getFieldSource() is None:
      return self.deferCall(self.setDefaultValue, self, defaultValue)
    self._defaultValue = defaultValue

  def getFieldSource(self) -> type:
    """Getter-function for field source"""
    return self._fieldSource

  def getFieldName(self, ) -> str:
    """Getter-function for field name"""
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
    return self._fieldOwner

  def __set_name__(self, fieldOwner: type, fieldName: str) -> None:
    self.setFieldName(fieldName)
    self.setFieldOwner(fieldOwner)

  def setFieldName(self, fieldName: str) -> None:
    """Setter-function for field name"""
    self._fieldName = fieldName
    self.update()

  def setFieldSource(self, source: type) -> None:
    """Setter-function for field source"""
    self._fieldSource = source
    self.update()

  def getPromises(self) -> list[Promise]:
    """Getter-function for the list of promises deferred."""
    return self._newPromises if self.getBusy() else self._promises

  def deferCall(self, func: Function, *args, **kwargs) -> None:
    """Creates a promise"""
    self.getPromises().append(Promise(func.__func__, self, *args, **kwargs))

  def getBusy(self) -> bool:
    """Getter-function for the busy flag. """
    return True if self._busy else False

  def setBusy(self, value: object) -> None:
    """Setter-function for the busy flag. """
    self._busy = True if value else False

  def activateBusy(self) -> None:
    """Sets the busy flag True."""
    self._busy = True

  def deActivateBusy(self) -> None:
    """Sets the busy flag False."""
    self._busy = False

  def update(self, ) -> None:
    """Updater"""
    promises = self.getPromises()
    self.activateBusy()
    while promises:
      promise = promises.pop(0)
      promise()
    promises = self.getPromises()
    self.deActivateBusy()
    while promises:
      self.getPromises().append(promises.pop(0))

  def setFieldOwner(self, fieldOwner: type) -> None:
    """Setter-function for field owner class."""
    if self.getFieldName() is None:
      return self.deferCall(self.setFieldOwner, self, fieldOwner)
    if self.getFieldSource() is None:
      return self.deferCall(self.setFieldOwner, self, fieldOwner)
    self.installFieldOwner(fieldOwner)
    self.update()

  @abstractmethod
  def installFieldOwner(self, fieldOwner: type) -> None:
    """Installs in the field on the owner."""

  def fieldInstanceCreatorFactory(self, source: type) -> Function:
    """Creates the field default value from the given source type."""

    try:
      defVal = self.getDefaultValue()
    except Exception as error:
      handle = getattr(error, 'handle')
      handle()
      defVal = None

    if defVal is not None:
      def creator(*_) -> object:
        """Creator Function"""
        return defVal

      return creator

    def creator(*_) -> object:
      """Creator function"""
      func = getattr(source, '__get_default_instance__', None)
      if func is None:
        return source()
      return func()

    return creator

  @abstractmethod
  def explicitGetter(self, obj: object, cls: type) -> object:
    """Explicit getter function. Subclasses must implement this method."""

  @abstractmethod
  def explicitSetter(self, obj: object, newValue: object) -> object:
    """Explicit setter function. Subclasses must implement this method."""

  @abstractmethod
  def explicitDeleter(self, obj: object, ) -> object:
    """Explicit deleter function. Subclasses must implement this method."""


class AbstractField(_AbstractFieldProperties):
  """Field class"""

  def __init__(self, *args, **kwargs) -> None:
    _AbstractFieldProperties.__init__(self, *args, **kwargs)

  def wrappedInitFactory(self, fieldOwner: type) -> Function:
    """Creates a wrapped __init__ method."""

    source = self.getFieldSource()
    originalInit = getattr(fieldOwner, '__init__')
    defValFactory = self.fieldInstanceCreatorFactory(source)

    def __wrapped_init__(instance: object, *args, **kwargs):
      originalInit(instance, *args, **kwargs)
      privateName = self.getPrivateName()
      defVal = None
      for arg in args:
        if isinstance(arg, source) and defVal is None:
          defVal = arg
      defVal = defValFactory() if defVal is None else defVal
      setattr(instance, privateName, defVal)

    return __wrapped_init__

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

  def deleterFunctionFactory(self, fieldOwner) -> Function:
    """Factory for deleter function."""
    pvtName = self.getPrivateName()
    parseInstance = self.parseInstanceFunctionFactory()

    def deleter(*args) -> None:
      """Deleter-function"""
      instance = parseInstance(*args, type_=fieldOwner)
      delattr(instance, pvtName)

    return deleter

  def setterFunctionFactory(self, fieldOwner) -> Function:
    """Factory for setter function."""
    pvtName = self.getPrivateName()
    parseInstance = self.parseInstanceFunctionFactory()
    fieldSource = self.getFieldSource()

    def setter(*args) -> None:
      """Setter-function."""
      instance = parseInstance(*args, type_=fieldOwner)
      newValue = parseInstance(*args, type_=fieldSource)
      setattr(instance, pvtName, newValue)

    return setter

  def getterFunctionFactory(self, fieldOwner) -> Function:
    """Factory for getter function"""
    pvtName = self.getPrivateName()
    parseInstance = self.parseInstanceFunctionFactory()

    def getter(*args) -> object:
      """Getter-function"""
      instance = parseInstance(*args, type_=fieldOwner)
      return getattr(instance, pvtName, )

    return getter

  def installFieldOwner(self, fieldOwner: type) -> None:
    """Installs in the field on the owner."""
    if self.getFieldName() is None or self.getFieldSource() is None:
      return self.deferCall(self.installFieldOwner, self, fieldOwner)
    getName = self.getGetterName()
    setName = self.getSetterName()
    delName = self.getDeleterName()

    __wrapped_init__ = self.wrappedInitFactory(fieldOwner)
    __getter_function__ = self.getterFunctionFactory(fieldOwner)
    __setter_function__ = self.setterFunctionFactory(fieldOwner)
    __deleter_function__ = self.deleterFunctionFactory(fieldOwner)

    setattr(fieldOwner, '__init__', __wrapped_init__)
    setattr(fieldOwner, getName, __getter_function__)
    setattr(fieldOwner, setName, __setter_function__)
    setattr(fieldOwner, delName, __deleter_function__)
    self.update()

  def explicitGetter(self, obj: object, cls: type) -> object:
    """Explicit getter function. Subclasses must implement this method."""
    getterKey = self.getGetterName()
    getterFunc = getattr(obj, getterKey, None)
    if getterFunc is None:
      warn('Getter-function for obj %s not available!' % obj)
      return 'Missing Getter!'
    value = getterFunc(obj)
    return value

  def explicitSetter(self, obj: object, newValue: object) -> object:
    """Explicit setter function. Subclasses must implement this method."""
    setterKey = self.getSetterName()
    setterFunc = getattr(obj, setterKey, None)
    if setterFunc is None:
      warn('Setter-function for obj %s not available!' % obj)
      return
    setterFunc(obj, newValue)

  def explicitDeleter(self, obj: object, ) -> object:
    """Explicit deleter function. Subclasses must implement this method."""
    deleterKey = self.getDeleterName()
    deleterFunc = getattr(obj, deleterKey, None)
    if deleterFunc is None:
      warn('Deleter-function for obj %s not available!' % obj)
      return
    deleterFunc(obj)

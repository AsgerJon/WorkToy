"""WorkToy - Core - AbstractDescriptor
Provides an abstract descriptor class."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from icecream import ic

from worktoy.core import StringAware, Function

ic.configureOutput(includeContext=True)


class MetaMeta(type):
  """Metaclass"""

  def __repr__(cls) -> str:
    return '__repr__: %s' % cls.__qualname__

  def __str__(cls) -> str:
    return '__str__: %s' % cls.__qualname__


class _AbstractDescriptorProperties(StringAware, metaclass=MetaMeta):
  """Properties class for AbstractDescriptor"""

  def __init__(self,
               obj: object = None,
               cls: type = None,
               *args, **kwargs) -> None:
    StringAware.__init__(self, *args, **kwargs)
    self._defVal = None
    self._sourceClass = None
    self._fieldName = None
    self._fieldOwner = None

  def setFieldName(self, fieldName: str) -> bool:
    """Setter-function for the field name of this instance."""
    self._fieldName = fieldName
    return True if self.getFieldName() == self._fieldName else False

  def getFieldName(self) -> str:
    """Getter-function for the field name of this instance. This is the
    name by which it appears in a class body. """
    return self._fieldName

  def setDefaultValue(self, defaultValue: object) -> None:
    """Setter-function for the default value"""
    self._defVal = defaultValue

  def getDefaultValue(self) -> object:
    """Getter-functino for the default value"""
    return self._defVal

  def setSourceClass(self, source: type) -> None:
    """Setter-function for the type of the underlying value."""
    self._sourceClass = source

  def getSourceClass(self, ) -> type:
    """Getter-function for the type of the underlying value."""
    return self._sourceClass

  def getPrivateVariableName(self) -> str:
    """Getter-function for private variable name"""
    return '_%s' % self.getFieldName()

  def getGetterFunctionName(self) -> str:
    """Getter-function for the name of the getter function on the owner
    class."""
    startLetter = self.getFieldName()[0].upper()
    restLetters = self.getFieldName()[1:]
    return '_get%s%s' % (startLetter, restLetters)

  def getSetterFunctionName(self) -> str:
    """Getter-function for the name of the setter function on the owner
    class."""
    startLetter = self.getFieldName()[0].upper()
    restLetters = self.getFieldName()[1:]
    return '_set%s%s' % (startLetter, restLetters)

  def getDeleterFunctionName(self) -> str:
    """Getter-function for the name of the deleter function on the owner
    class."""
    startLetter = self.getFieldName()[0].upper()
    restLetters = self.getFieldName()[1:]
    return '_del%s%s' % (startLetter, restLetters)

  def getCreatorFunctionName(self) -> str:
    """Getter-function for the name of the creator function on the owner
    class."""
    startLetter = self.getFieldName()[0].upper()
    restLetters = self.getFieldName()[1:]
    return '_create%s%s' % (startLetter, restLetters)


class AbstractDescriptor(_AbstractDescriptorProperties):
  """WorkToy - Core - AbstractDescriptor
  Provides an abstract descriptor class."""

  __key__ = 'Abstract'

  @classmethod
  def __class_getitem__(cls, argTuple: tuple = None) -> AbstractDescriptor:
    if not isinstance(argTuple, tuple):
      argTuple = (argTuple,)
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
    return self.explicitGetter(obj, cls)

  def __set__(self, obj: object, newValue: object) -> None:
    self.explicitSetter(obj, newValue)

  def __delete__(self, obj: object) -> None:
    self.explicitDeleter(obj)

  def explicitGetter(self, obj: object, cls: type) -> object:
    """Explicit getter function. Subclasses can reimplement this and other
    accessor functions customising behaviour."""
    getter = getattr(self.getOwner(), self.getGetterFunctionName(), None)
    if getter is None:
      raise TypeError
    return getter(obj)

  def explicitSetter(self, obj: object, newValue: object) -> None:
    """Explicit setter function."""
    setter = getattr(self.getOwner(), self.getSetterFunctionName(), None)
    if setter is None:
      raise TypeError
    sourceType = self.getSourceClass()
    if sourceType is None:
      msg = """Setter function called before sourceType has been defined!"""
      raise TypeError(msg)
    if not isinstance(sourceType, type):
      msg = """Expected sourceType to be of type 'type', but received: """
      body = """%s!""" % type(sourceType)
      raise TypeError(self.monoSpace('%s%s' % (msg, body)))
    if not isinstance(newValue, sourceType):
      msg = """Setter function expected new value: %s to be of type: %s, 
      but received: %s!""" % (newValue, sourceType, type(newValue))
      raise TypeError(self.monoSpace(msg))
    setter(obj, newValue)

  def explicitDeleter(self, obj: object) -> None:
    """Explicit deleter function."""
    deleter = getattr(self.getOwner(), self.getDeleterFunctionName(), None)
    if deleter is None:
      raise TypeError
    deleter(obj)

  def __str__(self, ) -> str:
    fieldName = self.getFieldName()
    fieldClassName = self.__class__.__qualname__
    ownerClass = self.getOwner()
    sourceClass = self.getSourceClass()
    source, owner = None, None
    if sourceClass is not None and isinstance(sourceClass, type):
      source = sourceClass.__qualname__
    if ownerClass is not None and isinstance(ownerClass, type):
      owner = ownerClass.__qualname__
    if fieldName is None and source is None:
      return 'Descriptor class: %s ready to be initialised.' % fieldClassName
    if fieldName is None:
      msg = """Descriptor class %s exposing source type: %s."""
      return msg % (fieldClassName, source)
    msg = """Descriptor class %s exposing source type: %s set at owner 
    class: %s at field name: %s"""
    return msg % (fieldClassName, source, owner, fieldName)

  def __repr__(self) -> str:
    fieldName = self.getFieldName()
    fieldClassName = self.__class__.__qualname__
    msg = """%s = %s(...)""" % (fieldName, fieldClassName)
    return msg

  def setOwner(self, type_: type) -> bool:
    """Setter-function for the class where this instance was created."""
    fieldName = self.getFieldName()
    privateName = self.getPrivateVariableName()
    getterName = self.getGetterFunctionName()
    setterName = self.getSetterFunctionName()
    creatorName = self.getCreatorFunctionName()
    deleterName = self.getDeleterFunctionName()

    def getter(cls: type, obj: object, **kwargs) -> object:
      """Getter-function"""
      out = getattr(obj, privateName, None)
      if out is None and kwargs.get('_redundant', False):
        raise RecursionError
      if out is None:
        creatorFunction = getattr(obj, creatorName, None)
        if creatorFunction is None:
          raise TypeError
        creatorFunction(obj)
        return getter(cls, obj, _redundant=True)
      return out

    sourceCreator = self.sourceInstanceFactory()

    def creator(cls: type, obj: object) -> None:
      """Creator-function"""
      instance = sourceCreator(cls, obj)
      setattr(obj, privateName, instance)

    def setter(cls: type, obj: object, newValue: object) -> None:
      """Setter-function"""
      setattr(obj, privateName, newValue)

    def deleter(cls: type, obj: object) -> None:
      """Deleter-function"""
      delattr(obj, privateName)
      delattr(obj, fieldName)

    setattr(type_, getterName, classmethod(getter))
    setattr(type_, creatorName, classmethod(creator))
    setattr(type_, setterName, classmethod(setter))
    setattr(type_, deleterName, classmethod(deleter))
    self._fieldOwner = type_
    if self.getOwner() is type_:
      return True
    return False

  def getOwner(self) -> type:
    """Getter-function for the class where this instance was created."""
    return self._fieldOwner

  def sourceInstanceFactory(self) -> Function:
    """Factory for source instance creators."""
    source = self.getSourceClass()

    def sourceInstanceCreator(cls: type, obj: object) -> object:
      """Source instance creator"""
      return source()

    return sourceInstanceCreator

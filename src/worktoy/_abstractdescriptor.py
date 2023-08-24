"""WorkToy - AbstractDescriptor
Abstract base class for creating descriptor objects within the WorkToy
module. Provides a foundational structure for managing properties with
specialized getter, setter, and factory methods. Designed to be subclassed.
"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import Never

from worktoy import DefaultClass
from worktoy import FunctionList, Function


class _PropertiesDescriptor(DefaultClass):
  """Contains the property-related functions"""

  def __init__(self, *args, **kwargs):
    DefaultClass.__init__(self, *args, **kwargs)
    self._name = None
    self._targetClass = None
    self._parseClass = self.parseFactory(type, 'cls', 'type_', 'class')

  def _getName(self) -> str:
    """Getter-function for the name"""
    if self._name is None:
      raise TypeError
    return self._name

  def getInstanceName(self) -> str:
    """Getter-function for the key to the sourceInstance on the target"""
    return '_%sInstance' % self._getName()

  def getGetterName(self) -> str:
    """Getter-function for the key to the getter-function on the target"""
    return '_get%s' % self._getName().capitalize()

  def getFactoryName(self) -> str:
    """Getter-function for the key to the factory function on the target"""
    return '_set%s' % self._getName().capitalize()

  def _setName(self, name: str) -> None:
    """Setter-function for the name."""
    if self._name is not None:
      raise TypeError
    self._name = name


class AbstractDescriptor(_PropertiesDescriptor):
  """WorkToy - AbstractDescriptor
  This class provides the abstract baseclass for descriptors"""

  def __init__(self, *args, **kwargs) -> None:
    """
    Constructor for initializing instance. Calls parent's constructor and
    sets the target class.

    :param *args: Positional arguments for parent.
    :param **kwargs: Keyword arguments for parent.
    """
    _PropertiesDescriptor.__init__(self, *args, **kwargs)

  @abstractmethod
  def getSourceClass(self) -> type:
    """
    Abstract method to get source class. Must be implemented by subclasses.

    :return: Type of the source class.
    """

  @abstractmethod
  def instanceCreatorFactory(self) -> Function:
    """
    Abstract factory to create creator-function for source class. Subclasses
    must implement.

    :return: Function object for creator function.
    """

  def _getTargetClass(self) -> type:
    """Getter-function for the source class"""
    return self._targetClass

  def _setTargetClass(self, *args, **kwargs) -> None:
    """Setter-function for the target class"""
    if self._targetClass is not None:
      raise TypeError
    cls = self._parseClass(*args, **kwargs)
    if not isinstance(cls, type):
      raise TypeError
    initName = '__init__'
    getterName = self.getGetterName()
    factoryName = self.getFactoryName()
    wrappedInit = self.getExtendedInit(cls)
    getterFunc = self.getterFunctionFactory()
    factoryFunc = self.instanceCreatorFactory()
    setattr(cls, initName, wrappedInit)
    setattr(cls, getterName, getterFunc)
    setattr(cls, factoryName, factoryFunc)
    self._targetClass = cls

  def getExtendedInit(self, cls: type) -> Function:
    """This method extends the target __init__."""
    targetInit = getattr(cls, '__init__', None)
    if targetInit is None:
      raise TypeError
    if not isinstance(targetInit, (*FunctionList,)):
      raise TypeError
    varName = self.getInstanceName()

    def wrappedInit(instance: object, *args, **kwargs) -> None:
      """Extended initiator method"""
      targetInit(instance, *args, **kwargs)
      setattr(instance, varName, None)

    return wrappedInit

  def getterFunctionFactory(self) -> Function:
    """Factory for the getter function"""
    varName = self.getInstanceName()

    def getterFunction(instance: object, ) -> object:
      """Getter-function"""
      sourceInstance = getattr(instance, varName, None)
      if sourceInstance is None:
        raise TypeError
      return sourceInstance

    return getterFunction

  def factoryFunctionFactory(self) -> Function:
    """Factory for the factory function"""
    varName = self.getInstanceName()
    factory = self.factoryFunctionFactory()

    def factoryFunction(instance: object) -> None:
      """Factory-function"""
      sourceInstance = factory(instance)
      setattr(instance, varName, sourceInstance)

    return factoryFunction

  def __set_name__(self, target: type, name: str) -> None:
    """Implementation of name setter. The 'target' is also called 'owner'
    in documentation."""
    self._name = name
    self._setTargetClass(target)

  def __get__(self, obj: object, target: type) -> object:
    """
    Implementation of descriptor getter. Retrieves getter function from
    target and invokes it on the instance.

    :param obj: Object instance.
    :param target: Type of target class.
    :return: Result of calling getter function.
    """
    getter = getattr(target, self.getGetterName(), None)
    if getter is None:
      raise AttributeError
    if not isinstance(getter, Function):
      raise TypeError
    return getter(obj)

  def __set__(self, *_) -> Never:
    """
    Implementation of descriptor setter. Disabled, raises TypeError.

    :raise TypeError: Always raised as setting is disabled.
    """
    raise TypeError

  def __delete__(self, *_) -> Never:
    """
    Implementation of descriptor deletion. Disabled, raises TypeError.

    :raise TypeError: Always raised as deletion is disabled.
    """
    raise TypeError

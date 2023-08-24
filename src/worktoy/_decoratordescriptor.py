"""WorkToy - DecoratorDescriptor
This subclass of AbstractDescriptor combines decorator and descriptor
capability such that decorated classes can be placed as descriptors on
other classes.

Instances receive a 'source' class through the __call__ method. This must
set the following instance variables:
  - sourceClass: should point to the SourceClass itself, not to an instance.
  - sourceInstanceCreatorFactory: should point to a method creating
    instance factories to be set on target. The creator function must not
    require arguments.

The AbstractDecorator further supports the following optional capabilities:
  - Reimplementation of 'getExtendedInit'. The default is to place a
  variable in the local namespace pointing to None. This variable is later
  populated with the getter and creator methods. Subclasses may
  reimplement this method to provide alternative behaviour.

  - Reimplementation of 'getterFunctionFactory'. This method creates a
  getter function that is later set as attribute on the target class. Then
  the __get__ uses this function to retrieve the source value from the
  target instance. Subclasses may reimplement this method to provide
  alternative behaviour.

  - Reimplementation of 'factoryFunctionFactory'. This method relies on
  the instance creation method provided by the subclass, which takes no
  arguments. Subclasses may reimplement this method to provide alternative
  behaviour.

    """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy import AbstractDescriptor, Function


class DecoratorDescriptor(AbstractDescriptor):
  """WorkToy - DecoratorDescriptor
  This subclass of AbstractDescriptor combines decorator and descriptor
  capability such that decorated classes can be placed as descriptors on
  other classes."""

  def __init__(self, *args, **kwargs) -> None:
    AbstractDescriptor.__init__(self, *args, **kwargs)
    self._sourceClass = None

  def getSourceClass(self) -> type:
    """Getter-function for the source class"""
    return self._sourceClass

  def setSourceClass(self, cls: type) -> None:
    """Setter-function for the source class. """
    if not isinstance(cls, type):
      raise TypeError
    self._sourceClass = cls

  def instanceCreatorFactory(self, ) -> Function:
    """Creates a factory, which in turn creates instances of source class."""

    def createInstance() -> object:
      """Creator function"""
      return self.getSourceClass()()

    return createInstance

  def __call__(self, cls: type) -> object:
    """When an instance decorates a class, it invokes this method"""
    if self.getSourceClass() is not None:
      raise TypeError
    self.setSourceClass(cls)
    return self

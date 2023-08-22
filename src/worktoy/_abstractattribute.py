"""AbstractAttribute provides a base class for implementation of
attributes. This is particularly convenient along with the custom a custom
metaclass"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod

from worktoy import MetaAttribute, DefaultClass


class AbstractAttribute(DefaultClass, metaclass=MetaAttribute):
  """Abstract implementation of descriptors. """

  def __init__(self, *args, **kwargs) -> None:
    self._name = None
    self._owner = None

  def _getAttributeName(self) -> str:
    """Getter-function for the name under which the value is placed on the
    owner class. """
    if self._name is None or not isinstance(self._name, str):
      raise TypeError
    return '__%s_value__' % self._name

  @abstractmethod
  def _getDefaultValue(self, cls: type) -> object:
    """Getter-function for the default value. Subclasses must implement
    this method. """

  def _getOwner(self) -> type:
    """Getter-function for the owner class"""
    if self._owner is None:
      raise TypeError
    return self._owner

  def _getName(self, ) -> str:
    """Getter-function for the name of the attribute instance set by the
    __set_name__."""
    return self._name

  def __set_name__(self, cls: type, name: str) -> None:
    """This method runs when an instance of this class is created and set
    on the class body"""
    self._name = name
    self._cls = cls
    key = self._getAttributeName()
    defVal = self._getDefaultValue(cls)
    setattr(cls, key, defVal)

  def __get__(self, obj: object, cls: type) -> object:
    """Returns the name"""
    val = self._explicitGetter(obj, cls)
    return self._typeGuard(val)

  def __set__(self, obj: object, newValue: object) -> None:
    """Sets the name"""
    self._explicitSetter(obj, self._typeGuard(newValue))

  def __delete__(self, obj: object) -> None:
    """Not implemented"""
    return self._explicitDeleter(obj)

  def _explicitGetter(self, obj: object, cls: type) -> object:
    """Explicit getter function.
    Subclasses can reimplement this method along with the explicit getter
    and setter for convenient and flexible customization of descriptor
    behaviour"""
    if self._getOwner() != cls:
      raise TypeError
    return getattr(obj, self._getAttributeName(), None)

  def _explicitSetter(self, obj: object, newValue: object) -> None:
    """Explicit setter function"""
    setattr(obj, self._getAttributeName(), newValue)

  def _explicitDeleter(self, obj: object) -> None:
    """Explicit deleter function"""
    delattr(obj, self._getName())
    delattr(obj, self._getAttributeName())

  @abstractmethod
  def _getType(self, ) -> type:
    """Getter-function for the type supported by the attribute. Subclasses
    must implement this method. The abstract methods related to types
    should not contradict each other, although subclasses are free to do
    so."""

  @abstractmethod
  def _typeCheck(self, value: object) -> bool:
    """This method is responsible for defining whether a given object
    exactly of the type intended for this attribute class. This method
    should be used by the abstract method _typeGuard to handle objects
    based on their type. The metaclass also uses this part of the check to
    define the instancecheck method."""

  @abstractmethod
  def _typeGuard(self, value: object) -> object:
    """This method prevents the objects of unsupported types from
    interacting with the attribute. Subclasses should implement this
    method such that its implementation of _typeCheck is responsible for
    determining if the object belongs to the type supported by the
    Attribute class. Additionally, this class is responsible for any
    potential attempts at type conversion. Finally, this class is
    responsible for handling unsupported types that it fails to convert.
    The recommended approach is to raise a TypeError."""

"""AbstractAttribute provides a base class for implementation of
attributes. This is particularly convenient along with the custom a custom
metaclass"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations


class AbstractAttribute:
  """Pre attribute"""

  def __init__(self, *args, **kwargs) -> None:
    argType = [i for i in args if isinstance(i, type) or [None]][0]
    kwargType = kwargs.get('type_', None)
    type_ = kwargType or argType or None
    if type_ is None:
      defVal = [i for i in args if not isinstance(i, type) or [None]][0]
    else:
      defVal = [i for i in args if isinstance(i, argType) or [None]][0]
      if defVal is not None:
        type_ = type(defVal)
    self._valueType = type_
    self._defVal = defVal
    self._name = None
    self._owner = None

  def _getAttributeName(self) -> str:
    """Getter-function for the name under which the value is placed on the
    owner class. """
    if self._name is None or not isinstance(self._name, str):
      raise TypeError
    return '__%s_value__' % self._name

  def __set_name__(self, cls: type, name: str) -> None:
    """This method runs when an instance of this class is created and set
    on the class body"""
    self._name = name
    self._cls = cls
    setattr(cls, self._getAttributeName(), self._defVal)

  def __get__(self, obj: object, cls: type) -> object:
    """Returns the name"""
    val = getattr(obj, self._getAttributeName(), None)
    if val is None:
      return self._defVal
    if self._valueType is None:
      self._valueType = type(val)
    return self._explicitGetter(obj, cls)

  def __set__(self, obj: object, newValue: object) -> None:
    """Sets the name"""
    if self._valueType is None:
      self._valueType = type(newValue)
    if not isinstance(newValue, self._valueType):
      raise TypeError
    self._explicitSetter(obj, newValue)

  def __delete__(self, obj: object) -> None:
    """Not implemented"""
    return self._explicitDeleter(obj)

  def _explicitGetter(self, obj: object, cls: type) -> object:
    """Explicit getter function.
    Subclasses can reimplement this method along with the explicit getter
    and setter for convenient and flexible customization of descriptor
    behaviour"""
    return getattr(obj, self._getAttributeName(), None)

  def _explicitSetter(self, obj: object, newValue: object) -> None:
    """Explicit setter function"""
    setattr(obj, self._getAttributeName(), newValue)

  def _explicitDeleter(self, obj: object) -> None:
    """Explicit deleter function"""
    setattr(obj, self._getAttributeName(), None)

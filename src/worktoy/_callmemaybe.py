"""WorkToy - CallMeMaybe
This class is the baseclass for the callables in the package"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Never

from worktoy import AbstractAttribute
from worktoy._basetypes import WrapperMethod, BuiltinFunction, \
  WrapperDescriptor, Method, Function


class CallMeMaybe(AbstractAttribute):
  """WorkToy - CallMeMaybe
  This class is the baseclass for the callables in the package"""
  _callTypes = [
    Function, Method, WrapperDescriptor, WrapperMethod, BuiltinFunction
  ]

  def __init__(self, *args, **kwargs) -> None:
    self._innerMethod = None
    self._setInnerFunction(*args, **kwargs)
    AbstractAttribute.__init__(self, *args, **kwargs)

  def _getOwner(self) -> type:
    """Getter-function for the owner class"""
    return self._owner

  def _getName(self) -> str:
    """Getter-function for instance name as it appears on the owner."""
    return self._name

  def __set_name__(self, owner: type, name: str) -> None:
    self._owner = owner
    self._name = name

  def __call__(self, *args, **kwargs) -> object:
    """Invokes the function"""
    if self._innerMethod is None:
      return self._setInnerFunction(*args, **kwargs)
    return self._invokeInnerMethod(*args, **kwargs)

  def _setInnerFunction(self, *args, **kwargs) -> None:
    kwargFunc = kwargs.get('func', None)
    argFunc = [[a for a in args if callable(a)] or [None]][0]
    func = kwargFunc or argFunc or None
    if func is None:
      return
    self._innerMethod = func

  def _invokeInnerMethod(self, *args, **kwargs) -> object:
    """Invokes the inner-function"""
    if self._innerMethod is None:
      raise TypeError
    return self._innerMethod(*args, **kwargs)

  def __get__(self, obj: object, owner: type) -> Method:
    """Returns inner function invoked on obj"""
    if isinstance(self._innerMethod, staticmethod):
      return self._innerMethod

    arg = owner if isinstance(self._innerMethod, classmethod) else obj

    def func(*args, **kwargs) -> object:
      """LMAO"""
      return self._innerMethod(arg, *args, **kwargs)

    Annotations = getattr(self._innerMethod, '__annotations__', None)
    Docs = getattr(self._innerMethod, '__doc__', None)
    setattr(func, '__annotations__', Annotations)
    setattr(func, '__doc__', Docs)
    return func

  def __set__(self, *_) -> Never:
    """Illegal setter function"""
    raise TypeError

  def __delete__(self, *_) -> Never:
    raise TypeError

  def _getType(self, ) -> type:
    """Returns Function"""
    return Function

  def _typeCheck(self, value: object, ) -> object:
    """Checks if value is an instance of the class"""
    return True if isinstance(value, (*self._callTypes,)) else False

  def _typeGuard(self, value: object) -> object:
    """This implementation does not rely on the type guard"""
    return value

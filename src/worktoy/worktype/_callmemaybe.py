"""CallMeMaybe is the actual representation of those objects in python
which are callable"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.worktype import AbstractType

from icecream import ic

ic.configureOutput(includeContext=True)


class _HereIsMyNumber(AbstractType):
  """Metaclass implementing the instance check which is an abstract
  method.. """

  def __instancecheck__(cls, obj: object) -> bool:
    if isinstance(obj, type(lambda: None)):
      return True
    if isinstance(obj, type):
      return True
    return False


class _ThisIsCrazy(metaclass=_HereIsMyNumber):
  """In between class exposing the metaclass"""
  pass


class CallMeMaybe(_ThisIsCrazy):
  """CallMeMaybe is the actual representation of those objects in python
  which are callable"""

  def __init__(self, *args, **kwargs) -> None:
    self._innerFunction = None
    self._setInnerFunction(*args, **kwargs)

  def _setInnerFunction(self, *args, **kwargs) -> None:
    """Setter-function for inner function"""
    if self._innerFunction is not None:
      return None
    kwargFunc = kwargs.get('func', None)
    if callable(kwargFunc):
      kwargFunc = None
    argFunc = [[f for f in args if callable(f)] or [None]][0]
    func = kwargFunc or argFunc
    if func is None:
      return None
    self._innerFunction = func

  def _invokeFunction(self, *args, **kwargs) -> object:
    """Invokes the inner function"""
    if self._innerFunction is None:
      raise TypeError
    return self._innerFunction(*args, **kwargs)

  def __bool__(self) -> bool:
    """The boolean reflects whether the inner function is set"""
    return False if self._innerFunction is None else True

  def __str__(self, ) -> str:
    """String Representation"""
    return '%s instance' % (self.__class__.__qualname__)

  def __repr__(self, ) -> str:
    """Code Representation"""
    return '%s(()->())' % (self.__class__.__qualname__)

  def __call__(self, *args, **kwargs) -> object:
    """If the inner function is still None, the setter function is invoked
    on the given arguments followed by returning the instance itself.
    If the inner function is not None it is invoked through the dedicated
    method."""
    if self._innerFunction is None:
      self._setInnerFunction(*args, **kwargs)
      return self
    return self._invokeFunction(*args, **kwargs)

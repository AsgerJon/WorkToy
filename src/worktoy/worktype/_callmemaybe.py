"""CallMeMaybe is the actual representation of those objects in python
which are callable"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.worktype import AbstractType


class _HereIsMyNumber(AbstractType):
  """Meta implementation providing instancecheck. """

  def __instancecheck__(cls, obj: object) -> bool:
    if isinstance(obj, type(lambda: None)):
      return True
    if isinstance(obj, type):
      return True
    return False


class CallMeMaybe(metaclass=_HereIsMyNumber):
  """CallMeMaybe is the actual representation of those objects in python
  which are callable"""

  def __init__(self, *args, **kwargs) -> None:
    self._innerFunction = None

  def __call__(self, *args, **kwargs) -> object:
    """Calls the inner function or sets the inner function if not set"""

  def _setInnerFunction(self, *args, **kwargs) -> None:
    """Setter-function for inner function"""
    if not kwargs.get('overwrite', not self):
      raise TypeError
    self._innerFunction = [[arg for arg in args if arg in self] or [None]][0]
    if self._innerFunction is None:
      raise TypeError

  def _invokeFunction(self, *args, **kwargs) -> object:
    """Invokes the inner function"""
    if self:
      return self._innerFunction(*args, **kwargs)
    raise TypeError

  def __bool__(self) -> bool:
    """The boolean reflects whether the inner function is set"""
    return False if self._innerFunction else True

  def __str__(self, ) -> str:
    """String Representation"""
    return '%s' % self.__class__.__qualname__

  def __repr__(self, ) -> str:
    """Code Representation"""
    return '%s()' % self.__class__.__qualname__

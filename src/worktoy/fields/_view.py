"""WorkToy - Fields - View
Creates a fake field that is not reflecting an underlying variable,
but instead computes the value at call time."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import inspect
from typing import Any

from icecream import ic

from worktoy.core import Function
from worktoy.fields import AbstractField


class View(AbstractField):
  """WorkToy - Fields - View
  Creates a fake field that is not reflecting an underlying variable,
  but instead computes the value at call time."""

  def __init__(self, name: str = None, *args, **kwargs) -> None:
    AbstractField.__init__(self, None, *args, **kwargs)
    self._fieldName = None
    if isinstance(name, str):
      self._fieldName = name
    self._innerFunction = None

  def __call__(self, *args, **kwargs) -> Any:
    """Sets or invokes the inner function."""
    if self._innerFunction is None:
      if callable(args[0]):
        self._setInnerFunction(args[0])
        setattr(args[0], '__set_name__', self.__set_name__)
        return self
      raise TypeError
    return self._invokeInnerFunction(*args, **kwargs)

  def _setInnerFunction(self, func: Function) -> None:
    self._innerFunction = func
    if self._fieldName is None:
      setattr(self, '_fieldName', getattr(func, '__qualname__'))

  def _getInnerFunction(self) -> Function:
    return self._innerFunction

  def _invokeInnerFunction(self, obj: object, cls: type) -> Any:
    innerFunction = self._getInnerFunction()
    return innerFunction(obj, )

  def explicitGetter(self, obj: object, cls: type) -> Any:
    """Explicit getter function. Tries to find the _get[NAME] method on
    the object."""
    return self._invokeInnerFunction(obj, cls)

  def __set_name__(self, cls: type, name: str) -> None:
    setattr(cls, self._fieldName, self)
    return AbstractField.__set_name__(self, cls, name)

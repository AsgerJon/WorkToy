"""WorkToy - Core - FunctionDecorator
General function decorator."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from worktoy.core import Function


class FunctionDecorator:
  """WorkSide - Fields - EventHandle
  Implements recording of events on the instances allowing descriptors to
  return information based on the recorded events. """

  def __init__(self, *args, **kwargs) -> None:
    self._innerFunction = None

  def __call__(self, *args, **kwargs) -> Any:
    """Calls the inner function if present or sets inner function."""
    if self._innerFunction is None:
      func = (*args,) or (None,)[0]
      if func is None:
        from worktoy.waitaminute import UnexpectedStateError
        raise UnexpectedStateError('func')
      if not isinstance(func, Function):
        from worktoy.waitaminute import TypeSupportError
        expected = Function
        actual = self._innerFunction
        raise TypeSupportError(expected, actual, 'func')
      return self.setInnerFunction(func)
    return self.invokeInnerFunction(*args, **kwargs)

  def setInnerFunction(self, func: Function) -> None:
    """Setter-function for the inner function"""
    self._innerFunction = func

  def getInnerFunction(self, *args, **kwargs) -> Function:
    """Getter-function for the inner function."""
    name = '_innerFunction'
    if self._innerFunction is None:
      from worktoy.waitaminute import UnexpectedStateError
      raise UnexpectedStateError(name)
    if not isinstance(self._innerFunction, Function):
      from worktoy.waitaminute import TypeSupportError
      expected = Function
      actual = self._innerFunction
      raise TypeSupportError(expected, actual, name)
    return self._innerFunction

  def invokeInnerFunction(self, *args, **kwargs) -> Any:
    """Invokes the inner function."""
    func = self.getInnerFunction()
    return func(*args, **kwargs)

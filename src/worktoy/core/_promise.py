"""WorkToy - Core - Promise
Defines a deferred function call along with arguments."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from types import MethodType

from worktoy.core import Function


class Promise:
  """WorkToy - Core - Promise
  Defines a deferred function call along with arguments."""

  def __init__(self, func: Function, *args, **kwargs) -> None:
    if isinstance(func, MethodType):
      func = func.__func__
    self._func = func
    self._args = args
    self._kwargs = kwargs

  def __call__(self, *args, **kwargs) -> object:
    """Invokes the underlying function."""
    return self._func(*self._args, **self._kwargs)

  def __eq__(self, other: object) -> bool:
    """If 'other' is a Promise, function and arguments must be the same.
    If 'other' is a function, then it compares with the function on the
    promise. """
    if isinstance(other, Function):
      return self._func == other
    if isinstance(other, MethodType):
      return self == other.__func__
    if isinstance(other, Promise):
      return self == other._func
    return NotImplemented

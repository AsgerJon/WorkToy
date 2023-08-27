"""WorkToy - Core - CallMeMaybe
Descriptor class for callables"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core import Function
from worktoy.fields import AbstractDescriptor


class CallMeMaybe(AbstractDescriptor):
  """WorkToy - Core - CallMeMaybe
  Descriptor class for callables"""

  def __init__(self, func: Function = None, *args, **kwargs) -> None:
    AbstractDescriptor.__init__(self, *args, **kwargs)
    self._innerFunc = func
    self._innerFuncArg = None
    self._valueType = Function

  def __call__(self, *args, **kwargs) -> object:
    """Function should be set by the __init__ method."""
    if self._innerFunc is None:
      self._innerFunc = args[0]
      return self
    this = self._innerFunc
    instance = self._innerFuncArg
    return this(instance, this, *args, **kwargs)

  def explicitGetter(self, obj: object, cls: type) -> object:
    """Explicit Getter"""
    self._innerFuncArg = obj
    return self


CALL = CallMeMaybe

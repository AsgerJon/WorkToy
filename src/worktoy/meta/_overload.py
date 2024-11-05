"""Overload encapsulates type signature to function mapping. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.parse import maybe
from worktoy.text import typeMsg

try:
  from typing import TYPE_CHECKING, Callable, Any
except ImportError:
  TYPE_CHECKING = False
  Callable = object
  Any = object

if TYPE_CHECKING:
  RawSigs = list[list[type]]
else:
  RawSigs = object


class Overload:
  """Overload encapsulates type signature to function mapping. """

  __type_signature__ = None
  __wrapped_function__ = None
  __class_method_flag__ = None

  def setTypeSignature(self, *types: type) -> None:
    """Setter-function for the type signature."""
    if self.__type_signature__ is not None:
      e = """The type signature is already set."""
      raise TypeError(e)
    self.__type_signature__ = types

  def getTypeSignature(self, ) -> RawSigs:
    """Getter-function for the type signature."""
    if self.__type_signature__ is None:
      e = """The type signature is not set."""
      raise TypeError(e)
    return self.__type_signature__

  def getWrappedFunction(self, ) -> callable:
    """Getter-function for the wrapped function."""
    if self.__wrapped_function__ is None:
      e = """The wrapped function is not set."""
      raise TypeError(e)
    return self.__wrapped_function__

  def setWrappedFunction(self, wrappedFunction: Callable) -> Callable:
    """Setter-function for the wrapped function."""
    if self.__wrapped_function__ is not None:
      e = """The wrapped function is already set."""
      raise TypeError(e)
    if not callable(wrappedFunction):
      e = """The wrapped function must be callable."""
      raise TypeError(e)
    self.__wrapped_function__ = wrappedFunction
    return wrappedFunction

  def __init__(self, *types: type) -> None:
    self.setTypeSignature(*types)

  def __call__(self, target: Any) -> Any:
    """Decorates target"""
    if isinstance(target, classmethod):
      e = """This version does not implement overload support for 
      classmethods!"""
      raise NotImplementedError(e)
    self.setWrappedFunction(target)
    return self

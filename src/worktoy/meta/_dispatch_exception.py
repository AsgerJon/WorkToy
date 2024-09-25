"""DispatchException provides a custom exception raised when an instance
of OverloadDispatcher fails to resolve the correct function from the
given arguments. Because the overload protocol relies on type matching,
this exception subclasses TypeError such that it can be caught by external
error handlers. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.text import monoSpace

try:
  from typing import TYPE_CHECKING
except ImportError:
  TYPE_CHECKING = False

if TYPE_CHECKING:
  from worktoy.meta import Overload


class DispatchException(TypeError):
  """DispatchException provides a custom exception raised when an instance
  of OverloadDispatcher fails to resolve the correct function from the
  given arguments. """

  __overload_function__ = None
  __pos_args__ = None

  def __init__(self, func: Overload, *args) -> None:
    e = """When calling the overloaded function '%s' the dispatcher could 
    not resolve the correct function from the given arguments: %s!"""
    self.__overload_function__ = func
    self.__pos_args__ = [*args, ]
    argStr = ["""  '%s' of type '%s'""" % (arg, type(arg)) for arg in args]
    argStr = ',\n'.join(argStr)
    errorMsg = monoSpace(e % (func.__function_name__, argStr))
    TypeError.__init__(self, errorMsg)

  def getOverload(self) -> Overload:
    """Return the Overload instance."""
    return self.__overload_function__

  def getArgs(self) -> list:
    """Return the arguments causing the exception."""
    return self.__pos_args__

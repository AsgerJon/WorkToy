"""
_CallMeMaybe encapsulates function decoration.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from types import FunctionType as Func

from ..parse import maybe
from ..static import AbstractObject
from ..waitaminute import MissingVariable, TypeException

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any


class _CallMeMaybe(AbstractObject):
  """_CallMeMaybe encapsulates function decoration."""

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Fallback variables
  __fallback_wrapper__ = lambda hereIsMyNumber: hereIsMyNumber

  #  Private variables
  __wrapper__ = None  # The function that will actually decorate
  __wrapped__ = None  # The function that is wrapped by the decorator

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _getWrapper(self, ) -> Func:
    """
    Getter-function for the wrapper function.
    """
    return maybe(self.__wrapper__, self.__fallback_wrapper__)

  def _getWrapped(self) -> Func:
    """
    Getter-function for the wrapped function.
    """
    if self.__wrapped__ is None:
      raise MissingVariable('wrapped', Func)
    return self.__wrapped__

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, wrapperFunction: Func) -> None:
    """Initialize the CallMeMaybe object."""
    if not isinstance(wrapperFunction, Func):
      raise TypeException('wrapper', wrapperFunction, Func)
    self.__wrapper__ = wrapperFunction

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __call__(self, *args, **kwargs) -> Any:
    """Call the wrapped function with the given arguments."""
    try:
      wrapped = self._getWrapped()
    except MissingVariable as mv:
      if len(args) == 1 and not kwargs:
        if isinstance(args[0], Func):
          self.__wrapped__ = args[0]
          return self
      raise mv
    else:
      return wrapped(*args, **kwargs)
    finally:
      pass

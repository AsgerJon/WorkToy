"""Instances of Abstract indicate objects that are expected, but yet to be
implemented. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.text import monoSpace, funcReport

try:
  from typing import Self
except ImportError:
  Self = object

try:
  from typing import TYPE_CHECKING
except ImportError:
  TYPE_CHECKING = False

if TYPE_CHECKING:
  from depr.meta import CallMeMaybe


class Abstract:
  """Instances of Abstract decorates methods in classes that require an
  implementation in a subclass. """

  __field_name__ = None
  __field_owner__ = None
  __wrapped__ = None

  def __set_name__(self, owner: type, name: str) -> None:
    """Set the name of the field and the owner of the field."""
    self.__field_name__ = name
    self.__field_owner__ = owner

  def __call__(self, callMeMaybe: CallMeMaybe) -> Self:
    """Set the function as the callable for the type signature. """
    if self.__wrapped__ is not None:
      e = """Decorator received a second function!"""
      raise AttributeError(e)
    self.__wrapped__ = callMeMaybe
    return self

  def getWrappedFunction(self, ) -> CallMeMaybe:
    """Getter-function for the wrapped function."""
    if self.__wrapped__ is None:
      e = """The wrapped function is not set!"""
      raise AttributeError(monoSpace(e))
    return self.__wrapped__

  def __str__(self, ) -> str:
    """Return a string representation of the object."""
    #  Base data
    return funcReport(self.__wrapped__)


abstract = Abstract()

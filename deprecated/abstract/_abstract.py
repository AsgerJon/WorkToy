"""Instances of Abstract indicate objects that are expected, but yet to be
implemented. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.text import monoSpace, funcReport

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Self
  from worktoy.mcls import CallMeMaybe


class Abstract:
  """Instances of Abstract decorates methods in classes that require an
  implementation in a subclass. """

  __field_name__ = None
  __field_owner__ = None
  __wrapped_function__ = None

  def __init__(self, func: CallMeMaybe) -> None:
    """Initialize the Abstract object."""
    self.__wrapped_function__ = func

  def __set_name__(self, owner: type, name: str) -> None:
    """Set the name of the field and the owner of the field."""
    self.__field_name__ = name
    self.__field_owner__ = owner


def abstract(callMeMaybe: CallMeMaybe) -> Abstract:
  """Decorator for abstract methods. """
  return Abstract(callMeMaybe)

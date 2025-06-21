"""
Cast provides casting from any number of positional arguments to one
target type.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.static import AbstractObject, _Attribute

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Callable, Any


class Cast(AbstractObject):
  """Cast provides casting from any number of positional arguments to one
  target type."""

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __target_type__ = None

  #  Public Variables
  target = _Attribute()  # No default target

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, *args, ) -> None:
    """
    Initialize the Cast instance with a target type.
    """
    for arg in args:
      if isinstance(arg, type):
        self.__target_type__ = arg
        break
    else:
      raise NotImplementedError('missing argument for target type')

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _instantiateTarget(self, *args, ) -> Any:  # target
    """
    Instantiate the target type with the given arguments.
    """
    return self.target(*args, )

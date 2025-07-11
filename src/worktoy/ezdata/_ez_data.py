"""
EZData leverages the 'worktoy' library to provide a dataclass.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, Iterator

from . import EZMeta
from ..mcls import BaseObject

if TYPE_CHECKING:  # pragma: no cover
  from typing import Callable


def _root(callMeMaybe: Callable) -> Callable:
  """
  _root is a decorator that ensures the decorated function is called
  with the root class of EZData.
  """

  setattr(callMeMaybe, '__is_root__', True)
  return callMeMaybe


class EZData(BaseObject, metaclass=EZMeta):
  """
  EZData is a dataclass that provides a simple way to define data
  structures with validation and serialization capabilities.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @_root
  def __init__(self, *args, **kwargs) -> None:
    """This is just here for type checking purposes. The EZMeta control
    flow removes it with the auto-generated __init__ method."""

  @_root
  def __iter__(self, ) -> Iterator:
    """See documentation for __init__ above."""

  @_root
  def __setitem__(self, *_) -> None:
    """See documentation for __init__ above."""

  @_root
  def __getitem__(self, *_) -> None:
    """See documentation for __init__ above."""

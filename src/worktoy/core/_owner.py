"""
OWNER provides a descriptor class for the contextual owner of an 'Object'
object.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover'
  from typing import Any, TypeVar, Callable


class ContextOwner:
  """
  OWNER provides a descriptor class for the contextual owner of an 'Object'
  object.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __get__(self, instance: Any, owner: type) -> Any:
    """Returns the owner of the 'Object' instance. """
    if instance is None:
      return self
    return owner

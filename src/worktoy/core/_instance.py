"""INSTANCE provides the contextual instance of an 'Object' object."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, TypeVar, Callable


class ContextInstance:
  """INSTANCE provides the contextual instance of an 'Object' object."""

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __get__(self, instance: Any, owner: type) -> Any:
    """Returns the instance of the 'Object' instance."""
    if instance is None:
      return self
    if TYPE_CHECKING:  # pragma: no cover
      from worktoy.core import Object
      assert isinstance(instance, Object)
    contextInstance = instance.getContextInstance()
    if contextInstance is None:  # must resolve next level up
      raise NotImplementedError
    return contextInstance

"""
'ContextInstance' and 'ContextOwner' back 'Object.instance' and
'Object.owner', returning the active value from the descriptor context.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class ContextInstance:
  """Descriptor that returns the currently active instance.

  When accessed on a class, returns the descriptor itself. When
  accessed on an 'Object' instance, returns the top-of-stack
  instance via 'Object.getContextInstance'. Raises
  'WithoutException' if no context frame is active.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __get__(self, instance: Any, owner: type) -> Any:
    """Return 'self' on class access; delegate to
    'instance.getContextInstance' on instance access."""
    if instance is None:
      return self
    return instance.getContextInstance()


class ContextOwner:
  """Descriptor that returns the currently active owner class.

  When accessed on a class, returns the descriptor itself. When
  accessed on an 'Object' instance, returns the top-of-stack owner
  via 'Object.getContextOwner'. Raises 'WithoutException' if no
  context frame is active.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __get__(self, instance: Any, owner: type) -> Any:
    """Return 'self' on class access; delegate to
    'instance.getContextOwner' on instance access."""
    if instance is None:
      return self
    return instance.getContextOwner()

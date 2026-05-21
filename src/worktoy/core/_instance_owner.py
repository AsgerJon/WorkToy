"""
'ContextInstance' and 'ContextOwner' are the two descriptors that
back 'Object.instance' and 'Object.owner'. Each one delegates to the
descriptor's context stack (managed by 'Object.createContext' /
'Object.exitContext') and returns the currently active value, or
raises 'WithoutException' if no context frame is on the stack.

They are intentionally minimal: each defines only '__get__'. Writes
to 'self.instance' or 'self.owner' from inside an '__instance_*'
hook are not supported.
"""
#  AGPL-3.0 license
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

"""
ContextCaller provides a descriptor class for the contextual caller.
Instead of using 'self.instance.foo' in context-only methods,
use 'self.caller.foo'.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, TypeVar, Callable, Self


class ContextCaller:
  """
  ContextCaller provides a descriptor class for the contextual caller.
  Instead of using 'self.instance.foo' in context-only methods,
  use 'self.caller.foo'.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __get__(self, instance: Any, owner: type) -> Any:
    """Returns the caller """
    if instance is None:
      return self
    out = getattr(instance, '__context_caller__', )
    if out is None:
      raise RuntimeError

"""
Root resolves the top-level instance in a system of nested descriptors.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.core import Object

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Callable, Self


class Root(Object):
  """
  Descriptor that resolves the root instance in a chain of nested
  descriptors.

  Standard descriptors receive the immediate parent object as the
  `instance` in their `__get__`, `__set__`, and `__delete__` methods.
  When descriptors are nested — for example, when a descriptor is
  defined on another descriptor-backed object — the `instance` becomes
  the containing descriptor, not the outermost owner.

  This descriptor retrieves and caches the *true root instance*, i.e.,
  the non-descriptor object that initiated the attribute access.

  Example:

    class RGB:
      root = Root()

    class Brush:
      color = RGB()

    class Painter:
      brush = Brush()

    painter = Painter()
    painter.brush.color.root  # Returns the `Painter` instance.

  This is useful for nested descriptors that require context from the
  top-level instance in order to resolve attribute names, per-instance
  state, or other root-level metadata.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __get__(self, instance: Any, owner: type) -> Self:
    """
    Returns the root instance of the descriptor chain.
    If `instance` is None, returns the descriptor itself.
    """
    if instance is None:
      return self
    return getattr(instance, 'root', self)

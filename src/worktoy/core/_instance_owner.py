"""
'ContextInstance' and 'ContextOwner' back 'Object.instance' and
'Object.owner', returning the active value from the descriptor context.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any


class ContextInstance:
  """
  Inside the hooks of a descriptor based on 'Object', 'self.instance'
  must give the instance of the access in progress, the object the
  attribute is read from, written to or deleted from. The same name read
  through the class must give something harmless, and the descriptor
  machinery must never depend on it, since a subclass may shadow it.

  Implementation
  --------------

  Through the class, the descriptor returns itself. Through an 'Object',
  it returns 'getContextInstance()', which reads the top frame of the
  context stack, and fails outside an access as that method describes.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __get__(self, instance: Any, owner: type) -> Any:
    if instance is None:
      return self
    return instance.getContextInstance()


class ContextOwner:
  """
  Inside the hooks of a descriptor based on 'Object', 'self.owner' must
  give the owning class of the access in progress.

  Implementation
  --------------

  Through the class, the descriptor returns itself. Through an 'Object',
  it returns 'getContextOwner()', which reads the top frame of the
  context stack, and fails outside an access as that method describes.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __get__(self, instance: Any, owner: type) -> Any:
    if instance is None:
      return self
    return instance.getContextOwner()

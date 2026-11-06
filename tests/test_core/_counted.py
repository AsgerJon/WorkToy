"""
Counted is the descriptor of the 'Object' docstring, keeping a count on
each instance.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.core import Object
from worktoy.core.sentinels import DELETED

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any


class Counted(Object):
  """
  A descriptor on 'Object' defines a read, a write and a deletion in one
  method each and leaves the frames and hooks to the base. 'Counted' is
  the example of the 'Object' docstring: the value lives in '_count' on
  the instance, zero until written, and a deletion leaves 'DELETED'
  there so the next read fails as a deleted attribute does.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __instance_get__(self, instance: Any, owner: type, **kw) -> Any:
    return getattr(instance, '_count', 0)

  def __instance_set__(self, instance: Any, value: Any, **kw) -> None:
    instance._count = value

  def __instance_delete__(
      self, instance: Any, old: Any = None, **kw) -> None:
    instance._count = DELETED

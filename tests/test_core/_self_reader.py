"""
SelfReader is a descriptor whose 'hookOnGet' reads its own field again.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.core import Object

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any


class SelfReader(Object):
  """
  A read hook reading the field it belongs to, as an 'onGet' comparing
  the field with the value it was handed, would run itself again without
  end. 'Object' refuses such a read with 'RecursiveRead' at the line
  making it. 'SelfReader' makes that read from 'hookOnGet'.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __instance_get__(self, instance: Any, owner: type, **kw) -> Any:
    return 1

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NOTIFIERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def hookOnGet(self, instance: Any, value: Any, **kw) -> None:
    getattr(instance, self.getFieldName())

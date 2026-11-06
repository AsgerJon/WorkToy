"""
EarlyReader is a descriptor whose 'hookPreGet' reads its own field.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.core import Object

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any


class EarlyReader(Object):
  """
  The refusal of a read made from a read hook names the hook that runs,
  'preGet' or 'onGet'. 'EarlyReader' makes the read from 'hookPreGet',
  so the refusal is seen to name that phase, and the read never gets as
  far as a value.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NOTIFIERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def hookPreGet(self, instance: Any, **kw) -> None:
    getattr(instance, self.getFieldName())

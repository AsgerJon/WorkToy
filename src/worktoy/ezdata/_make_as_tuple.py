"""``makeAsTuple`` returns a closure that returns the field
values as a ``tuple``."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ._ez_slot import EZSlot

if TYPE_CHECKING:  # pragma: no cover
  from typing import Callable, List, Tuple


def makeAsTuple(fields: List[EZSlot]) -> Callable:
  """Build ``asTuple`` returning the field values as a tuple."""
  fieldNames = tuple(f.name for f in fields)

  def asTuple(self) -> Tuple:
    return tuple(getattr(self, n) for n in fieldNames)

  return asTuple

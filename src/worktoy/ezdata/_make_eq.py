"""``makeEq`` returns the auto-generated ``__eq__`` closure."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ._ez_slot import EZSlot

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Callable, List


def makeEq(fields: List[EZSlot]) -> Callable:
  """Build ``__eq__`` that compares field-by-field with strict typing."""
  fieldNames = tuple(f.name for f in fields)

  def __eq__(self, other: Any) -> bool:
    if type(self) is not type(other):
      return NotImplemented
    for name in fieldNames:
      if getattr(self, name) != getattr(other, name):
        return False
    return True

  return __eq__

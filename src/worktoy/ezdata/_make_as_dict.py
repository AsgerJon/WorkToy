"""``makeAsDict`` returns a closure that returns the field
values as a ``dict``."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ._ez_slot import EZSlot

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Callable, Dict, List


def makeAsDict(fields: List[EZSlot]) -> Callable:
  """Build ``asDict`` returning the field values as a dict."""
  fieldNames = tuple(f.name for f in fields)

  def asDict(self) -> Dict[str, Any]:
    return {n: getattr(self, n) for n in fieldNames}

  return asDict

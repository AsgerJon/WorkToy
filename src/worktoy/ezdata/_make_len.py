"""``makeLen`` returns a closure returning the number of fields."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ._ez_slot import EZSlot

if TYPE_CHECKING:  # pragma: no cover
  from typing import Callable, List


def makeLen(fields: List[EZSlot]) -> Callable:
  """Build ``__len__`` returning the number of fields."""
  count = len(fields)

  def __len__(self) -> int:
    return count

  return __len__

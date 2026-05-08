"""``makeIter`` returns a closure yielding field values in
declaration order."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ._ez_slot import EZSlot

if TYPE_CHECKING:  # pragma: no cover
  from typing import Callable, Iterator, List


def makeIter(fields: List[EZSlot]) -> Callable:
  """Build ``__iter__`` yielding field values in declaration order."""
  fieldNames = tuple(f.name for f in fields)

  def __iter__(self) -> Iterator:
    for name in fieldNames:
      yield getattr(self, name)

  return __iter__

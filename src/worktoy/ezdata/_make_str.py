"""``makeStr`` returns a positional-style ``__str__`` closure."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ._ez_slot import EZSlot

if TYPE_CHECKING:  # pragma: no cover
  from typing import Callable, List


def makeStr(fields: List[EZSlot]) -> Callable:
  """Build a positional ``__str__``: ``ClassName(v1, v2, v3)``."""
  fieldNames = tuple(f.name for f in fields)

  def __str__(self) -> str:
    parts = [str(getattr(self, n)) for n in fieldNames]
    return '%s(%s)' % (type(self).__name__, ', '.join(parts))

  return __str__

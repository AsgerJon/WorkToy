"""``makeHash`` returns the auto-generated ``__hash__`` closure;
frozen classes hash their value tuple, others raise on call."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..waitaminute.ez import UnfrozenHashException
from ._ez_slot import EZSlot

if TYPE_CHECKING:  # pragma: no cover
  from typing import Callable, List


def makeHash(fields: List[EZSlot], frozen: bool) -> Callable:
  """Build ``__hash__``.

  - Frozen classes hash the tuple of field values.
  - Unfrozen classes raise ``UnfrozenHashException`` on call.
  """
  fieldNames = tuple(f.name for f in fields)

  if frozen:
    def __hash__(self) -> int:
      return hash(tuple(getattr(self, n) for n in fieldNames))
    return __hash__

  def __hash__(self) -> int:
    raise UnfrozenHashException(type(self).__name__)
  return __hash__

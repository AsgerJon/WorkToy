"""``validateOrderable`` checks that every default value of an
``order=True`` class supports the ``<`` operator."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..waitaminute.ez import UnorderedEZException
from ._ez_slot import EZSlot

if TYPE_CHECKING:  # pragma: no cover
  from typing import List


def validateOrderable(fields: List[EZSlot], className: str) -> None:
  """Raise ``UnorderedEZException`` if any default is not orderable.

  Tries ``val < val`` on each non-``None`` default. Catches
  ``TypeError`` (the standard "not supported between instances
  of" case) and re-raises as ``UnorderedEZException``. Any other
  exception class propagates unchanged.
  """
  for slot in fields:
    val = slot.defaultValue
    if val is None:
      continue
    try:
      _ = val < val
    except TypeError:
      raise UnorderedEZException(
          className, slot.name, slot.typeValue)

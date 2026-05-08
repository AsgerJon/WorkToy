"""``makeGetItem`` returns the auto-generated ``__getitem__``
closure supporting int, str, and slice keys."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..waitaminute import TypeException
from ._ez_slot import EZSlot
from ._wrap_index import wrapIndex

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Callable, List


def makeGetItem(fields: List[EZSlot]) -> Callable:
  """Build ``__getitem__`` supporting int, str, and slice keys."""
  fieldNames = tuple(f.name for f in fields)

  def __getitem__(self, key: Any) -> Any:
    if isinstance(key, int):
      idx = wrapIndex(key, len(fieldNames))
      return getattr(self, fieldNames[idx])
    if isinstance(key, str):
      if key in fieldNames:
        return getattr(self, key)
      raise KeyError(key)
    if isinstance(key, slice):
      return tuple(getattr(self, n) for n in fieldNames[key])
    raise TypeException('key', key, int, str, slice)

  return __getitem__

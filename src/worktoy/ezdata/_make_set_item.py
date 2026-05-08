"""``makeSetItem`` returns the auto-generated ``__setitem__``
closure mirroring ``__getitem__``'s key handling, with extra
slice-write rules."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..utilities import textFmt
from ..waitaminute import TypeException
from ._ez_slot import EZSlot
from ._wrap_index import wrapIndex

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Callable, List


def makeSetItem(fields: List[EZSlot]) -> Callable:
  """Build ``__setitem__`` mirroring ``__getitem__``'s key handling."""
  fieldNames = tuple(f.name for f in fields)

  def __setitem__(self, key: Any, value: Any) -> None:
    if isinstance(key, int):
      idx = wrapIndex(key, len(fieldNames))
      setattr(self, fieldNames[idx], value)
      return
    if isinstance(key, str):
      if key in fieldNames:
        setattr(self, key, value)
        return
      raise KeyError(key)
    if isinstance(key, slice):
      if isinstance(value, str):
        info = """Tried setting slice: 'self[%s]' to a 'str' object:
        '%s'. Because this is nearly always not meant to be taken as
        an iterable of characters, 'EZData' does not allow this
        despite the fact that Python technically does. Please note
        that this prohibition applies only to 'str' not to 'bytes'
        or 'bytearray'."""
        raise TypeError(textFmt(info % (key, value)))
      sliceSlots = fieldNames[key]
      values = tuple(value)
      if len(sliceSlots) != len(values):
        info = """Slice '%s' of '%s' with %d slots cannot be set to
        value of length %d!""" % (
            key, type(self).__name__, len(fieldNames), len(values))
        raise IndexError(textFmt(info))
      for n, v in zip(sliceSlots, values):
        setattr(self, n, v)
      return
    raise TypeException('key', key, int, str, slice)

  return __setitem__

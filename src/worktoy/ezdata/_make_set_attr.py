"""``makeSetAttr`` returns the auto-generated ``__setattr__``
closure; behavior depends on ``frozen``."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..utilities import textFmt
from ..waitaminute.ez import FrozenEZException
from ._coerce_attr import coerceAttr
from ._ez_slot import EZSlot

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Callable, List


def makeSetAttr(fields: List[EZSlot], frozen: bool) -> Callable:
  """Build ``__setattr__``.

  Always validates the key against ``__slots__`` and coerces the
  value to the slot's declared type. When ``frozen`` is true and
  the instance has been initialized (``__ez_initialized__`` set),
  any write raises ``FrozenEZException``.
  """
  fieldNames = frozenset(f.name for f in fields)
  fieldTypes = {f.name: f.typeValue for f in fields}

  if frozen:
    def __setattr__(self, key: str, value: Any) -> None:
      if key == '__ez_initialized__':
        object.__setattr__(self, key, value)
        return
      if key not in fieldNames:
        info = """%s has no field %r""" % (type(self).__name__, key)
        raise AttributeError(textFmt(info))
      if getattr(self, '__ez_initialized__', False):
        oldValue = getattr(self, key, None)
        raise FrozenEZException(
            key, type(self).__name__, oldValue, value)
      coerced = coerceAttr(value, fieldTypes[key])
      object.__setattr__(self, key, coerced)
    return __setattr__

  def __setattr__(self, key: str, value: Any) -> None:
    if key not in fieldNames:
      info = """%s has no field %r""" % (type(self).__name__, key)
      raise AttributeError(textFmt(info))
    coerced = coerceAttr(value, fieldTypes[key])
    object.__setattr__(self, key, coerced)
  return __setattr__

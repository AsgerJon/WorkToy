"""``makeInit`` returns the auto-generated ``__init__`` closure
used by EZData classes."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ._coerce_kwarg import coerceKwarg
from ._coerce_positional import coercePositional
from ._ez_slot import EZSlot

if TYPE_CHECKING:  # pragma: no cover
  from typing import Callable, List


def makeInit(fields: List[EZSlot], frozen: bool) -> Callable:
  """Build the auto-generated ``__init__``.

  - Defaults are written first via ``object.__setattr__`` so the
    generated ``__setattr__`` does not need to special-case the
    init phase.
  - Positional args are applied in slot order; ``None`` is
    treated as "leave the default."
  - Keyword args override; unknown names are silently dropped.
  - If ``frozen`` is true, an ``__ez_initialized__`` marker is
    set at the end so the frozen ``__setattr__`` knows to refuse
    further writes.
  """
  fieldNames = tuple(f.name for f in fields)
  fieldTypes = {f.name: f.typeValue for f in fields}
  defaults = {f.name: f.defaultValue for f in fields}

  def __init__(self, *args, **kwargs) -> None:
    for name in fieldNames:
      object.__setattr__(self, name, defaults[name])
    n = len(fieldNames)
    for i, val in enumerate(args[:n]):
      if val is None:
        continue
      name = fieldNames[i]
      coerced = coercePositional(val, fieldTypes[name])
      object.__setattr__(self, name, coerced)
    for key, val in kwargs.items():
      if key not in fieldTypes:
        continue
      coerced = coerceKwarg(val, fieldTypes[key])
      object.__setattr__(self, key, coerced)
    if frozen:
      object.__setattr__(self, '__ez_initialized__', True)

  return __init__

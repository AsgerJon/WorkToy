"""``coercePositional`` coerces a positional ``__init__`` argument
to the slot's declared type, wrapping any failure in
``TypeException``."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..waitaminute import TypeException

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


def coercePositional(value: Any, fieldType: type) -> Any:
  """Coerce a positional argument to ``fieldType``.

  ``str`` targets reject non-``str`` values directly. Other
  targets attempt ``fieldType(value)``; any failure becomes a
  ``TypeException`` chained to the original.
  """
  if isinstance(value, fieldType):
    return value
  if fieldType is str:
    raise TypeException('arg', value, fieldType)
  try:
    return fieldType(value)
  except Exception as exception:
    raise TypeException('arg', value, fieldType) from exception

"""``coerceKwarg`` coerces a keyword ``__init__`` argument, letting
the underlying coercion failure propagate unchanged."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..waitaminute import TypeException

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


def coerceKwarg(value: Any, fieldType: type) -> Any:
  """Coerce a keyword argument to ``fieldType``.

  ``str`` targets reject non-``str`` values directly. Other
  targets attempt ``fieldType(value)``; any failure propagates
  unchanged (so ``int('sixty-nine')`` surfaces as ``ValueError``).
  """
  if isinstance(value, fieldType):
    return value
  if fieldType is str:
    raise TypeException('val', value, fieldType)
  return fieldType(value)

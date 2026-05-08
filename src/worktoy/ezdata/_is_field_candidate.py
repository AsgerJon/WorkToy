"""``isFieldCandidate`` decides whether a class-body entry should
be treated as an EZData field."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


def isFieldCandidate(name: str, value: Any) -> bool:
  """Return ``True`` if a class-body entry should become a field.

  Excludes dunders, callables, and descriptors. Plain values are
  always accepted.
  """
  if name.startswith('__') and name.endswith('__'):
    return False
  if callable(value):
    return False
  if hasattr(value, '__get__'):
    return False
  if hasattr(value, '__set__'):
    return False
  return True

"""``resolveAnnotation`` resolves a class-body annotation to a
runtime ``type``, accepting either real types or PEP 563 strings."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

import builtins
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


def resolveAnnotation(annotation: Any) -> Any:
  """Resolve an annotation to a runtime ``type``, or return ``None``.

  Under ``from __future__ import annotations`` (PEP 563),
  class-body annotations are stored as strings. This helper
  accepts either a type object directly, or a string naming a
  built-in type, and returns the corresponding ``type`` (or
  ``None`` if the annotation cannot be resolved).
  """
  if isinstance(annotation, type):
    return annotation
  if isinstance(annotation, str):
    candidate = getattr(builtins, annotation, None)
    if isinstance(candidate, type):
      return candidate
    if annotation == 'NoneType':
      return type(None)
  return None

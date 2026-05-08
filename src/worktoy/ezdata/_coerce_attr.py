"""``coerceAttr`` is the post-init attribute-write coercer; it has
the same semantics as ``coerceKwarg``."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ._coerce_kwarg import coerceKwarg

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


def coerceAttr(value: Any, fieldType: type) -> Any:
  """Coerce a post-init attribute write to ``fieldType``.

  Delegates to ``coerceKwarg``: ``str`` targets reject non-``str``
  values directly; other targets coerce, with any failure
  propagating unchanged.
  """
  return coerceKwarg(value, fieldType)

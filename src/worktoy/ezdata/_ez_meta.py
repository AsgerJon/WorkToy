"""``EZMeta`` is the metaclass for ``EZData`` and its subclasses."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..mcls import Base, BaseMeta
from ._ez_space import EZSpace

if TYPE_CHECKING:  # pragma: no cover
  pass


class EZMeta(BaseMeta):
  """Metaclass for ``EZData``; constructs an ``EZSpace`` namespace."""

  @classmethod
  def __prepare__(
      mcls, name: str, bases: Base, **kwargs,
  ) -> EZSpace:
    """Filter out the ``_InitSub`` shim base then build the namespace."""
    bases = tuple(b for b in bases if b.__name__ != '_InitSub')
    return EZSpace(mcls, name, bases, **kwargs)

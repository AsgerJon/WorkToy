"""``makeDelAttr`` returns a closure that always raises
``EZDeleteException``; EZData does not support attribute
deletion."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..waitaminute.ez import EZDeleteException

if TYPE_CHECKING:  # pragma: no cover
  from typing import Callable


def makeDelAttr() -> Callable:
  """Build ``__delattr__`` that always raises ``EZDeleteException``."""

  def __delattr__(self, key: str) -> None:
    raise EZDeleteException(type(self), key)

  return __delattr__

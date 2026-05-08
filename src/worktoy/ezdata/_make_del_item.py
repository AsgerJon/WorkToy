"""``makeDelItem`` returns a closure that always raises
``TypeError``; EZData does not support item deletion."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..utilities import textFmt

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Callable


def makeDelItem() -> Callable:
  """Build ``__delitem__`` that always raises ``TypeError``."""

  def __delitem__(self, key: Any) -> None:
    info = """%s does not support item deletion (received key: %r)""" % (
        type(self).__name__, key)
    raise TypeError(textFmt(info))

  return __delitem__

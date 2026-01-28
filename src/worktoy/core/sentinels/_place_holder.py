"""
PLACE_HOLDER provides a sentinel object used to indicate that a value has
not yet been set. Intended for use in 'write-once' implementations. The
sentinel object should *not* be returned from any '__get__'
implementation, instead it should use fallback, create new object or raise
'AttributeError'.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.core.sentinels import Sentinel

if TYPE_CHECKING:  # pragma: no cover
  pass


class PLACE_HOLDER(Sentinel):
  """
  PLACE_HOLDER provides a sentinel object used to indicate that a value has
  not yet been set. Intended for use in 'write-once' implementations. The
  sentinel object should *not* be returned from any '__get__'
  implementation, instead it should use fallback, create new object or raise
  'AttributeError'.
  """

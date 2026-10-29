"""
DELETED is the sentinel a descriptor stores in place of a value to mark
that value as deleted.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from . import Sentinel


class DELETED(Sentinel):
  """
  DELETED is the sentinel a descriptor stores in its backing slot to mark
  an attribute as deleted; the 'worktoy.core' base then raises
  'MissingVariable' (an 'AttributeError' subclass) on the next read
  rather than returning 'DELETED'.

  A box resolves a value from the slot on the accessing instance, and
  builds its default into that slot when it is empty. Rather than thread
  a deleted state through that, deletion stores 'DELETED' in the slot;
  the next read finds it and signals 'Object.__get__' to raise.
  """
  pass

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

  A descriptor resolves a value through up to three lookups: the value on
  the accessing instance, a default set on the descriptor object, and a
  fallback set on the descriptor class. Rather than thread deletion
  through all three, it is implemented by setting the slot to 'DELETED';
  the first lookup then finds it and signals 'Object.__get__' to raise.
  """
  pass

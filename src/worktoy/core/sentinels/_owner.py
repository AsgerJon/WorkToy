"""
OWNER provides a sentinel object used together with THIS by the descriptor
flow where OWNER provides a placeholder for the owning class, while THIS
refers to an instance of the class (self typically).
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from . import Sentinel


class OWNER(Sentinel):
  """
  OWNER is a sentinel placeholder for the owning class, the 'owner'
  argument passed to '__get__' in the descriptor protocol. In a deferred
  'AttriBox' constructor argument it is replaced at access time by that
  class, while THIS stands in for the accessing instance. Unlike THIS,
  OWNER plays no role in overload signatures.
  """

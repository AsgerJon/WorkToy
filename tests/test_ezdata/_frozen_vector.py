"""
FrozenVector is 'Vector' declared frozen, with the same fields.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from . import Vector


class FrozenVector(Vector, frozen=True):
  """
  A frozen subclass of a mutable class is allowed, keeps the
  signature of its base, and is therefore congruent with it: a
  'FrozenVector' compares equal to a 'Vector' of the same values.
  """

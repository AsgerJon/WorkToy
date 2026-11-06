"""
Vector is a mutable dataclass of two floats, the root of a lineage.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.ezdata import EZData


class Vector(EZData):
  """
  Two classes compare equal only when they are congruent: in one
  lineage and of one field-type signature. 'Vector' is the root;
  'FrozenVector' keeps its signature, 'Vector3' changes it.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Fields
  x = 0.0
  y = 0.0

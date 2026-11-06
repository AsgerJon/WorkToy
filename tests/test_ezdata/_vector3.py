"""
Vector3 is 'Vector' with a third field.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from . import Vector


class Vector3(Vector):
  """
  A subclass adding a field changes the signature and is no longer
  congruent with its base, so no 'Vector3' compares equal to a
  'Vector'. The inherited fields come first, in the order of the base.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Fields
  z = 0.0

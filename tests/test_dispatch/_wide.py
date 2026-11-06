"""
Wide is a worktoy class with a flexible declaration of four classes.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.dispatch import overload
from worktoy.mcls import BaseObject


class Wide(BaseObject):
  """
  A flexible declaration of more than three classes is registered once
  and matched by its classes in any order rather than one signature per
  order. 'Wide' declares four classes and returns them in declared order.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload.flex(str, int, float, bytes)
  def mix(self, s: str, i: int, f: float, b: bytes) -> tuple:
    return s, i, f, b

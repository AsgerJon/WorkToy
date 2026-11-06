"""
Figure is a worktoy class overloading 'scale' on an integer.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.dispatch import overload
from worktoy.mcls import BaseObject


class Figure(BaseObject):
  """
  The inheritance of overloads follows Python's lookup of the name, and
  a diamond shows where that lookup goes. 'Figure' is the ancestor both
  branches share: 'scale' takes an integer.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(int)
  def scale(self, n: int) -> tuple:
    return 'figure-int', n

"""
Square is a 'Shape' redeclaring one inherited signature and adding one.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.dispatch import overload

from . import Shape


class Square(Shape):
  """
  An equal signature declared again replaces the inherited one, a new
  signature joins the inherited ones, and the inherited 'THIS' still
  means 'Shape'. 'Square' redeclares the integer and adds a float.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(float)
  def scale(self, f: float) -> tuple:
    return 'square-float', f

  @overload(int)
  def scale(self, n: int) -> tuple:
    return 'square-int', n

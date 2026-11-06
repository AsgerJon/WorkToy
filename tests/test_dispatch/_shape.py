"""
Shape is a worktoy class overloading 'scale' on an integer and on another
shape.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core.sentinels import THIS
from worktoy.dispatch import overload
from worktoy.mcls import BaseObject


class Shape(BaseObject):
  """
  A subclass overloading a name it inherits keeps the inherited
  declarations at a greater distance. 'Shape' is the base: 'scale' takes
  an integer or another shape, the latter declared with 'THIS'.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(int)
  def scale(self, n: int) -> tuple:
    return 'shape-int', n

  @overload(THIS)
  def scale(self, other: Shape) -> tuple:
    return 'shape-this', type(other).__name__

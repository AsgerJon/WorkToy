"""
Geometry is a worktoy class with aliases of a box and of three kinds of
method and an overloaded one.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox, Alias
from worktoy.dispatch import overload
from worktoy.mcls import BaseObject


class Geometry(BaseObject):
  """
  An 'Alias' gives an attribute a second name that reads, writes and
  deletes the same value, and may name a method of any kind as well.
  'Geometry' aliases its box 'width' as 'w', its method 'area' as
  'size', its staticmethod 'unit' as 'u', its classmethod 'kind' as 'k'
  and its overloaded 'scale' as 's'.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Public Variables
  width = AttriBox[int](240)

  #  Aliases
  w = Alias('width')
  size = Alias('area')
  u = Alias('unit')
  k = Alias('kind')
  s = Alias('scale')

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def area(self) -> int:
    return self.width * self.width

  @staticmethod
  def unit() -> str:
    return 'px'

  @classmethod
  def kind(cls) -> str:
    return cls.__name__

  @overload(int)
  def scale(self, n: int) -> int:
    return self.width * n

  @overload(float)
  def scale(self, f: float) -> float:
    return self.width * f

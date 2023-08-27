"""LMAO"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from _mainclass08 import Number
from worktoy.core import DefaultClass
from worktoy.fields import CLASS


class Base(DefaultClass):
  """LMAO"""

  __num__ = CLASS[Number,]

  def __init__(self, x: float = None, y: float = None) -> None:
    x, y = self.maybe(x, 0), self.maybe(y, 0)
    DefaultClass.__init__(self, x, y)
    self.__num__.__real_part__ = x
    self.__num__.__imaginary_part__ = y

  def __str__(self, ) -> str:
    return 'Number: %s' % self.__num__

  def __repr__(self, ) -> str:
    return '__repr__: %s' % self.__num__.__repr__()

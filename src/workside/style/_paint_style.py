"""WorkToy - Style - PaintStyle
Collection of settings applied to instances of QPainter. """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.base import DefaultClass


class PaintStyle(DefaultClass):
  """WorkToy - Style - PaintStyle
  Collection of settings applied to instances of QPainter. """

  def __init__(self, *args, **kwargs) -> None:
    DefaultClass.__init__(self, *args, **kwargs)

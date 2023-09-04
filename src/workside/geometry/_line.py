"""WorkSide - Geometry - Line
Representation of visual line."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from workside.geometry import Rect
from worktoy.fields import View


class Line(Rect):
  """WorkSide - Geometry - Line
  Representation of visual line."""

  __geometry_class_name__ = 'Line'

  def __init__(self, *args, **kwargs) -> None:
    Rect.__init__(self, *args, **kwargs)

  @View()
  def rect(self, ) -> Rect:
    """Returns the surrounding rectangle"""
    return Rect(self.left, self.top, self.right, self.bottom)

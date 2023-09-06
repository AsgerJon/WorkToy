"""WorkSide - Draw - Pen
Subclass of QPen"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QPen, QColor

from workside.draw import LineStyleSym, RGB
from worktoy.base import DefaultClass


class Pen(QPen, DefaultClass):
  """WorkSide - Draw - Pen
  Subclass of QPen"""

  def __init__(self, *args, **kwargs) -> None:
    DefaultClass.__init__(self, *args, **kwargs)
    QPen.__init__(self)
    lineStyle = self.maybeType(LineStyleSym, *args)
    lineStyle = self.maybe(lineStyle, LineStyleSym.solid)
    self.setStyle(lineStyle.style)
    rgbColor = self.maybeType(RGB, *args)
    col = self.maybeType(QColor, *args)
    lineColor = QColor(0, 0, 0, 255)
    if rgbColor is not None:
      lineColor = rgbColor.asQColor()
    elif col is not None:
      lineColor = col
    self.setColor(lineColor)
    width = self.maybeType(int, *args)
    width = self.maybe(width, 1)
    self.setWidth(width)

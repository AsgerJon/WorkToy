"""WorkSide - Style - Line
Representation of style settings for QPen."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QPen, QPainter

from workside.style import RGB, RGBField, PenSymField, PenSym
from worktoy.base import DefaultClass
from worktoy.fields import IntField, View


class Line(DefaultClass):
  """WorkSide - Style - PenStyle
  Representation of style settings for QPen."""

  color = RGBField(RGB.black)
  width = IntField(1)
  pen = PenSymField(0)

  @View('style')
  def getPen(self) -> QPen:
    """Getter-function for the QPen."""
    qPen = QPen()
    qPen.setWidth(self.width)
    qPen.setColor(self.color)
    qPen.setStyle(self.pen)
    return qPen

  def __matmul__(self, painter: QPainter) -> QPainter:
    """The matmul operator applies the style to the given QPainter."""
    if not isinstance(painter, QPainter):
      return NotImplemented
    painter.setPen(self.style)
    return painter


lineBase = Line()
lineBase.color = RGB.BLACK
lineBase.width = 1
lineBase.pen = PenSym.SOLID

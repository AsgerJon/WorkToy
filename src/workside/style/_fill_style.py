"""WorkSide - Style - BrushStyle
Representation of style settings for QBrush."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QPen, QBrush, QPainter

from workside.style import RGB, RGBField, PenSymField, BrushSymFill, BrushSym
from worktoy.base import DefaultClass
from worktoy.fields import IntField, View


class Fill(DefaultClass):
  """WorkSide - Style - BrushStyle
  Representation of style settings for QBrush."""

  color = RGBField(RGB.yellow)
  brush = BrushSymFill(1)

  @View('style')
  def getBrush(self) -> QBrush:
    """Getter-function for the QBrush."""
    brush = QBrush()
    brush.setColor(self.color)
    brush.setStyle(self.brush)
    return brush

  def __matmul__(self, painter: QPainter) -> QPainter:
    """The matmul operator applies the style to the given QPainter."""
    if not isinstance(painter, QPainter):
      return NotImplemented
    painter.setBrush(self.style)
    return painter


fillBase = Fill()
fillBase.color = RGB.WHITE
fillBase.brush = BrushSym.EMPTY

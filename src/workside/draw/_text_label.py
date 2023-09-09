"""WorkSide - Draw - TextLabel
Settings used to draw label."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QFont, QPen, QColor, Qt, QBrush

from workside.draw import Graphic
from worktoy.fields import Field


class TextLabel(Graphic):
  """WorkSide - Draw - TextLabel
  Settings used to draw label."""

  font = Field()
  fontPen = Field()
  boxPen = Field()
  brush = Field()

  def __init__(self, *args, **kwargs) -> None:
    Graphic.__init__(self, *args, **kwargs)

  def createFont(self, ) -> QFont:
    """Creator-function for the font."""
    fontFamily = 'Modern No. 20'
    fontPointSize = 16
    fontWeight = QFont.Weight.Normal
    font = QFont()
    font.setFamily(fontFamily)
    font.setPointSize(fontPointSize)
    font.setWeight(fontWeight)
    return font

  def createFontPen(self) -> QPen:
    """Creator-function for the QPen used to write the text."""
    penWidth = 1
    penColor = QColor(0, 0, 0, 255)
    penStyle = Qt.PenStyle.SolidLine
    pen = QPen()
    pen.setStyle(penStyle)
    pen.setColor(penColor)
    pen.setWidth(penWidth)
    return pen

  @font.getter
  def getFont(self, *args, **kwargs) -> QFont:
    """Getter-function for the font"""
    _font = getattr(self, '_font', None)
    if _font is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      _font = self.createFont()
      setattr(self, '_font', _font)
      return self.getFont(*args, _recursion=True)
    return _font

  @font.setter
  def setFont(self, font: QFont) -> None:
    """Setter-function for the font. It does not replace the existing
    variable but instead udpates its values."""
    _font = self.getFont()
    _font.setFamily(font.family())
    _font.setPointSize(font.pointSize())
    _font.setWeight(font.weight())
    setattr(self, '_font', _font)

  @fontPen.getter
  def getFontPen(self, *args, **kwargs) -> QPen:
    """Getter-function for the pen."""
    _fontPen = getattr(self, '_fontPen', None)
    if _fontPen is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      _fontPen = self.createFontPen()
      setattr(self, '_fontPen', _fontPen)
      return self.getFontPen(*args, _recursion=True)
    return _fontPen

  @fontPen.setter
  def setFontPen(self, fontPen: QPen) -> None:
    """Setter-function for the pen used to draw the text."""
    _fontPen = self.getFontPen()
    _fontPen.setWidth(fontPen.width())
    _fontPen.setColor(fontPen.color())
    _fontPen.setStyle(fontPen.style())
    setattr(self, '_fontPen', _fontPen)

  @brush.getter
  def getBrush(self, *args) -> QBrush:
    """Getter-function for the brush."""
    brushColor = QColor(127, 255, 0, 255)
    brushStyle = Qt.BrushStyle.SolidPattern
    brush = QBrush()
    brush.setColor(brushColor)
    brush.setStyle(brushStyle)
    return brush

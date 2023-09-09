"""WorkSide - Widgets - TextWidget
Implementing text labels on the paint event."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QPen, QFont, QBrush, QPaintEvent

from workside.draw import labelFontPen, subHeaderFontPen, headerFontPen
from workside.draw import subHeaderBoxPen, headerBoxPen, labelBoxPen
from workside.draw import labelFont, headerFont, subHeaderFont
from workside.draw import labelBrush, headerBrush, subHeaderBrush
from workside.widgets import CoreWidget
from worktoy.fields import Field


class TextWidget(CoreWidget):
  """WorkSide - Widgets - TextWidget
  Implementing text labels on the paint event."""

  text = Field()

  def __init__(self, text: str, *args, **kwargs) -> None:
    self._text = None
    CoreWidget.__init__(self, *args, **kwargs)
    textLevel = kwargs.get('textLevel', 'label')
    self._setTextLevel(textLevel)

  @text.getter
  def text(self, *args) -> str:
    """Getter-function for the text contained in the widget."""
    return self._text

  @text.setter
  def text(self, *args) -> None:
    """Setter-function for the text contained in the widget."""
    for arg in args:
      if isinstance(arg, str):
        self._text = arg
        break

  def _getTextLevel(self) -> str:
    return self._textLevel

  def _setTextLevel(self, textLevel: str) -> None:
    if textLevel not in self.stringList('label, header, subHeader'):
      raise ValueError
    self._textLevel = textLevel

  def getFontPen(self) -> QPen:
    """Getter-function for the font pen"""
    if self._getTextLevel() == 'label':
      return labelFontPen
    if self._getTextLevel() == 'header':
      return headerFontPen
    if self._getTextLevel() == 'subHeader':
      return subHeaderFontPen

  def getFont(self) -> QFont:
    """Getter-function for the font pen"""
    if self._getTextLevel() == 'label':
      return labelFont
    if self._getTextLevel() == 'header':
      return headerFont
    if self._getTextLevel() == 'subHeader':
      return subHeaderFont

  def getBrush(self) -> QBrush:
    """Getter-function for the font pen"""
    if self._getTextLevel() == 'label':
      return labelBrush
    if self._getTextLevel() == 'header':
      return headerBrush
    if self._getTextLevel() == 'subHeader':
      return subHeaderBrush

  def getBoxPen(self) -> QPen:
    """Getter-function for the pen used to draw the border on the text
    box."""
    if self._getTextLevel() == 'label':
      return labelBoxPen
    if self._getTextLevel() == 'header':
      return headerBoxPen
    if self._getTextLevel() == 'subHeader':
      return subHeaderBoxPen

  def getAlignmentFlags(self) -> Qt.AlignmentFlag:
    """Getter-function for the alignment flag."""
    return Qt.AlignmentFlag.AlignCenter

  def paintEvent(self, event: QPaintEvent) -> None:
    """Implementation through the WorkPainter class."""
    from workside.widgets import WorkPainter
    painter = WorkPainter()
    painter.begin(self)
    painter.fillBackground()
    painter.printText()
    painter.end()

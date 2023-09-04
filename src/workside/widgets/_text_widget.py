"""WorkSide - Style - Font
This class represents a font in the framework."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QRect, Qt, QSize
from PySide6.QtGui import QFont, QFontMetrics, QPen, QBrush, QColor, \
  QPaintEvent, QPainter
from icecream import ic

from workside.geometry import Rect, Size
from workside.settings import defaultFontSize
from workside.style import FontSizeField, RGBField, FontFamily, FontWeight, \
  fontBase, lineBase, fillBase, styleBase
from workside.widgets import CoreWidget
from worktoy.core import loremSample
from worktoy.fields import SymField, IntLabel, StrField, View

ic.configureOutput(includeContext=True)


class TextWidget(CoreWidget):
  """WorkSide - Style - Font
  This class represents a font in the framework."""

  horizontalAlign = 'left'
  verticalAlign = 'center'

  style = styleBase
  Text = StrField('LMAO')

  def getFlags(self) -> Qt.AlignmentFlag:
    """Getter-function for text flags"""
    return Qt.AlignmentFlag.AlignJustify | Qt.AlignmentFlag.AlignVCenter

  def getText(self) -> str:
    """Getter-function for formatted and filtered text."""

  @View('metrics')
  def getMetrics(self) -> QFontMetrics:
    """Getter-function for QFontMetrics"""
    return QFontMetrics(self.style.font, )

  @View('rect')
  def getRect(self, text: str = None) -> Rect:
    """GET RECT!!"""
    return Rect(self.QRect)

  @View('QRect')
  def getQRect(self, text: str = None, ) -> QRect:
    """Getter-function for the rectangle bounding the text. """
    return self.metrics.boundingRect(self.Text)

  @View('size')
  def getSize(self) -> Size:
    """Getter-function for the size of the rectangle bounding the text."""
    return self.getRect().getSize()

  def getQSize(self, text: str = None) -> QSize:
    """Getter-function for the size bounding the text."""
    return self.getQRect().size()

  def paintEvent(self, event: QPaintEvent) -> None:
    """Implementation of paint event."""
    painter = QPainter()
    painter.begin(self)

    painter.end()

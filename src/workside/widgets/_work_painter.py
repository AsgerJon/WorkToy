"""WorkSide - Widgets - WorkPainter
Custom implementation of QPainter."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtGui import QColor, QBrush
from PySide6.QtGui import QPainter, Qt, QFontMetrics, QPen
from PySide6.QtWidgets import QWidget

if TYPE_CHECKING:
  from workside.widgets import CoreWidget, TextWidget
else:
  CoreWidget, TextWidget = QWidget, QWidget

from worktoy.fields import Field


class WorkPainter(QPainter):
  """WorkSide - Widgets - WorkPainter
  Custom implementation of QPainter."""

  blankPen = Field()
  blankBrush = Field()

  @blankBrush.getter
  def getBlankBrush(self, *args) -> QBrush:
    """Getter-function for the blank brush"""
    brush = QBrush()
    brush.setStyle(Qt.BrushStyle.NoBrush)
    brush.setColor(QColor(255, 255, 255, 0))
    return brush

  @blankPen.getter
  def getBlankPen(self, *args) -> QPen:
    """Getter-function for the blank pen"""
    pen = QPen()
    pen.setStyle(Qt.PenStyle.NoPen)
    pen.setColor(QColor(255, 255, 255, 0))
    pen.setWidth(1)
    return pen

  def __init__(self, *args, **kwargs) -> None:
    QPainter.__init__(self, *args, **kwargs)
    self._widget = None

  def getActiveWidget(self) -> CoreWidget:
    """Getter-function for the widget"""
    return self._widget

  def setActiveWidget(self, widget: CoreWidget) -> None:
    """Setter-function for the widget"""
    self._widget = widget

  def clearWidget(self, ) -> None:
    """Clears the current widget."""
    self._widget = None

  def begin(self, widget: CoreWidget) -> bool:
    """Reimplementation"""
    self._widget = widget
    self.setRenderHint(QPainter.RenderHint.Antialiasing)
    return QPainter.begin(self, widget)

  def end(self) -> None:
    """Reimplementation"""
    self._widget = None
    return QPainter.end(self)

  def printText(self) -> None:
    """Prints the available text from the widget."""
    viewRect = self.viewport()
    widget = self.getActiveWidget()
    if not isinstance(widget, TextWidget):
      return
    text = widget.text
    flags = widget.getAlignmentFlags()
    font = widget.getFont()
    fontPen = widget.getFontPen()
    brush = widget.getBrush()
    boxPen = widget.getBoxPen()
    metrics = QFontMetrics(font, )
    textRect = metrics.boundingRect(viewRect, flags, text)
    self.setPen(boxPen)
    self.setBrush(brush)
    self.drawRect(textRect)
    self.setPen(fontPen)
    self.setFont(font)
    self.drawText(textRect, flags, text)

  def fillBackground(self, ) -> None:
    """Fills the background."""
    viewRect = self.viewport()
    widget = self.getActiveWidget()
    if not isinstance(widget, CoreWidget):
      return
    self.setBrush(widget.backgroundBrush)
    self.setPen(self.blankPen)
    self.drawRoundedRect(viewRect, 8, 8, )

  def outlineBackground(self) -> None:
    """Draws outline around the background."""
    viewRect = self.viewport()
    widget = self.getActiveWidget()
    if not isinstance(widget, TextWidget):
      return
    self.setBrush(widget.backgroundBrush)
    self.setPen(widget.backgroundPen)
    self.drawRoundedRect(viewRect, 8, 8, )

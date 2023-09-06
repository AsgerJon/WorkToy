"""Test"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QEvent, Qt, Signal, QPointF, QSize
from PySide6.QtGui import (QMouseEvent, QPaintEvent, QPainter, QColor,
                           QBrush, \
                           QPen)
from PySide6.QtWidgets import QLabel, QWidget
from icecream import ic

from workside.draw import RGB, Brush, Pen, FillStyleSym
from workside.widgets import CoreWidget, EventField
from worktoy.fields import AbstractField
from workside.fields import MouseMoveField


class TestWidget(CoreWidget):
  """CUNT"""

  movePos = EventField(QMouseEvent.position, QEvent.Type.MouseMove)

  def __init__(self, *args, **kwargs) -> None:
    CoreWidget.__init__(self, )
    self.setMouseTracking(True)
    self.setFixedSize(QSize(320, 240))

  def paintEvent(self, event: QPaintEvent) -> None:
    """Implementation of the painting."""
    CoreWidget.paintEvent(self, event)
    painter = QPainter()
    painter.begin(self, )
    viewRect = painter.viewport()
    pen = QPen()
    pen.setColor(QColor(0, 0, 0, 255))
    pen.setStyle(Qt.PenStyle.SolidLine)
    pen.setWidth(1)
    brush = QBrush()
    brush.setColor(QColor(255, 255, 0, 255))
    brush.setStyle(Qt.BrushStyle.SolidPattern)
    painter.setPen(pen)
    painter.setBrush(brush)
    painter.drawRect(viewRect, )
    flag = Qt.AlignmentFlag.AlignCenter
    text = 'lmao'
    painter.drawText(viewRect, flag, text)
    painter.end()

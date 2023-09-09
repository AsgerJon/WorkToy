"""WorkSide - Widgets - CoreWidget
The core widget is the abstract baseclass shared by the widgets in the
WorkSide framework."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QColor, QPen
from PySide6.QtWidgets import QWidget

from worktoy.base import DefaultClass
from worktoy.fields import Field


class CoreWidget(QWidget, DefaultClass, ):
  """WorkSide - Widgets - CoreWidget
  The core widget is the abstract baseclass shared by the widgets in the
  WorkSide framework."""

  backgroundBrush = Field()
  backgroundPen = Field()

  def __init__(self, *args, **kwargs) -> None:
    self._events = {}
    DefaultClass.__init__(self, *args, **kwargs)
    parent = self.maybe(QWidget, *args)
    QWidget.__init__(self)
    self.setMouseTracking(True)

  @backgroundBrush.getter
  def getBackgroundBrush(self, *args) -> QBrush:
    """Getter-function for basic background brush."""
    _backgroundBrush = QBrush()
    _backgroundBrush.setStyle(Qt.BrushStyle.SolidPattern)
    _backgroundBrush.setColor(QColor(191, 191, 191, 255))
    return _backgroundBrush

  @backgroundPen.getter
  def getBackgroundPen(self, *args, ) -> QPen:
    """Getter-function for basic background pen."""
    _backgroundPen = QPen()
    _backgroundPen.setStyle(Qt.PenStyle.SolidLine)
    _backgroundPen.setColor(QColor(0, 0, 0, 255))
    _backgroundPen.setWidth(2)
    return _backgroundPen

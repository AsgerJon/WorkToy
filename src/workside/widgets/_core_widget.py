"""WorkSide - Widgets - CoreWidget
The core widget is the abstract baseclass shared by the widgets in the
WorkSide framework."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from workside.settings import ClickTimes
from PySide6.QtCore import QEvent
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QWidget

from workside.widgets import ButtonSym, TimedFlag
from worktoy.base import DefaultClass


class CoreWidget(QWidget, DefaultClass):
  """WorkSide - Widgets - CoreWidget
  The core widget is the abstract baseclass shared by the widgets in the
  WorkSide framework."""

  _eventHistoryLength = 8

  def __init__(self, *args, **kwargs) -> None:
    self._events = {}
    DefaultClass.__init__(self, *args, **kwargs)
    parent = self.maybe(QWidget, *args)
    QWidget.__init__(self)
    self.setMouseTracking(True)
    self._clickState = 0
    self._pressHoldTimer = TimedFlag()

  def event(self, event: QEvent) -> bool:
    """Implementation"""
    return QWidget.event(self, event)

  def mousePressEvent(self, event: QMouseEvent) -> None:
    """Implementation of mouse button functionalities."""
    if not self._clickState:  # Making this the first press
      self._clickState = 1
      self._pressHoldTimer

  def mouseReleaseEvent(self, event: QMouseEvent) -> None:
    """Implementation of mouse button functionalities."""

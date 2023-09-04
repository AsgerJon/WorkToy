"""WorkSide - Widgets - CoreWidget
Abstract baseclass for the custom widgets. """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import Any

from PySide6.QtCore import QRect, Signal
from PySide6.QtGui import QPaintEvent
from PySide6.QtWidgets import QWidget
from icecream import ic

from worktoy.base import DefaultClass

from worktoy.fields import SymField
from workside.geometry import Rect
from workside.style import AlignmentSym

ic.configureOutput(includeContext=True)


class CoreWidget(QWidget, DefaultClass):
  """WorkSide - Widgets - CoreWidget
  This class provides the baseclass for the widgets."""

  paintStart = Signal()
  paintEnd = Signal()

  def __init__(self, *args, **kwargs) -> None:
    DefaultClass.__init__(self, *args, **kwargs)
    parent = self.maybeType(QWidget, *args)
    QWidget.__init__(self, )

  def getViewport(self) -> Rect:
    """Getter-function for the viewport."""
    return Rect(self.visibleRegion().boundingRect())

  def getViewportQRect(self) -> QRect:
    """Getter-function for QRect representation of the viewport."""
    return self.visibleRegion().boundingRect()

  def paintEvent(self, event: QPaintEvent) -> None:
    """Implementation of paint event"""
    self.paintStart.emit()

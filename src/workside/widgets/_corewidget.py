"""WorkSide - Widgets - CoreWidget
Abstract baseclass for the custom widgets. """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod

from PySide6.QtCore import QRect
from PySide6.QtGui import QPaintEvent
from PySide6.QtWidgets import QWidget
from icecream import ic

from worktoy.base import DefaultClass

ic.configureOutput(includeContext=True)


class CoreWidget(QWidget, DefaultClass):
  """WorkSide - Widgets - CoreWidget
  This class provides the baseclass for the widgets."""

  def __init__(self, *args, **kwargs) -> None:
    DefaultClass.__init__(self, *args, **kwargs)
    QWidget.__init__(self, self.maybeType(QWidget, *args))

  @abstractmethod
  def sizeControl(self, ) -> None:
    """Method responsible for sizing the widget.
    Subclasses must implement this method. """

  @abstractmethod
  def alignmentControl(self) -> None:
    """Method responsible for placing the widget in its available space.
    Subclasses must implement this method."""

  def availableSpace(self) -> QRect:
    """Getter-function for the rectangle the parent layout makes available
    to this widget. """

  def resetWidgets(self) -> None:
    """Resets and creates widgets"""

  def show(self) -> None:
    """Reimplementation of the show method"""

  def paintEvent(self, event: QPaintEvent) -> None:
    """Implementation of paint event"""

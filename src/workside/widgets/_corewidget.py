"""WorkSide - Widgets - CoreWidget
Abstract baseclass for the custom widgets. """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod

from PySide6.QtCore import QRect
from PySide6.QtGui import QPaintEvent
from PySide6.QtWidgets import (QWidget, QLayout)

from worktoy import WorkThis, DefaultClass


class CoreWidget(QWidget, DefaultClass):
  """WorkSide - Widgets - CoreWidget
  This class provides the baseclass for the widgets."""

  @WorkThis()
  def getParentLayout(self, this, *args, **kwargs) -> QLayout:
    """Getter-function for the parent layout"""

  def __init__(self, *args, **kwargs) -> None:
    self._parseParent = self.parseFactory(QWidget, 'parent', 'main')
    parent = self._parseParent(*args, **kwargs)
    QWidget.__init__(self, parent)

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

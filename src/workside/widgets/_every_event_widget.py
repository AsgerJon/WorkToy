"""WorkSide - Widgets - EveryEvent
This widget lists most of the methods related to events."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QEvent, QTimerEvent
from PySide6.QtGui import (QEnterEvent, QMouseEvent, QContextMenuEvent,
                           QDragEnterEvent, QDragLeaveEvent, QDragMoveEvent,
                           QKeyEvent, QPaintEvent,
                           QShowEvent, QResizeEvent, QDropEvent, QCloseEvent,
                           QMoveEvent,
                           QWheelEvent,
                           QFocusEvent, QInputMethodEvent)
from PySide6.QtWidgets import QWidget


class EveryEvent(QWidget):
  """WorkSide - Widgets - EveryEvent
  This widget lists most of the methods related to events."""

  def enterEvent(self, event: QEnterEvent) -> None:
    """Implementation"""

  def leaveEvent(self, event: QEvent) -> None:
    """Implementation"""

  def mouseMoveEvent(self, event: QMouseEvent) -> None:
    """Implementation"""

  def mousePressEvent(self, event: QMouseEvent) -> None:
    """Implementation"""

  def mouseReleaseEvent(self, event: QMouseEvent) -> None:
    """Implementation"""

  def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
    """Implementation"""

  def contextMenuEvent(self, event: QContextMenuEvent) -> None:
    """Implementation"""

  def customEvent(self, event: QEvent) -> None:
    """Implementation"""

  def dragEnterEvent(self, event: QDragEnterEvent) -> None:
    """Implementation"""

  def dragLeaveEvent(self, event: QDragLeaveEvent) -> None:
    """Implementation"""

  def dragMoveEvent(self, event: QDragMoveEvent) -> None:
    """Implementation"""

  def keyPressEvent(self, event: QKeyEvent) -> None:
    """Implementation"""

  def keyReleaseEvent(self, event: QKeyEvent) -> None:
    """Implementation"""

  def paintEvent(self, event: QPaintEvent) -> None:
    """Implementation"""

  def showEvent(self, event: QShowEvent) -> None:
    """Implementation"""

  def resizeEvent(self, event: QResizeEvent) -> None:
    """Implementation"""

  def dropEvent(self, event: QDropEvent) -> None:
    """Implementation"""

  def closeEvent(self, event: QCloseEvent) -> None:
    """Implementation"""

  def moveEvent(self, event: QMoveEvent) -> None:
    """Implementation"""

  def wheelEvent(self, event: QWheelEvent) -> None:
    """Implementation"""

  def changeEvent(self, event: QEvent) -> None:
    """Implementation"""

  def focusInEvent(self, event: QFocusEvent) -> None:
    """Implementation"""

  def focusOutEvent(self, event: QFocusEvent) -> None:
    """Implementation"""

  def timerEvent(self, event: QTimerEvent) -> None:
    """Implementation"""

  def inputMethodEvent(self, event: QInputMethodEvent) -> None:
    """Implementation"""

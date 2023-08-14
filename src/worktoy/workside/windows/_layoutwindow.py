"""LayoutWindow subclasses BaseWindow providing the visual widgets in the
window. While this class should not provide business logic, it should
implement methods for dynamic functionalities of the widgets."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QWidget
from icecream import ic

from worktoy.workside.windows import BaseWindow

wordStart = QTextCursor.MoveOperation.StartOfWord
wordEnd = QTextCursor.MoveOperation.EndOfWord
move = QTextCursor.MoveMode.MoveAnchor
mark = QTextCursor.MoveMode.KeepAnchor

ic.configureOutput(includeContext=True)


class LayoutWindow(BaseWindow):
  """LayoutWindow subclasses BaseWindow providing the visual widgets in the
  window. While this class should not provide business logic, it should
  implement methods for dynamic functionalities of the widgets."""

  def __init__(self, parent: QWidget = None) -> None:
    BaseWindow.__init__(self, parent)

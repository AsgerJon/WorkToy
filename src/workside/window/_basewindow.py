"""WorkSide - Window - BaseWindow
Lowest window class organising menus and actions. """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QMainWindow, QWidget

from worktoy.base import DefaultClass


class BaseWindow(QMainWindow, DefaultClass):
  """WorkSide - Window - BaseWindow
  Lowest window class organising menus and actions. """

  def __init__(self, *args, **kwargs) -> None:
    DefaultClass.__init__(self, *args, **kwargs)
    parent = self.maybeType(QWidget, *args)
    QMainWindow.__init__(self, )

  def show(self) -> None:
    """Passes to super call"""
    QMainWindow.show(self)

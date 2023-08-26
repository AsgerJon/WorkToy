"""WorkSide - Window - BaseWindow
Lowest window class organising menus and actions. """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QMainWindow, QWidget

from worktoy.core import DefaultClass


class BaseWindow(QMainWindow, DefaultClass):
  """WorkSide - Window - BaseWindow
  Lowest window class organising menus and actions. """

  def parseParent(self, *args, **kwargs) -> QWidget:
    """Parses arguments to parent of type QWidget"""
    parentArg = self.maybeType(QWidget, *args)
    parentKwarg = self.parseKey('parent', 'main', **kwargs)
    parentDefault = None
    parent = self.maybe(parentKwarg, parentArg, parentDefault)
    if not isinstance(parent, QWidget):
      parent = None
    return parent

  def __init__(self, *args, **kwargs) -> None:
    DefaultClass.__init__(self, *args, **kwargs)
    QMainWindow.__init__(self, self.parseParent(*args, **kwargs))

"""WorkToy - Window - LayoutWindow
This class is responsible for painting the window. """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QSize
from PySide6.QtWidgets import QGridLayout

from workside.widgets import CoreWidget, Banner
from workside.window import BaseWindow


class LayoutWindow(BaseWindow):
  """WorkToy - Window - LayoutWindow
  This class is responsible for painting the window. """

  def __init__(self, *args, **kwargs) -> None:
    BaseWindow.__init__(self, *args, **kwargs)
    self.setMinimumSize(QSize(480, 320))
    self._baseLayout = QGridLayout()
    self._baseWidget = CoreWidget()
    self._topLeft = Banner(True, True, )
    self._topRight = Banner(True, True, )
    self._bottomRight = Banner(True, True, )
    self._bottomLeft = Banner(True, True, )
    self._left = Banner(True, False)
    self._right = Banner(True, False)
    self._top = Banner(False, True)
    self._bottom = Banner(False, True)

  def setupWidgets(self) -> None:
    """Sets up widgets"""
    self._baseLayout.addWidget(self._topLeft, 0, 0)
    self._baseLayout.addWidget(self._topRight, 0, 2)
    self._baseLayout.addWidget(self._bottomRight, 2, 2)
    self._baseLayout.addWidget(self._bottomLeft, 2, 0)
    self._baseLayout.addWidget(self._left, 1, 0)
    self._baseLayout.addWidget(self._right, 1, 2)
    self._baseLayout.addWidget(self._top, 0, 1)
    self._baseLayout.addWidget(self._bottom, 2, 1)
    self._baseWidget.setLayout(self._baseLayout)
    self.setCentralWidget(self._baseWidget)

  def show(self) -> None:
    """Sets up widgets before super call"""
    self.setupWidgets()
    BaseWindow.show(self)

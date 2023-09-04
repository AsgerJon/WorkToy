"""WorkToy - Window - LayoutWindow
This class is responsible for painting the window. """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QGridLayout, QWidget, QPushButton

from workside.window import BaseWindow


class LayoutWindow(BaseWindow):
  """WorkToy - Window - LayoutWindow
  This class is responsible for painting the window. """

  def __init__(self, *args, **kwargs) -> None:
    BaseWindow.__init__(self, *args, **kwargs)
    self._n = 16
    self._baseLayout = QGridLayout()
    self._baseWidget = QWidget()
    self._debugButton01 = QPushButton()
    self._debugButton01.setText('Debug_1')
    self._debugButton01.clicked.connect(self._debugFunction01)
    self._debugButton02 = QPushButton()
    self._debugButton02.setText('Debug_2')
    self._debugButton02.clicked.connect(self._debugFunction02)
    self._debugButton03 = QPushButton()
    self._debugButton03.setText('Debug_3')
    self._debugButton03.clicked.connect(self._debugFunction03)

  def _debugFunction01(self) -> None:
    """LMAO"""

  def _debugFunction02(self) -> None:
    """LMAO"""

  def _debugFunction03(self) -> None:
    """LMAO"""

  def setupWidgets(self) -> None:
    """Sets up widgets"""
    self._baseLayout.addWidget(self._debugButton01, 0, 1)
    self._baseLayout.addWidget(self._debugButton02, 1, 0)
    self._baseLayout.addWidget(self._debugButton03, 1, 1)
    self._baseWidget.setLayout(self._baseLayout)
    self.setCentralWidget(self._baseWidget)

  def show(self) -> None:
    """Sets up widgets before super call"""
    self.setupWidgets()
    BaseWindow.show(self)

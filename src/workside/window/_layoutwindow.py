"""WorkToy - Window - LayoutWindow
This class is responsible for painting the window. """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QPointF
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QGridLayout, QWidget, QPushButton

from workside.widgets import TestWidget
from workside.window import BaseWindow

print(TestWidget)

print(TestWidget.movePos)


class LayoutWindow(BaseWindow):
  """WorkToy - Window - LayoutWindow
  This class is responsible for painting the window. """

  def __init__(self, *args, **kwargs) -> None:
    BaseWindow.__init__(self, *args, **kwargs)
    self._n = 16
    self._baseLayout = QGridLayout()
    self._baseWidget = QWidget()
    self._cunt = TestWidget('Cunt')
    self._debugButton01 = QPushButton()
    self._debugButton01.setText('Debug_1')
    self._debugButton01.clicked.connect(self._debugFunction01)
    self._debugButton02 = QPushButton()
    self._debugButton02.setText('Debug_2')
    self._debugButton02.clicked.connect(self._debugFunction02)
    self._debugButton03 = QPushButton()
    self._debugButton03.setText('Debug_3')
    self._debugButton03.clicked.connect(self._debugFunction03)
    self._cunt.singleClick.connect(self.lol)
    self._cunt.doubleClick.connect(self.lol2)
    self._cunt.pressHold.connect(self.lol3)

  def lol(self, widget: QWidget, point: QPointF) -> None:
    """LMAO"""
    print('single click')
    print(self._cunt.getPressPosition())

  def lol2(self, widget: QWidget, point: QPointF) -> None:
    """LMAO"""
    print('double click')
    print(self._cunt.getPressPosition())

  def lol3(self, ) -> None:
    """LMAO"""
    print('press hold')
    print(self._cunt.getPressPosition())

  def _debugFunction01(self) -> None:
    """LMAO"""
    print('debug 01')

  def _debugFunction02(self) -> None:
    """LMAO"""
    print('debug 02')

  def _debugFunction03(self) -> None:
    """LMAO"""
    print('debug 03')
    print(self._cunt.movePos)

  def setupWidgets(self) -> None:
    """Sets up widgets"""
    self._baseLayout.addWidget(self._cunt, 0, 0)
    self._baseLayout.addWidget(self._debugButton01, 0, 1)
    self._baseLayout.addWidget(self._debugButton02, 1, 1)
    self._baseLayout.addWidget(self._debugButton03, 1, 0)
    self._baseWidget.setLayout(self._baseLayout)
    self.setCentralWidget(self._baseWidget)

  def show(self) -> None:
    """Sets up widgets before super call"""
    self.setupWidgets()
    BaseWindow.show(self)

"""WorkToy - Window - LayoutWindow
This class is responsible for painting the window. """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QSize
from PySide6.QtWidgets import QGridLayout, QWidget, QLabel

from workside.metaside import BaseWindow
from workside.window import CoreWindow


class LayoutWindow(CoreWindow):
  """WorkToy - Window - LayoutWindow
  This class is responsible for painting the window. """

  def __init__(self, *args, **kwargs) -> None:
    CoreWindow.__init__(self, *args, **kwargs)
    self._baseLayout = QGridLayout()
    self._baseWidget = QWidget()
    self._label = QLabel('LMAO')
    self.setWindowTitle('LOL')
    self.setMinimumSize(QSize(640, 480))

  def _resetWidgets(self) -> None:
    """Reset"""
    self._baseLayout = QGridLayout()
    self._baseWidget = QWidget()
    self._label = QLabel('LMAO')
    self.setWindowTitle('LOL')
    self.setMinimumSize(QSize(640, 480))

  def show(self) -> None:
    """LOL"""
    self._resetWidgets()
    self._baseLayout.addWidget(self._label, 0, 0)
    self._baseWidget.setLayout(self._baseLayout)
    self.setCentralWidget(self._baseWidget)
    CoreWindow.show(self)

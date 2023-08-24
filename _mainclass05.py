"""Testing of WorkToy"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import os
from typing import TYPE_CHECKING

from PySide6.QtCore import QSize, Qt, QKeyCombination
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import QMainWindow, QGridLayout, QLabel, QWidget
from icecream import ic

if TYPE_CHECKING:
  pass
else:
  pass


class BaseWindow(QMainWindow):
  pass


class BaseWidget(QWidget):
  pass


class MainWindow(BaseWindow):
  """MainWindow"""

  @classmethod
  def getRisitas(cls) -> QPixmap:
    """Getter-function for risitas"""
    here = os.path.dirname(__file__)
    iconPath = os.path.join(here, 'src', 'icons')
    iconPath = os.path.join(iconPath, 'risitas.jpg')
    return QPixmap(iconPath)

  def __init__(self, *args, **kwargs) -> None:
    BaseWindow.__init__(self, *args, **kwargs)
    self.setWindowTitle('YOLO')
    self._baseWidget = None
    self._baseLayout = None
    self._label = QLabel('FUCK YOU')
    self._menuBar = self.menuBar()
    self._fileMenu = self._menuBar.addMenu('Files')
    self._editMenu = self._menuBar.addMenu('Edit')
    self._helpMenu = self._menuBar.addMenu('Help')
    self._debugMenu = self._menuBar.addMenu('Debug')
    debugIcon = QIcon(MainWindow.getRisitas())
    debugKey = Qt.Key.Key_F1
    debugKeyCombination = QKeyCombination(debugKey)
    shortCutContext = Qt.ShortcutContext.ApplicationShortcut
    self._debugAction01 = self._debugMenu.addAction('DEBUG 01')
    self._debugAction01.setIcon(debugIcon)
    self._debugAction01.setShortcut(debugKeyCombination)
    self._debugAction01.setShortcutContext(shortCutContext)
    self._debugAction01.setShortcutVisibleInContextMenu(True)
    self._debugAction01.setIconVisibleInMenu(True)
    self._debugAction01.triggered.connect(self._debugFunc01)

  def _debugFunc01(self) -> None:
    """Debug func 01"""
    parentLayout = self.info.parentWidget().layout()
    ic(parentLayout)

  def _createBaseWidget(self, ) -> None:
    """Creator-function from BaseWidget"""
    self._baseWidget = BaseWidget()

  def _getBaseWidget(self, **kwargs) -> BaseWidget:
    """Getter-function for BaseWidget"""
    if self._baseWidget is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createBaseWidget()
      return self._getBaseWidget(_recursion=True)
    return self._baseWidget

  def _createBaseLayout(self) -> None:
    """Creator-function for the layout"""
    self._baseLayout = QGridLayout()

  def _getBaseLayout(self, **kwargs) -> QGridLayout:
    """Getter-function for the base layout"""
    if self._baseLayout is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createBaseLayout()
      return self._getBaseLayout(_recursion=True)
    return self._baseLayout

  def _setupWidgets(self) -> None:
    self._label = QLabel('YOLO')
    self._getBaseLayout().addWidget(self._label, 0, 0)
    self._getBaseLayout().addWidget(
      self.info, 1, 1, Qt.AlignmentFlag.AlignRight)
    self._getBaseWidget().setLayout(self._getBaseLayout())
    self.setCentralWidget(self._getBaseWidget())
    self.setMinimumSize(QSize(640, 480))

  def show(self) -> None:
    """Reimplementation of show method"""
    self._setupWidgets()
    QMainWindow.show(self)

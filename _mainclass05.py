"""Testing of WorkToy"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QSize
from PySide6.QtWidgets import QWidget, QMainWindow, QGridLayout, QLabel

ShibokenObject = type(type(QWidget))


class MetaWidget(ShibokenObject):
  """Subclassing the metaclass used by QWidget"""

  def __new__(mcls,
              name: str,
              bases: tuple[type],
              namespace: dict,
              **kwargs) -> None:
    return ShibokenObject.__new__(mcls, name, bases, namespace, **kwargs)

  def __init__(cls,
               name: str,
               bases: tuple[type],
               namespace: dict,
               **kwargs) -> None:
    ShibokenObject.__init__(cls, name, bases, namespace, **kwargs)


class BaseWidget(QWidget, metaclass=MetaWidget):
  """Widget with exposed metaclass"""


class BaseWindow(QMainWindow, metaclass=MetaWidget):
  """Window class with exposed metaclass"""


class MainWindow(BaseWindow):
  """MainWindow"""

  def __init__(self, *args, **kwargs) -> None:
    BaseWindow.__init__(self, *args, **kwargs)
    self.setWindowTitle('YOLO')
    self._baseWidget = None
    self._baseLayout = None
    self._label = None

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
    self._getBaseWidget().setLayout(self._getBaseLayout())
    self.setCentralWidget(self._getBaseWidget())
    self.setBaseSize(QSize(640, 480))

  def show(self) -> None:
    """Reimplementation of show method"""
    self._setupWidgets()
    QMainWindow.show(self)

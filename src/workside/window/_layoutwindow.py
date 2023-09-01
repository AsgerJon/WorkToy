"""WorkToy - Window - LayoutWindow
This class is responsible for painting the window. """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QSize
from PySide6.QtWidgets import QGridLayout, QWidget, QLabel

from workside.window import BaseWindow


class LayoutWindow(BaseWindow):
  """WorkToy - Window - LayoutWindow
  This class is responsible for painting the window. """

  def __init__(self, *args, **kwargs) -> None:
    BaseWindow.__init__(self, *args, **kwargs)
    self._baseLayout = QGridLayout()
    self._baseWidget = QWidget()

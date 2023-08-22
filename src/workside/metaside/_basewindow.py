"""WorkSide - BaseWindow
This class provides the functionalities of QMainWindow with exposed
metaclass."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QMainWindow

from workside.metaside import MetaSide


class MetaWindow(MetaSide):
  """WorkSide - BaseWindow
  This class provides the functionalities of QMainWindow with exposed
  metaclass."""
  pass


class BaseWindow(QMainWindow, MetaWindow):
  """In between subclass of QMainWindow with exposed metaclass"""
  pass

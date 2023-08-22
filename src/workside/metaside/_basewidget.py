"""WorkSide - BaseWidget
This class provides the functionalities of QWidget with exposed metaclass."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QWidget

from workside.metaside import MetaSide


class MetaWidget(MetaSide):
  """WorkSide - BaseWidget
  This class provides the functionalities of QWidget with exposed
  metaclass."""
  pass


class BaseWidget(QWidget, metaclass=MetaWidget):
  """In between subclass of QWidget with exposed metaclass"""
  pass

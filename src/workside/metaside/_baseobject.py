"""WorkSide - BaseObject
This class provides the functionalities of QObject with exposed metaclass.
"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QObject

from workside.metaside import MetaSide


class MetaObject(MetaSide):
  """WorkSide - BaseObject
  This class provides the functionalities of QObject with exposed metaclass.
  """
  pass


class BaseObject(QObject, metaclass=MetaObject):
  """In between subclass of QObject with exposed metaclass"""
  pass

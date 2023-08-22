"""WorkSide - Widgets - CoreWidget
This class provides the baseclass for the widgets. It should not be
instantiated directly, but should be further subclassed. """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Signal

from workside.metaside import BaseWidget


class CoreWidget(BaseWidget):
  """WorkSide - Widgets - CoreWidget
  This class provides the baseclass for the widgets. It should not be
  instantiated directly, but should be further subclassed. """

  def __init__(self, *args, **kwargs) -> None:
    BaseWidget.__init__(self, *args, **kwargs)
    self._owner = None
    self._name = None

  def __set_name__(self, owner: type, name: str) -> None:
    self._name = name
    self._owner = owner

  def __get__(self, obj: object, owner: type) -> object:
    pass

  def __set__(self, obj: object, newValue: object) -> None:
    pass

  def __delete__(self, obj: object) -> None:
    pass

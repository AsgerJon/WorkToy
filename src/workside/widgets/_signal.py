"""WorkToy - Notify
This subclass of 'Signal' allows modification"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Signal
from icecream import ic

ic.configureOutput(includeContext=True)


class Notify(Signal):
  """WorkToy - Notify
  This subclass of 'Signal' allows modification"""

  def __init__(self, *args, **kwargs) -> None:
    super().__init__(*args, **kwargs)

  def __get__(self, obj: object, owner: object) -> object:
    """Reimplementation of __get__"""

    ic(obj, owner)
    return super().__get__(obj, owner)

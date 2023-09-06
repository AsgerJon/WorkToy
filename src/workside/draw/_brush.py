"""WorkSide - Draw - Brush
Subclass of QBrush"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QBrush

from workside.draw import RGB, FillStyleSym
from worktoy.base import DefaultClass


class Brush(QBrush, DefaultClass):
  """Brush subclass"""

  def __init__(self, *args, **kwargs) -> None:
    DefaultClass.__init__(self, *args, **kwargs)
    QBrush.__init__(self, )
    for arg in args:
      print(arg, isinstance(arg, RGB), isinstance(arg, FillStyleSym), )

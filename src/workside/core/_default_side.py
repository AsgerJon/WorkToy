"""WorkSide - Core - DefaultSide
Adds workside related functionality to the DefaultClass from WorkToy."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from PySide6.QtCore import QRect, QRectF, QSizeF, QSize, QPoint, QPointF, \
  QLineF, QLine
from PySide6.QtGui import QPaintDevice
from PySide6.QtWidgets import QWidget

from workside.geometry import Rect, Size
from worktoy.base import DefaultClass


class DefaultSide(DefaultClass):
  """WorkSide - Core - DefaultSide
  Adds workside related functionality to the DefaultClass from WorkToy."""

  def __init__(self, *args, **kwargs) -> None:
    DefaultClass.__init__(self, *args, **kwargs)
    _tempVariable = None

  def __call__(self, obj: Any) -> Any:
    self._tempVariableBase = obj
    self._tempVariableType = type(obj)
    if isinstance(obj, (QRect, QRectF, QLine, QLineF)):
      self._tempVariableData = dict(left=int(obj.left()),
                                    top=int(obj.top()),
                                    right=int(obj.right()),
                                    bottom=int(obj.bottom()), )
    if isinstance(obj, (QSizeF, QSize)):
      self._tempVariableData = dict(width=int(obj.width()),
                                    height=int(obj.height()))
    if isinstance(obj, (QPointF, QPoint)):
      self._tempVariableData = dict(width=int(obj.x()),
                                    height=int(obj.y()))
    if isinstance(obj, QPaintDevice):
      self._tempVariableType = QSize
      self._tempVariableData = dict(width=int(obj.width()),
                                    height=int(obj.height()))
    if isinstance(obj, QWidget):
      return self(obj.visibleRegion().boundingRect())

  def __rshift__(self, other: type) -> Any:
    if other is Rect:
      ints = []
      if self._tempVariableType in [QRect, QRectF, QLine, QLineF]:
        ints = [v for (k, v) in self._tempVariableData.items()]
      elif self._tempVariableType in [QSizeF, QSize, QPointF, QPoint]:
        ints = [v for (k, v) in self._tempVariableData.items()]
        ints = [0, 0, *ints]
      return Rect.fromIntegers(*ints)
    if other is Size:
      if self._tempVariableType in [QRect, QRectF, QLine, QLineF]:
        return

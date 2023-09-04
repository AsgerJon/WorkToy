"""WorkSide - Geometry - Point
Represents a point in the plane"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QPoint, QPointF

from workside.geometry import GeoMeta
from worktoy.fields import IntField, View


class Point(metaclass=GeoMeta):
  """WorkSide - Geometry - Size
  Rectangular size representation."""

  __geometry_class_name__ = 'Point'

  def __init__(self, left: int, top: int) -> None:
    self.left = left
    self.top = top

  left = IntField(1)
  top = IntField(1)

  @View()
  def toQPoint(self) -> QPoint:
    """Converts to instance of QPoint"""
    return QPoint(self.left, self.top)

  @View()
  def toQPointF(self, ) -> QPointF:
    """Converts to instance of QPointF"""
    return QPointF(self.left, self.top)

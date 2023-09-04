"""WorkSide - Geometry - Size
Rectangular size representation."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import QSize, QSizeF, QRect, QRectF
from icecream import ic

from worktoy.base import DefaultClass
from worktoy.fields import IntField, View
from workside.geometry import GeoMeta

if TYPE_CHECKING:
  pass

ic.configureOutput(includeContext=True)


class Size(DefaultClass, metaclass=GeoMeta):
  """WorkSide - Geometry - Size
  Rectangular size representation."""

  __geometry_class_name__ = 'Size'
  width = IntField(1)
  height = IntField(1)

  def __init__(self, *args, **kwargs) -> None:
    DefaultClass.__init__(self, *args, **kwargs)
    intArgs = []
    for arg in args:
      clsName = getattr(arg.__class__, '__geometry_class_name__', None)
      if isinstance(arg, Size) or clsName == 'Rect':
        self.width = arg.width
        self.height = arg.height
        return
      if isinstance(arg, (QRect, QRectF, QSize, QSizeF)):
        self.width = arg.width()
        self.height = arg.height()
        return
      if isinstance(arg, complex):
        self.width = int(arg.real)
        self.height = int(arg.imag)
        return
      if isinstance(arg, (int, float)):
        intArgs.append(int(arg))
    if len(intArgs) > 1:
      self.width, self.height = intArgs[:2]
      return
    self.width, self.height = 1, 1

  @View()
  def area(self, ) -> int:
    """Area View"""
    return self.width * self.height

  @View('QSizeF')
  def toQSizeF(self) -> QSizeF:
    """Converts to instance of QSizeF"""
    return QSizeF(self.width, self.height)

  @View('QSize')
  def toQSize(self) -> QSize:
    """Converts to instance of QSize"""
    return QSize(self.width, self.height)

  def __str__(self, ) -> str:
    name = self.__class__.__qualname__
    width, height = self.width, self.height
    return '%s: width: %d, height. %d' % (name, width, height)

  def __repr__(self, ) -> str:
    name = self.__class__.__qualname__
    width, height = self.width, self.height
    return '%s(%d, %d)' % (name, width, height)

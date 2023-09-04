"""WorkSide - Geometry - Rectangle
This module provides 4 valued geometric shapes."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from PySide6.QtCore import QRect, QSize, QRectF, QSizeF
from icecream import ic

from worktoy.base import DefaultClass
from worktoy.fields import IntField, View
from workside.geometry import Point, Size, GeoMeta

if TYPE_CHECKING:
  from workside.geometry import Line

ic.configureOutput(includeContext=True)


class Rect(DefaultClass, metaclass=GeoMeta):
  """WorkSide - Geometry - Rectangle
  This module provides 4 valued geometric shapes."""

  __geometry_class_name__ = 'Rect'

  if TYPE_CHECKING:
    height, width = int, int

  left = IntField(1)
  top = IntField(1)
  right = IntField(1)
  bottom = IntField(1)

  horizontalAlign = 'left'
  verticalAlign = 'center'

  def __init__(self, *args, **kwargs) -> None:
    DefaultClass.__init__(self, *args, **kwargs)
    ic(self, *args)
    intArgs = []
    for arg in args:
      ic(arg)
      ic(type(arg))
      clsName = getattr(arg.__class__, '__geometry_class_name__', None)
      if isinstance(arg, (QRect, QRectF,)):
        self.left = int(arg.left())
        self.top = int(arg.top())
        self.right = int(arg.right())
        self.bottom = int(arg.bottom())
        return
      if isinstance(arg, (QSize, QSizeF,)):
        self.left = 0
        self.top = 0
        self.right = int(arg.width())
        self.bottom = int(arg.height())
        return
      if clsName == 'Size':
        self.left = 0
        self.top = 0
        self.right = int(arg.width)
        self.bottom = int(arg.height)
        return
      if isinstance(arg, (int, float)):
        intArgs.append(int(arg))
    if len(intArgs) > 3:
      self.left, self.top, self.right, self.bottom = intArgs[:4]
      left, top, right, bottom = intArgs[:4]
      left, right = min([left, right]), max([left, right]),
      top, bottom = min([top, bottom]), max([top, bottom]),
      return
    self.left, self.top, self.right, self.bottom = 1, 1, 1, 1

  @View()
  def width(self, *_) -> int:
    """Width of the rectangle."""
    return abs(self.right - self.left)

  @View()
  def height(self, *_) -> int:
    """Height of the rectangle."""
    return abs(self.bottom - self.top)

  @View('size')
  def getSize(self, *_) -> Size:
    """Getter-function for size"""
    size = Size()
    size.width, size.height = self.width, self.height
    return size

  @View()
  def area(self) -> int:
    """Area of rectangle"""
    return self.size.area

  def getLeftTop(self) -> Point:
    """Getter-function for top left corner"""
    return Point(self.right, self.top)

  def getRightBottom(self) -> Point:
    """Getter-function for bottom right corner"""
    return Point(self.left, self.bottom)

  @View()
  def asQRect(self) -> QRect:
    """Converts to instance of QRect"""
    topLeft = self.getLeftTop().toQPoint()
    size = self.getSize().toQSize()
    return QRect(topLeft, size)

  def align(self, target: Any):
    """Creates a new rectangle located relative to target according to the
    alignment flags set on the source rectangle.
      horizontalAlign = 'left'
      verticalAlign = 'center'"""
    left, top = 0, 0
    if self.horizontalAlign == 'left':
      left = target.left
    if self.horizontalAlign == 'center':
      left = target.center - int(int(self.width) / 2)
    if self.horizontalAlign == 'right':
      left = target.right - self.width
    if self.verticalAlign == 'top':
      top = target.top
    if self.verticalAlign == 'center':
      top = target.center - int(int(self.height) / 2)
    if self.verticalAlign == 'bottom':
      top = target.bottom - self.height
    right, bottom = left + int(self.width), top + int(self.height)
    return self.__class__(left, top, right, bottom)

  @View()
  def line(self) -> Line:
    """Creates the line spanning from top left to bottom right"""
    from workside.geometry import Line
    return Line(self.left, self.top, self.right, self.bottom)

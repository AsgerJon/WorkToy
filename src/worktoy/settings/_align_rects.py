"""WorkToy - Core - AlignRects 
Code writing assistant"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from PySide6.QtCore import QRect, QPoint

from worktoy.descriptors import Attribute
from worktoy.settings import AlignFlag, AlignLeft, AlignTop, AlignHCenter, \
  AlignRight, AlignBottom, AlignVCenter, getNamedAlignment, getVertical, \
  getHorizontal
from worktoy.worktoyclass import WorkToyClass


class AlignRects(WorkToyClass):
  """Provides a callable that aligns rects"""

  alignment = Attribute(AlignLeft)
  verticalAlignment = Attribute()
  horizontalAlignment = Attribute()

  def __init__(self, *args, **kwargs) -> None:
    WorkToyClass.__init__(self, *args, **kwargs)

  @horizontalAlignment.GET
  def getHorizontalAlignment(self) -> AlignFlag:
    """Getter-function for horizontal alignment flag."""
    return getHorizontal(self.alignment)

  @horizontalAlignment.SET
  def setHorizontalAlignment(self, align: Any) -> None:
    """Setter-function for horizontal alignment flag."""
    if isinstance(align, str):
      return self.setHorizontalAlignment(getNamedAlignment(align))
    if isinstance(align, AlignFlag):
      self.alignment = self.verticalAlignment | align
      return
    raise ValueError

  @verticalAlignment.GET
  def getVerticalAlignment(self) -> AlignFlag:
    """Getter-function for vertical alignment flag."""
    return getVertical(self.alignment)

  @verticalAlignment.SET
  def setVerticalAlignment(self, align: Any) -> None:
    """Setter-function for vertical alignment flag."""
    if isinstance(align, str):
      return self.setVerticalAlignment(getNamedAlignment(align))
    if isinstance(align, AlignFlag):
      self.alignment = self.horizontalAlignment | align
      return
    raise ValueError

  def __call__(self, dynRect: QRect, statRect: QRect) -> QRect:
    """Aligns dynRect with statRect according to the currently set
    alignment flags"""

    left, top = None, None

    if self.horizontalAlignment == AlignLeft:
      left = statRect.left()
    if self.horizontalAlignment == AlignHCenter:
      left = int(0.5 * (statRect.width() - dynRect.width()))
    if self.horizontalAlignment == AlignRight:
      left = statRect.right() - dynRect.width()

    if self.verticalAlignment == AlignTop:
      top = statRect.top()
    if self.verticalAlignment == AlignVCenter:
      top = int(0.5 * (statRect.height() - dynRect.height()))
    if self.verticalAlignment == AlignBottom:
      top = statRect.height() - dynRect.height()

    if not self.plenty(left, top):
      raise ValueError
    topLeft = QPoint(left, top)
    size = dynRect.size()
    return QRect(topLeft, size)

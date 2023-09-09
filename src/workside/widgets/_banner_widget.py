"""WorkSide - Widgets - Banner
Constant colored banner widgets"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QPaintEvent

from workside.widgets import CoreWidget, WorkPainter


class Banner(CoreWidget):
  """WorkSide - Widgets - Banner
  Constant colored banner widgets"""

  def __init__(self, vertical: bool = None, horizontal: bool = None,
               *args, **kwargs) -> None:
    CoreWidget.__init__(self, *args, **kwargs)
    if vertical:
      self.setFixedWidth(16)
    if horizontal:
      self.setFixedHeight(16)

  def paintEvent(self, event: QPaintEvent) -> None:
    """Paint event"""
    painter = WorkPainter()
    painter.begin(self, )
    painter.fillBackground()
    painter.outlineBackground()
    painter.end()

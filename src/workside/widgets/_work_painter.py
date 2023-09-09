"""WorkSide - Widgets - WorkPainter
Custom implementation of QPainter."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QPainter, QPaintDevice, Qt

from workside.widgets import CoreWidget


class WorkPainter(QPainter):
  """WorkSide - Widgets - WorkPainter
  Custom implementation of QPainter."""

  def __init__(self, *args, **kwargs) -> None:
    QPainter.__init__(self, *args, **kwargs)

  def begin(self, widget: CoreWidget) -> bool:
    """Reimplementation"""
    return QPainter.begin(self, widget)

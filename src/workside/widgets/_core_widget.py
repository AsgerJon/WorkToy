"""WorkSide - Widgets - CoreWidget
The core widget is the abstract baseclass shared by the widgets in the
WorkSide framework."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QWidget

from worktoy.base import DefaultClass


class CoreWidget(QWidget, DefaultClass, ):
  """WorkSide - Widgets - CoreWidget
  The core widget is the abstract baseclass shared by the widgets in the
  WorkSide framework."""

  def __init__(self, *args, **kwargs) -> None:
    self._events = {}
    DefaultClass.__init__(self, *args, **kwargs)
    parent = self.maybe(QWidget, *args)
    QWidget.__init__(self)
    self.setMouseTracking(True)

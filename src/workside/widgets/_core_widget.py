"""WorkSide - Widgets - CoreWidget
The core widget is the abstract baseclass shared by the widgets in the
WorkSide framework."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from workside.widgets import ButtonSym, ModSym, ActSym
from worktoy.base import DefaultClass
from worktoy.fields import Flag


class CoreWidget(QWidget, DefaultClass):
  """WorkSide - Widgets - CoreWidget
  The core widget is the abstract baseclass shared by the widgets in the
  WorkSide framework."""

  #  States
  position = PointField
  #  Flags
  underPointer = Flag(QWidget, )
  isMoving = Flag(QWidget, )
  #  Signals
  pointer = Signal(QWidget, ActSym, ButtonSym, ModSym, )

  def __init__(self, *args, **kwargs) -> None:
    DefaultClass.__init__(self, *args, **kwargs)
    parent = self.maybe(QWidget, *args)
    QWidget.__init__(self, parent)

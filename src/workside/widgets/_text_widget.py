"""WorkSide - Widgets - TextWidget
Implementing text labels on the paint event."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QPaintEvent, QResizeEvent

from workside.widgets import CoreWidget


class TextWidget(CoreWidget):
  """WorkSide - Widgets - TextWidget
  Implementing text labels on the paint event."""

  def __init__(self, *args, **kwargs) -> None:
    CoreWidget.__init__(self, *args, **kwargs)

  def paintEvent(self, event: QPaintEvent) -> None:
    """Paint event implementation."""

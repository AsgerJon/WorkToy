"""WorkSide - Widgets - MousePoint
Creates a descriptor on the class body on the CoreWidget subclass exposing
the position of the mouse given on the mouse move event."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QEvent

from workside.widgets import AbstractEventField, CoreWidget


class MousePoint(AbstractEventField):
  """LMAO"""

  def __init__(self, *args, **kwargs) -> None:
    AbstractEventField.__init__(self, *args, **kwargs)

  def handleEvent(self, widget: CoreWidget, event: QEvent) -> QEvent:
    """Handles the event"""
    if event.type() == QEvent.Type.MouseMove:
      self.explicitSetter(widget, event.position())
      setattr(widget, self.getPrivateName(), event.position())
    return event

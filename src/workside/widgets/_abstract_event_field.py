"""WorkSide - Widgets - AbstractEventField
Implements descriptor fields on CoreWidget subclasses. """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import Any, TYPE_CHECKING

from PySide6.QtCore import QPointF, QEvent
from PySide6.QtWidgets import QWidget

from worktoy.fields import AbstractField

if TYPE_CHECKING:
  from workside.widgets import CoreWidget


class AbstractEventField(AbstractField):
  """WorkSide - Widgets - EventListener
  General monitor of the events."""

  #
  def __init__(self, *args, **kwargs) -> None:
    AbstractField.__init__(self, *args, **kwargs, )
  #
  # @abstractmethod
  # def handleEvent(self, widget: CoreWidget, event: QEvent) -> QEvent:
  #   """Handles the given event and returns it. """
  #
  # def __set_name__(self, cls: type, name: str) -> None:
  #   AbstractField.__set_name__(self, cls, name)
  #   preEvent = getattr(cls, 'event', QWidget.event)
  #   if TYPE_CHECKING:
  #     preEvent = QWidget.event
  #
  #   def newEvent(widget: CoreWidget, event: QEvent) -> bool:
  #     """Decorated event handler on the widget."""
  #     event = self.handleEvent(widget, event)
  #     return preEvent(widget, event)
  #
  #   setattr(cls, 'event', newEvent)

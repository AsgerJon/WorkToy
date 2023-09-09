"""WorkSide - Handlers - DecorateEventHandler
Subclass of AbstractEventHandler implementing decorators for setting the
augment and consume methods."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QEvent

from workside.handlers import AbstractEventHandler
from workside.widgets import CoreWidget
from worktoy.core import Function


class DecorateEventHandler(AbstractEventHandler):
  """WorkSide - Handlers - DecorateEventHandler
  Subclass of AbstractEventHandler implementing decorators for setting the
  augment and consume methods."""

  def __init__(self, *args, **kwargs) -> None:
    AbstractEventHandler.__init__(self, *args, **kwargs)
    self._innerConsumeEvent = None
    self._innerAugmentEvent = None

  def setConsumer(self, consumeEvent: Function) -> Function:
    """Setter-function for consumeEvent."""
    self.noneGuard(self._innerConsumeEvent, '_innerConsumeEvent')
    self._innerConsumeEvent = self.functionGuard(
      consumeEvent, 'consumeEvent')
    return consumeEvent

  def setAugmenter(self, augmentEvent: Function) -> Function:
    """Setter-function for augmentEvent."""
    self.noneGuard(self._innerAugmentEvent)
    self._innerAugmentEvent = self.functionGuard(
      augmentEvent, 'augmentEvent')
    return augmentEvent

  def consumeEvent(self, widget: CoreWidget, widgetEvent: QEvent) -> bool:
    """Reimplementation using decorated method. If not method is
    available, the method instead defaults to parent implementation. """
    if self._innerConsumeEvent is None:
      return AbstractEventHandler.consumeEvent(self, widget, widgetEvent)
    return self._innerConsumeEvent(widget, widgetEvent)

  def augmentEvent(self, widget: CoreWidget, widgetEvent: QEvent) -> QEvent:
    """Reimplementation using decorated method. If not method is
    available, the method instead defaults to parent implementation. """
    if self._innerAugmentEvent is None:
      return AbstractEventHandler.augmentEvent(self, widget, widgetEvent)
    return self._innerAugmentEvent(widget, widgetEvent)

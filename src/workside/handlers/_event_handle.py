"""WorkSide - Fields - EventHandle
General event handler."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Optional

from PySide6.QtCore import QEvent

from worktoy.core import FunctionDecorator


class EventHandler(FunctionDecorator):
  """WorkSide - Fields - EventHandle
  General event handler."""

  def __init__(self, eventType: QEvent.Type, *args, **kwargs) -> None:
    self._eventType = eventType
    FunctionDecorator.__init__(self, *args, **kwargs)

  def parseEvents(self, *args, **kwargs) -> list[QEvent]:
    """Parses arguments to find all instances of QEvent regardless of
    event type. """
    out = []
    for arg in args:
      if isinstance(arg, QEvent):
        out.append(arg)
    if out:
      return out
    from worktoy.waitaminute import ArgumentError
    raise ArgumentError('event', QEvent)

  def parseEventType(self, *events) -> Optional[QEvent]:
    """Parses the arguments to the first event of the correct event type."""
    for event in events:
      if event.type() == self._eventType:
        return event
    return None

  def invokeInnerFunction(self, *args, **kwargs) -> QEvent:
    """Invoking the inner-function."""
    events = self.parseEvents(*args, **kwargs)
    event = self.parseEventType(*events)
    if event is None:
      return events[0]
    return EventHandler.invokeInnerFunction(self, event)

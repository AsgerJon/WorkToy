"""WorkSide - Widgets - EventField
Descriptor implementation of widget values from events.

In the class body of a subclass of CoreWidget, set an instance of
EventField on an event method. Then instances of the subclass will have
access to that value directly.

For example:

  class Widget(CoreWidget):
    #  Subclass of CoreWidget

    localMouse = EventField(QMouseEvent.position, QMouseEvent)
    globalMouse = EventField(globalPosition, QEvent.Type.MouseMove)

The EventField constructor supports the following signatures:
  - (event: QEvent) -> (value), (QEvent.Type=Any)
  - (event: QEvent) -> (value)
The second argument should be used to restrict value updates to only the
indicated type. Please note that the 'Type' referred the Enum, not the
class. Two events of the same 'type' may have different 'Type'. The
explicit setter function inherited from AbstractField is invoked on the
value returned by the indicated method.

Please note that this is not the case for the third
signature which is intended for use as a decorator. In this case the
decorated method is responsible for processing the events.

The first argument given to the custom method is the widget receiving the
event and the second argument is the event itself. The method is then free
to process the event.

IMPORTANT: Keep in mind that instances of QEvent are garbage collected
more quickly than in other Python contexts. It is, generally speaking,
not possible to keep events after they are processed. For this reason,
custom methods decorated to be used by EventField, should extract the
necessary information from the event immediately, rather than assigning
the event to the local namespace or adding the events to instance data
structures such as lists. Assume that the event becomes unavailable when
the method returns."""

#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import QEvent
from PySide6.QtWidgets import QWidget

from worktoy.core import Function
from worktoy.fields import AbstractField

if TYPE_CHECKING:
  pass
  from workside.widgets import CoreWidget


class EventField(AbstractField):

  def __init__(self, handle: Function, type_: QEvent.Type,
               *args, **kwargs) -> None:
    AbstractField.__init__(self, *args, **kwargs, )
    self._eventHandler = handle
    self._eventType = type_
    if self._eventHandler is None:
      raise NotImplementedError

  def getEventHandler(self) -> Function:
    """Getter-function for event handler"""
    return self._eventHandler

  def getEventType(self) -> QEvent.Type:
    """Getter-function for the event Type"""
    return self._eventType

  def checkEventType(self, event: QEvent) -> bool:
    """This method checks that the event is of the expected QEvent.Type."""
    return True if event.type() == self.getEventType() else False

  def handleEvent(self, widget: CoreWidget, event: QEvent) -> None:
    """Implements the event handling. """
    if self.checkEventType(event):
      handler = self.getEventHandler()
      self.explicitSetter(widget, handler(event))

  def __set_name__(self, cls: type, name: str) -> None:
    AbstractField.__set_name__(self, cls, name)
    preEvent = getattr(cls, 'event', QWidget.event)
    if TYPE_CHECKING:
      preEvent = QWidget.event

    def newEvent(widget: CoreWidget, event: QEvent) -> bool:
      """Decorated event handler on the widget."""
      self.handleEvent(widget, event)
      return preEvent(widget, event)

    setattr(cls, 'event', newEvent)

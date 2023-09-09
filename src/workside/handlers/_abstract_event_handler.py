"""WorkSide - Handlers - AbstractEventHandler
Baseclass for event handlers."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Optional

from PySide6.QtCore import QEvent
from PySide6.QtWidgets import QWidget

from worktoy.base import DefaultClass
from workside.widgets import CoreWidget


class AbstractEventHandler(DefaultClass):
  """WorkSide - Handlers - AbstractEventHandler
  Baseclass for event handlers."""

  def __init__(self, *args, **kwargs) -> None:
    DefaultClass.__init__(self, *args, **kwargs)
    self._fieldName = None
    self._widgetClass = None

  def __set_name__(self, cls: type, name: str) -> None:
    """Sets the name and class. """
    self.setFieldName(name)
    self.setWidgetClass(cls)

  def eventGuard(self, widgetEvent: QEvent, name: str = None) -> QEvent:
    """Raises error if 'widgetEvent' is not an instance of 'QEvent'."""
    if not isinstance(widgetEvent, QEvent):
      from worktoy.waitaminute import TypeSupportError
      expectedType = QEvent
      actualValue = widgetEvent
      argName = self.maybe(name, 'widgetEvent')
      raise TypeSupportError(expectedType, actualValue, argName)
    return widgetEvent

  def subClassGuard(self, cls: type, name: str = None) -> type:
    """Raises error if given class is not a subclass of CoreWidget. """
    argName = self.maybe(name, 'widgetClass')
    if not issubclass(self.someGuard(cls, argName), CoreWidget):
      from worktoy.waitaminute import UnsupportedSubclassException
      expected = CoreWidget
      actual = cls
      raise UnsupportedSubclassException(name, expected, actual)
    return cls

  def widgetGuard(self, widget: CoreWidget, name: str = None) -> CoreWidget:
    """Raises error if 'widget' is 'None' or is not an instance of the
    field class."""
    argName = self.maybe(name, 'widget')
    cls = self.someGuard(self.getWidgetClass(), 'widgetClass')
    if not isinstance(widget, cls):
      from worktoy.waitaminute import TypeSupportError
      expectedType = cls
      actualValue = widget
      raise TypeSupportError(expectedType, actualValue, argName)
    return widget

  def setFieldName(self, fieldName: str) -> None:
    """Setter-function for the field name."""
    self._fieldName = fieldName

  def getFieldName(self, ) -> str:
    """Setter-function for the field name."""
    return self._fieldName

  def setWidgetClass(self, cls: type) -> None:
    """Setter-function for the widget class."""
    self._widgetClass = self.subClassGuard(self.extendEvent(cls))

  def getWidgetClass(self, ) -> type:
    """Getter-function for the widget class."""
    return self._widgetClass

  def extendEvent(self, cls: type) -> type:
    """Extends the 'event' method on the given widget class with this
    event handler. """
    e = getattr(self.subClassGuard(cls), 'event', None)
    if e is None:
      __original_event__ = QWidget.event
    else:
      __original_event__ = self.functionGuard(e)

    def __new_event__(widget: CoreWidget, event: QEvent) -> bool:
      """Extended 'event' method."""
      filteredEvent = self.filterEvent(widget, event)
      if filteredEvent is None:
        return True
      return __original_event__(widget, self.eventGuard(filteredEvent))

    setattr(cls, 'event', __new_event__)
    return cls

  def filterEvent(self, widget: CoreWidget,
                  widgetEvent: QEvent) -> Optional[QEvent]:
    """The filter first passes the event to the 'consumeEvent' method. If
    this returns 'True' the event is considered handled, and this method
    returns 'True'.

    Otherwise, the event is passed to the 'augmentEvent' method and the
    returned event is then propagated to the 'event' method on the
    receiving widget."""
    widget = self.widgetGuard(widget, 'widget')
    widgetEvent = self.eventGuard(widgetEvent, 'widgetEvent')
    if not self.consumeEvent(widget, widgetEvent):
      return self.augmentEvent(widget, widgetEvent)

  def consumeEvent(self, widget: CoreWidget, widgetEvent: QEvent) -> bool:
    """Method responsible for consuming the event. If successful,
    this method should return True, in which case the event is not
    propagated any further.

    Subclasses are not required to implement this method. The default
    implementation always returns 'False'.

    Please note, that this method must either fullly consume the event or
    reject it. """
    return False

  def augmentEvent(self, widget: CoreWidget, widgetEvent: QEvent) -> QEvent:
    """Abstract method responsible for event augmentation. Use this method
    to implement pre-processing of events before they are propagated to
    the remaining widget logic.

    Subclasses are not required to implement this method. The default
    implementation simply returns the event without change.

    Please note, that this method is expected
    to return the augmented event. This means that the returned event must
    be of the same 'type' and 'QEvent.Type'. """
    return widgetEvent

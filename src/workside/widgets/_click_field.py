"""WorkSide - Widgets - ClickField
Implements recognition of mouse clicks. A regular single click has the
following progression:
  (T = T0): Mouse press
  (T < T1): Mouse release. If the mouse button is not released before T1
            the single-click is cancelled, but a press-hold may occur
            instead.
  (T = T2): After mouse release, the click event triggers after a short
            delay allowing for a double click to occur instead.
"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QEvent, QPointF
from PySide6.QtWidgets import QWidget

from workside.settings import ClickTimes
from workside.widgets import TimedFlag, CoreWidget
from worktoy.base import DefaultClass
from worktoy.core import Function
from worktoy.fields import Flag, Attribute
from worktoy.guards import TypeGuard


class ClickField(DefaultClass, ClickTimes):
  """WorkSide - Widgets - ClickField
  Implements recognition of mouse clicks."""

  functionGuard = TypeGuard(Function)
  clickPosition = Attribute(QPointF())

  def __init__(self, *args, **kwargs) -> None:
    DefaultClass.__init__(self, *args, **kwargs)
    self._fieldName = None
    self._fieldOwner = None

  def __set_name__(self, cls: type, name: str) -> None:
    self.setFieldName(name)
    self.setFieldOwner(cls)

  def getFieldName(self, capitalize: bool = None) -> str:
    """Getter-function for the field name."""
    if capitalize is None:
      return self._fieldName
    firstLetter = self._fieldName[0]
    return firstLetter.upper() + self._fieldName[1:]

  def getClickPositionName(self) -> str:
    """Getter-function for name of the click position timer."""
    return '_clickPosition%s' % self.getFieldName(True)

  def getPressName(self) -> str:
    """Getter-function for name of the press timer."""
    return '_press%s' % self.getFieldName(True)

  def getPressHoldName(self) -> str:
    """Getter-function for name of the press hold timer."""
    return '_pressHold%s' % self.getFieldName(True)

  def getDoubleClickDelayName(self) -> str:
    """Getter-function for the name of the double click delay."""
    return '_doubleClickDelay%s' % self.getFieldName(True)

  def getTripleClickDelayName(self) -> str:
    """Getter-function for the name of the triple click delay."""
    return '_tripleClickDelay%s' % self.getFieldName(True)

  def setFieldName(self, fieldName: str) -> None:
    """Setter-function for the field name."""
    self._fieldName = fieldName

  def setFieldOwner(self, fieldOwner: type) -> None:
    """Setter-function for the field owner."""
    self._fieldOwner = fieldOwner

  def initFactory(self, fieldOwner: type) -> Function:
    """Extends the '__init__' on the fieldOwner."""

    originalInit = getattr(fieldOwner, '__init__', None)

    def newInit(widget: CoreWidget, *args, **kwargs) -> None:
      """New init function."""
      originalInit(widget, *args, **kwargs)
      clickPositionName = self.getClickPositionName()
      pressName = self.getPressName()
      doubleName = self.getDoubleClickDelayName()
      pressHoldName = self.getPressHoldName()
      tripleName = self.getTripleClickDelayName()
      pressTimedFlag = TimedFlag(self.pressTime)
      doubleClickDelayTimedFlag = TimedFlag(self.doubleClickDelay)
      pressHoldTimedFlag = TimedFlag(self.pressHold)
      tripleClickDelayTimedFlag = TimedFlag(self.tripleClickDelay)
      setattr(widget, clickPositionName, QPointF())
      setattr(widget, pressName, pressTimedFlag)
      setattr(widget, doubleName, doubleClickDelayTimedFlag)
      setattr(widget, pressHoldName, pressHoldTimedFlag)
      setattr(widget, tripleName, tripleClickDelayTimedFlag)

    return newInit

  def eventFactory(self, fieldOwner: type) -> Function:
    """Extends the 'event' method on the fieldOwner."""

    originalEvent = getattr(fieldOwner, 'event', QWidget.event)

    def newEvent(widget: CoreWidget, event: QEvent) -> bool:
      """New event function."""
      if event.type() == QEvent.Type.MouseButtonPress:
        if not getattr(widget, self.getPressName()):
          setattr(widget, self.getClickPositionName(), event.position())
          getattr(widget, self.getPressName(), ).activate()

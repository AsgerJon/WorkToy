"""WorkSide - Widgets - MouseButtonField
Provides a descriptor field determining if the left mouse button is
pressed on a widget."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations
from typing import TYPE_CHECKING, Any

from worktoy.base import DefaultClass
from worktoy.core import Function
from worktoy.guards import TypeGuard
from worktoy.fields import AbstractField, Flag
from workside.widgets import TimedFlag, ButtonSym

if TYPE_CHECKING:
  from workside.widgets import CoreWidget


class MouseButtonField(DefaultClass):
  """WorkSide - Widgets - MouseButtonField
  Provides a descriptor field determining if the left mouse button is
  pressed on a widget."""

  functionGuard = TypeGuard(Function)
  _decayTime = 500

  def __init__(self, btn: ButtonSym, *args, **kwargs) -> None:
    DefaultClass.__init__(self, *args, **kwargs)
    self._button = btn
    self._fieldName = None
    self._fieldOwner = None

  def __set_name__(self, cls: type, name: str) -> None:
    self.setFieldName(name)
    self.setFieldOwner(cls)

  def setFieldName(self, fieldName: str) -> None:
    """Setter-function for field name."""
    self._fieldName = fieldName

  def setFieldOwner(self, fieldOwner: type) -> None:
    """Setter-function for field owner."""
    self._fieldOwner = fieldOwner
    setattr(self._fieldOwner, '__init__', self.getNewInit(self._fieldOwner))

  def getNewInit(self, fieldOwner: type) -> Function:
    """Creates a new '__init__' function that extends the existing one on
    the given type."""

    oldInit = getattr(fieldOwner, '__init__', None)
    oldInit = self.functionGuard(oldInit, '__init__')

    def newInit(widget: CoreWidget, *args, **kwargs) -> None:
      """Replacement '__init__' method."""
      oldInit(widget, *args, **kwargs)
      setattr(widget, self.getPrivateName(), TimedFlag(self._decayTime))

    return newInit

  def getPrivateName(self) -> str:
    """Getter-function for the name of the private variable."""
    return '_%s' % self._fieldName

  def __get__(self, obj: Any, cls: type) -> bool:
    return True if getattr(obj, self.getPrivateName(), None) else False

  def __set__(self, obj: Any, newValue) -> None:
    timer = getattr(obj, self.getPrivateName(), None)
    if isinstance(timer, TimedFlag):
      timer.start()

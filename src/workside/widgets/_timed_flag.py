"""WorkSide - Widgets - TimedFlag
Implementation of singleshot timers triggered by particular events."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from PySide6.QtCore import QTimer, Qt

from worktoy.base import DefaultClass
from worktoy.core import Function


class TimedFlag(QTimer, DefaultClass):
  """WorkSide - Widgets - Timer
  Implementation of singleshot timers triggered by particular events."""

  def __init__(self, *args, **kwargs) -> None:
    self._interval = None
    self._callback = None
    for arg in args:
      if isinstance(arg, int) and self._interval is None:
        self._interval = arg
      if isinstance(arg, Function) and self._callback is None:
        self._callback = arg
    DefaultClass.__init__(self, *args, **kwargs)
    QTimer.__init__(self, )
    self.setTimerType(Qt.TimerType.PreciseTimer)
    self.setSingleShot(True)
    self.setInterval(self.getInterval())
    self.timeout.connect(self.triggerCallback)

  def __bool__(self, ) -> bool:
    """Is True when the timer is active, otherwise False."""
    return True if self.isActive() else False

  def activate(self, callback: Function = None) -> None:
    """Method triggers the timer"""
    self.start()
    self.setCallback(callback)

  def setCallback(self, callback: Function) -> None:
    """Setter-function for the callback method. """
    self._callback = callback

  def getCallback(self, ) -> Function:
    """Getter-function for the callback method. """
    return self.maybe(self._callback, lambda: None)

  def getInterval(self, ) -> int:
    """Getter-function for defined time interval"""
    return self._interval

  def setInterval(self, interval: int) -> None:
    """Setter-function for defined time interval"""
    self._interval = interval

  def triggerCallback(self) -> Any:
    """Triggers the callback and returns its return value."""
    return self.getCallback()()

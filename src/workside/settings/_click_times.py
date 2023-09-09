"""WorkSide - Settings - ClickTimes
This module provides the time limits used by the ClickField class."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Signal, QPointF
from PySide6.QtWidgets import QWidget


# from workside.widgets import TimedFlag


class ClickTimes:
  """WorkSide - Settings - ClickTimes
  This module provides the time limits used by the ClickField class."""

  pressHold = Signal(QWidget, QPointF)
  singleSignal = Signal()
  singleClick = Signal(QWidget, QPointF)
  doubleSignal = Signal()
  doubleClick = Signal(QWidget, QPointF)
  maxDrift = 64
  pressTime = 500
  doubleClickDelay = 100
  pressHoldMin = 600
  pressHoldMax = 1000
  tripleClickDelay = 500

  @staticmethod
  def distance(P: QPointF, Q: QPointF) -> float:
    """Computes the distance between two points."""
    return ((P.x() - Q.x()) ** 2 + (P.y() - Q.y()) ** 2) ** 0.5

  def __init__(self, *args, **kwargs) -> None:
    self._pressTime = TimedFlag(self.pressTime)
    self._doubleClickDelayTimer = TimedFlag(self.doubleClickDelay)
    self._pressHoldMinTime = TimedFlag(self.pressHoldMin)
    self._pressHoldMaxTime = TimedFlag(self.pressHoldMax)
    self._tripleClickDelayTimer = TimedFlag(self.tripleClickDelay)
    self._doubleClickDelayTimer.timeout.connect(self.singleSignal.emit)
    self._tripleClickDelayTimer.timeout.connect(self.doubleSignal.emit)
    self._pressPosition = QPointF()

  def _resetTime(self, ) -> None:
    """Reset all timers"""
    self._pressTime.stop()
    self._doubleClickDelayTimer.stop()
    self._pressHoldMinTime.stop()
    self._pressHoldMaxTime.stop()
    self._tripleClickDelayTimer.stop()

  def singleClickFunction(self) -> None:
    """Completes single-click."""

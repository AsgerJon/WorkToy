"""WorkSide - Widgets - Velocities
Mouse velocities are still work in progress."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from time import time

from PySide6.QtCore import QPointF
from PySide6.QtWidgets import QWidget

from worktoy.base import DefaultClass


class CoreWidget(QWidget, DefaultClass):
  """WorkSide - Widgets - CoreWidget
  The core widget is the abstract baseclass shared by the widgets in the
  WorkSide framework."""

  _eventHistoryLength = 8

  def __init__(self, *args, **kwargs) -> None:
    self._events = {}
    DefaultClass.__init__(self, *args, **kwargs)
    parent = self.maybe(QWidget, *args)
    QWidget.__init__(self)
    self.setMouseTracking(True)
    self._mousePoints = []
    self._currendIndex = 0

  def _addPoint(self, point: QPointF, ) -> None:
    """Adds the given point to the list of recorded points. """
    self._mousePoints.append((point, time()))
    while len(self._mousePoints) > self._eventHistoryLength:
      self._mousePoints.pop()

  def _getLatestPoint(self) -> QPointF:
    """Getter-function for most recent point."""
    return self._mousePoints[-1]

  def _getVelocities(self) -> list[tuple[QPointF, float]]:
    """Getter-function for the velocities"""
    P, out = self._mousePoints, []
    for prev, post in zip(P[:-1], P[1:]):
      x0, y0, t0 = prev[0].x(), prev[0].y(), prev[1]
      x1, y1, t1 = post[0].x(), post[0].y(), post[1]
      deltaX, deltaY, deltaT = x1 - x0, y1 - y0, t1 - t0
      dx, dy, dt = deltaX / deltaT, deltaY / deltaT, deltaT
      out.append((QPointF(dx, dy), dt))
    return out

"""Test"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from time import time

from PySide6.QtGui import QMouseEvent

from worktoy.base import DefaultClass


class MouseHistory(DefaultClass):
  """Test"""

  def __init__(self, *args, **kwargs) -> None:
    DefaultClass.__init__(self, *args, **kwargs)
    self.data = [None for _ in range(96)]
    self._currentIndex = 0

  def curInd(self) -> int:
    """FUCK"""
    return self._currentIndex

  def record(self, event: QMouseEvent, ) -> None:
    """LMAO"""
    P = event.localPos()
    t = time()

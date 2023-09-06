"""WorkSide - Handlers - MouseEventSym
Symbolic class representing mouse events."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QEvent
from PySide6.QtGui import QMouseEvent

from worktoy.fields import ReadOnly
from worktoy.sym import BaseSym, SYM


class MouseEventSym(BaseSym):
  """WorkSide - Handlers - MouseEventSym
  Symbolic class representing mouse events."""

  Type = ReadOnly()
  value = ReadOnly()
  name = ReadOnly()

  MOVE = SYM.auto()
  MOVE.Type = QEvent.MouseMove
  MOVE.value = 0
  MOVE.name = 'Move'

  PRESS = SYM.auto()
  PRESS.Type = QEvent.MouseButtonPress
  PRESS.value = 1
  PRESS.name = 'Press'

  RELEASE = SYM.auto()
  RELEASE.Type = QEvent.MouseButtonRelease
  RELEASE.value = 2
  RELEASE.name = 'Release'

  DBLCLICK = SYM.auto()
  DBLCLICK.Type = QEvent.MouseButtonDblClick
  DBLCLICK.value = 3
  DBLCLICK.name = 'Double-click'

  ENTER = SYM.auto()
  ENTER.Type = QEvent.Enter
  ENTER.value = 4
  ENTER.name = 'Enter'

  LEAVE = SYM.auto()
  LEAVE.Type = QEvent.Leave
  LEAVE.value = 5
  LEAVE.name = 'Leave'

  def __hash__(self) -> int:
    return int.from_bytes(self.name.encode())

"""WorkToy - Widgets - ButtonSym
Symbolic class representation of mouse buttons."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Qt

from worktoy.fields import IntField
from worktoy.sym import BaseSym, SYM


class ButtonSym(BaseSym):
  """WorkToy - Widgets - ButtonSym
  Symbolic class representation of mouse buttons."""

  value = IntField(0)
  flag = Qt.MouseButton.LeftButton

  null = SYM.auto()
  null.value = 0
  null.flag = Qt.MouseButton.NoButton
  left = SYM.auto()
  left.value = 1
  left.flag = Qt.MouseButton.LeftButton
  right = SYM.auto()
  right.value = 2
  right.flag = Qt.MouseButton.RightButton
  back = SYM.auto()
  back.value = 3
  back.flag = Qt.MouseButton.BackButton
  middle = SYM.auto()
  middle.value = 4
  middle.flag = Qt.MouseButton.MiddleButton
  forward = SYM.auto()
  forward.value = 5
  forward.flag = Qt.MouseButton.ForwardButton

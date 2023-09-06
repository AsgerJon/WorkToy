"""WorkToy - Widgets - ButtonSym
Symbolic class representation of mouse buttons."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Qt

from worktoy.fields import ReadOnly
from worktoy.sym import BaseSym, SYM


class ButtonSym(BaseSym):
  """WorkToy - Widgets - ButtonSym
  Symbolic class representation of mouse buttons."""

  @classmethod
  def fromFlag(cls, buttonFlag: Qt.MouseButton) -> ButtonSym:
    """Returns the sym representing the flag"""
    for sym in ButtonSym:
      if sym.flag == buttonFlag:
        return sym

  value = ReadOnly()
  name = ReadOnly()
  flag = ReadOnly()

  null = SYM.auto()
  null.value = 0
  null.name = 'No Button'
  null.flag = Qt.MouseButton.NoButton
  left = SYM.auto()
  left.value = 1
  left.value = 'Left Button'
  left.flag = Qt.MouseButton.LeftButton
  right = SYM.auto()
  right.value = 2
  right.value = 'Right Button'
  right.flag = Qt.MouseButton.RightButton
  back = SYM.auto()
  back.value = 3
  back.value = 'Back Button'
  back.flag = Qt.MouseButton.BackButton
  middle = SYM.auto()
  middle.value = 4
  middle.value = 'Middle Button'
  middle.flag = Qt.MouseButton.MiddleButton
  forward = SYM.auto()
  forward.value = 5
  forward.value = 'Forward Button'
  forward.flag = Qt.MouseButton.ForwardButton

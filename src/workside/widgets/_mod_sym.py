"""WorkSide - Widget - ModSym
Symbolic class representation of keyboard modifications."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Qt

from worktoy.sym import BaseSym, SYM


class ModSym(BaseSym):
  """WorkSide - Widget - ModKey
  Symbolic class representation of keyboard modifications."""

  value = 0
  flag = Qt.KeyboardModifier

  null = SYM.auto()
  null.value = 0
  null.flag = Qt.KeyboardModifier.NoModifier

  CTRL = SYM.auto()
  CTRL.value = 2
  CTRL.flag = Qt.KeyboardModifier.ShiftModifier

  SHFT = SYM.auto()
  SHFT.value = 3
  SHFT.flag = Qt.KeyboardModifier.ControlModifier

  ALT = SYM.auto()
  ALT.value = 5
  ALT.flag = Qt.KeyboardModifier.AltModifier

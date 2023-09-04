"""WorkSide - Style - LineStyleSym
Symbolic class representation of line styles."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Qt

from worktoy.fields import IntField
from worktoy.sym import BaseSym, SYM


class LineStyleSym(BaseSym):
  """WorkSide - Style - LineStyleSym
  Symbolic class representation of line styles."""

  style = Qt.PenStyle.SolidLine
  value = IntField(0)

  empty = SYM.auto()
  empty.style = Qt.PenStyle.NoPen
  empty.value = 0

  solid = SYM.auto()
  solid.style = Qt.PenStyle.SolidLine
  solid.value = 1

  dash = SYM.auto()
  dash.style = Qt.PenStyle.DashLine
  dash.value = 2

  dot = SYM.auto()
  dot.style = Qt.PenStyle.DotLine
  dot.value = 3

  dashDot = SYM.auto()
  dashDot.style = Qt.PenStyle.DashDotLine
  dashDot.value = 4

"""WorkSide - Style - PenSym
Symbolic class representation of line styles."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Qt

from worktoy.sym import BaseSym, SYM


class PenSym(BaseSym):
  """WorkSide - Style - PenSym
  Symbolic class representation of line styles."""

  style = None

  empty = SYM.auto()
  empty.style = Qt.PenStyle.NoPen

  solid = SYM.auto()
  solid.style = Qt.PenStyle.SolidLine

  dash = SYM.auto()
  dash.style = Qt.PenStyle.DashLine

  dot = SYM.auto()
  dot.style = Qt.PenStyle.DotLine

  dashDot = SYM.auto()
  dashDot.style = Qt.PenStyle.DashDotLine

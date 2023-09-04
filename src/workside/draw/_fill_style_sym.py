"""WorkSide - Style - FillStyleSym
Symbolic class representation of brush styles."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Qt

from worktoy.sym import BaseSym, SYM


class FillStyleSym(BaseSym):
  """WorkSide - Style - FillStyleSym
  Symbolic class representation of brush styles."""

  style = Qt.BrushStyle.NoBrush
  value = 0

  empty = SYM.auto()
  empty.style = Qt.BrushStyle.NoBrush
  empty.value = 0

  blank = SYM.auto()
  blank.style = Qt.BrushStyle.SolidPattern
  blank.value = 1

  horizontal = SYM.auto()
  horizontal.style = Qt.BrushStyle.HorPattern
  horizontal.value = 2

  vertical = SYM.auto()
  vertical.style = Qt.BrushStyle.VerPattern
  vertical.value = 3

  grid = SYM.auto()
  grid.style = Qt.BrushStyle.CrossPattern
  grid.value = 4

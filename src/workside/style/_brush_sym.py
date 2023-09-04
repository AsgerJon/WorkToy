"""WorkSide - Style - FillSym
Symbolic class representation of brush styles."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Qt

from worktoy.sym import BaseSym, SYM


class BrushSym(BaseSym):
  """WorkSide - Style - FillSym
  Symbolic class representation of brush styles."""

  style = None

  empty = SYM.auto()
  empty.style = Qt.BrushStyle.NoBrush

  blank = SYM.auto()
  blank.style = Qt.BrushStyle.SolidPattern

  horizontal = SYM.auto()
  horizontal.style = Qt.BrushStyle.HorPattern

  vertical = SYM.auto()
  vertical.style = Qt.BrushStyle.VerPattern

  grid = SYM.auto()
  grid.style = Qt.BrushStyle.CrossPattern

"""WorkSide - Style - FillSymField
Field class for the symbolic brush style class."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from workside.style import BrushSym
from worktoy.fields import SymField
from worktoy.sym import SyMeta


class BrushSymFill(SymField):
  """WorkSide - Style - FillSymField
  Field class for the symbolic brush style class."""

  def __init__(self, *args, **kwags) -> None:
    SymField.__init__(self, BrushSym, 0, *args, **kwags)

  def getSymClass(self) -> SyMeta:
    return BrushSym

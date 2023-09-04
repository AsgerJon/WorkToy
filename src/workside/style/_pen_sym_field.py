"""WorkSide - Style - PenSymField
Field class for the symbolic line style class."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from workside.style import PenSym
from worktoy.fields import SymField
from worktoy.sym import SyMeta


class PenSymField(SymField):
  """WorkSide - Style - PenSymField
  Field class for the symbolic line style class."""

  def __init__(self, *args, **kwags) -> None:
    SymField.__init__(self, PenSym, 0, *args, **kwags)

  def getSymClass(self) -> SyMeta:
    return PenSym

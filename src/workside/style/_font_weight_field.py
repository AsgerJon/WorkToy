"""WorkSide - Style - FontWeightField
Symbolic field representing the font weight."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from workside.style import FontWeight
from worktoy.fields import IntField, SymField
from worktoy.sym import SyMeta


class FontWeightField(SymField):
  """WorkSide - Style - FontWeightField
  Symbolic field representing the font weight."""

  def __init__(self, defVal: Any, *args, **kwargs) -> None:
    defVal = 0
    SymField.__init__(self, FontWeight, 0, *args, **kwargs)

  def getSymClass(self) -> SyMeta:
    """Getter-function for the symbolic class."""
    return FontWeight

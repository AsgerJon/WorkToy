"""WorkSide - Style - FontFamilyField
Field supported symbolic font families."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from workside.style import FontFamily
from worktoy.fields import SymField
from worktoy.sym import SyMeta


class FontFamilyField(SymField):
  """WorkSide - Style - FontFamilyField
  Field supported symbolic font families."""

  def __init__(self, defVal: Any = None,
               *args, **kwargs) -> None:
    if isinstance(defVal, int):
      SymField.__init__(self, FontFamily, defVal, *args, **kwargs)

  def getSymClass(self) -> SyMeta:
    """Getter-function for the symbolic class."""
    return FontFamily

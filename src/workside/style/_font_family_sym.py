"""WorkToy - SYM - FontFamily
Symbolic class representing font families for use by QFont."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from PySide6.QtGui import QFont
from icecream import ic

from workside.style import FAMILIES
from worktoy.sym import BaseSym, SYM

fontFamilies = FAMILIES
ic.configureOutput(includeContext=True)


class FontFamily(BaseSym, symNames=FAMILIES):
  """WorkToy - SYM - FontFamily
  Symbolic class representing font families for use by QFont."""

  if TYPE_CHECKING:
    name = 'lol'
    value = 777

  def __rshift__(self, other: Any) -> Any:
    if isinstance(other, QFont):
      other.setFamily(self.name)
      return other

  def __getattr__(self, capKey: str) -> Any:
    ic()
    for (key, val) in self.__class__.__dict__.items():
      if key.lower() == capKey.lower():
        return val

  def __getattribute__(self, key: str) -> Any:
    """LMAO"""
    ic(key)

"""WorkToy - SYM - FontFamily
Symbolic class representing font families for use by QFont."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from PySide6.QtGui import QFont

from workside.style import FAMILIES
from worktoy.sym import BaseSym, SYM

fontFamilies = FAMILIES


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

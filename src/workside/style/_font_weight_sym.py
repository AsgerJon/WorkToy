"""WorkSide - Style - FontWeight
Symbolic class representing font weights for use by QFont."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from PySide6.QtGui import QFont

from worktoy.sym import BaseSym, SYM

from workside.style import WEIGHTS


class FontWeight(BaseSym, symNames=WEIGHTS):
  """WorkSide - Style - FontWeight
  Symbolic class representing font weights for use by QFont."""

  if TYPE_CHECKING:
    name = 'lol'
    value = 777

  def toQFontWeight(self) -> QFont.Weight:
    """Converts to value in QFont.Weight"""
    for w in QFont.Weight:
      if self.name.lower() == w.name.lower():
        return w
    raise NameError

  def __rshift__(self, other: Any) -> Any:
    if isinstance(other, QFont):
      other.setWeight(self.toQFontWeight())
      return other


for weight in WEIGHTS:
  setattr(FontWeight, weight, SYM.auto())

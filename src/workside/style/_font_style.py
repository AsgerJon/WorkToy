"""WorkSide - Style - Font
Collection of style settings."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QFont, QPainter

from workside.style import FontSizeField, FontWeightField, FontFamilyField, \
  FontFamily, FontWeight
from worktoy.base import DefaultClass
from worktoy.fields import View


class Font(DefaultClass):
  """WorkSide - Style - FontStyle
  Collection of style settings."""

  family = FontFamilyField(0)
  fontSize = FontSizeField(12)
  weight = FontWeightField('normal')

  @View('style')
  def getFont(self) -> QFont:
    """Getter-function for the QFont version of the font related style
    settings."""
    font = QFont()
    font.setFamily(self.family)
    font.setPointSize(self.fontSize)
    font.setWeight(self.weight)
    return font

  def __matmul__(self, painter: QPainter) -> QPainter:
    """The matmul operator applies the style to the given QPainter."""
    if not isinstance(painter, QPainter):
      return NotImplemented
    painter.setFont(self.style)
    return painter


fontBase = Font()
fontBase.family = FontFamily.Modern_No_20
fontBase.fontSize = 12
fontBase.weight = FontWeight.normal

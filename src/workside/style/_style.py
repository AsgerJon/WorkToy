"""WorkSide - Style - AbstractStyle
Subclasses of AbstractStyle applies situation specific settings to
instances of QPainter. Instances of the subclasses specify style flavours."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QFont, QBrush, QPen, QPainter

from workside.style import fillBase, fontBase, lineBase
from worktoy.base import DefaultClass
from worktoy.fields import View


class Style(DefaultClass):
  """WorkSide - Style - AbstractStyle
  Subclasses of AbstractStyle applies situation specific settings to
  instances of QPainter. Instances of the subclasses specify style
  flavours."""

  lineStyle = lineBase
  fontStyle = fontBase
  fillStyle = fillBase

  def __init__(self, *args, **kwargs) -> None:
    DefaultClass.__init__(self, *args, **kwargs)

  @View('font')
  def getFont(self) -> QFont:
    """Getter-function for the QFont version of the font related style
    settings."""
    return self.fontStyle

  @View('brush')
  def getBrush(self) -> QBrush:
    """Getter-function for the QBrush."""
    return self.fillStyle

  @View('pen')
  def getPen(self) -> QPen:
    """Getter-function for the QPen."""
    return self.lineStyle

  def __matmul__(self, painter: QPainter) -> QPainter:
    """The matmul operator applies the style to the given QPainter."""
    if not isinstance(painter, QPainter):
      return NotImplemented
    painter = self.lineStyle @ painter
    painter = self.fontStyle @ painter
    painter = self.fillStyle @ painter
    return painter


styleBase = Style()

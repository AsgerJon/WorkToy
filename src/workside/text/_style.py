"""WorkSide - Style - AbstractStyle
Subclasses of AbstractStyle applies situation specific settings to
instances of QPainter. Instances of the subclasses specify style flavours."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from workside.text import FontSym
from worktoy.base import DefaultClass


class STYLECLASS(DefaultClass):
  """WorkSide - Style - AbstractStyle
  Subclasses of AbstractStyle applies situation specific settings to
  instances of QPainter. Instances of the subclasses specify style
  flavours."""

  def __init__(self, *args, **kwargs) -> None:
    DefaultClass.__init__(self, *args, **kwargs)

    FONT = FontSym

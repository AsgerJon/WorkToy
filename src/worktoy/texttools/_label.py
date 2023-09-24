"""WorkToy - Core - Label 
Code writing assistant"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.texttools import Header


class Label(Header):
  """Subclass without margins, border and padding leaving only word wrap."""

  def __init__(self, *args, **kwargs) -> None:
    Header.__init__(self, *args, **kwargs)
    self.leftMargin = ''
    self.leftBorder = ''
    self.leftPadding = ''
    self.rightMargin = ''
    self.rightBorder = ''
    self.rightPadding = ''

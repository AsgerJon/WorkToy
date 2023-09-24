"""WorkToy - Core - TextBox 
Code writing assistant"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.texttools import Paragraph


class TextBox(Paragraph):
  """Provides a header for use with the text rendering"""

  def __init__(self, *args, **kwargs) -> None:
    Paragraph.__init__(self, *args, **kwargs)

  def lineFactory(self, fillChar: str) -> str:
    """Factory for creating repeating character lines"""
    n = self.lineLen - (len(self.left + self.right))
    inner = ''
    run = 1
    while run and len(inner) <= n:
      for c in fillChar:
        inner += c
        if len(inner) == n:
          run = 0
          break
    return self.left + inner + self.right

  def getHeader(self) -> str:
    """Getter-function for header lines"""
    return self.lineFactory('_')

  def getFooter(self) -> str:
    """Getter-function for header lines"""
    return self.lineFactory('¨')

  def __str__(self) -> str:
    box = [self.getHeader(), self.getContentLines(), self.getFooter()]
    return '\n'.join(box)

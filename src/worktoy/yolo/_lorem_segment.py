"""LoremSegment provides a segment of lorem ipsum text. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox
from worktoy.text import wordWrap
from worktoy.yolo import AbstractSegment, loremIpsum


class LoremSegment(AbstractSegment):
  """LoremSegment provides a segment of lorem ipsum text. """

  charLen = AttriBox[int](600)

  def __init__(self, *args) -> None:
    """LoremSegment constructor"""
    self.leftMargin = '# '
    self.rightMargin = ' #'
    self.topMargin = ' '
    self.bottomMargin = ' '

  def fitWidth(self, width: int) -> list[str]:
    """Returns the segment text fitted to the specified width."""
    innerWidth = width - len(self.leftMargin) - len(self.rightMargin)
    baseLines = wordWrap(innerWidth, loremIpsum(self.charLen))
    lines = []
    for line in baseLines:
      while len(line) > innerWidth:
        ' '.join(line.split()[:-1])
      while len(line) < innerWidth:
        line += ' '
      lines.append(line)
    out = []
    for line in lines:
      out.append('%s%s%s' % (self.leftMargin, line, self.rightMargin))
    return out

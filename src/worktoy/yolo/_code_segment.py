"""CodeSegment represents a segment of code. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox, Field
from worktoy.yolo import AbstractSegment


class CodeSegment(AbstractSegment):
  """CodeSegment class represents a segment of code. """

  __base_code__ = None
  spaceSymbol = AttriBox[str](' ')
  codeLines = AttriBox[list]([])

  lineNumber = Field()

  @lineNumber.GET
  def leftMargin(self) -> str:
    n = 0
    while 10 ** n < len(self.codeLines):
      n += 1
    return '| %%0%dd | ' % n

  def __init__(self, *lines) -> None:
    """CodeSegment constructor"""
    strArgs = [arg for arg in lines if isinstance(arg, str)]
    self.rightMargin = ' |'
    self.topMargin = '_'
    self.bottomMargin = '¨'

  def addLine(self, line: str) -> None:
    """Adds the given line to the code lines"""
    self.codeLines.append(line.replace('\n', ''))

  def fitWidth(self, width: int) -> list[str]:
    """Returns the segment code fitted to the specified width."""
    top, bottom = self.topMargin * width, self.bottomMargin * width
    spacer = ' ' * width
    innerWidth = width - len(self.lineNumber) - len(self.rightMargin)
    out = []
    for (i, line) in enumerate(self.codeLines):
      left = self.lineNumber % i
      while len(line) + len(left) + len(self.rightMargin) < width:
        line += ' '
      out.append('%s%s%s' % (left, line, self.rightMargin))
      if len(out[-1]) != width:
        print(out[-1])
        raise ValueError('Line length mismatch')
    return [spacer, top, *out, bottom, spacer]

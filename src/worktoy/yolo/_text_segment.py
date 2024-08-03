"""TextSegment represents normal text. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.text import wordWrap
from worktoy.yolo import AbstractSegment


class TextSegment(AbstractSegment):
  """TextSegment class represents a segment of text. """

  __base_text__ = None

  def __init__(self, *args) -> None:
    """TextSegment constructor"""
    strArgs = [arg for arg in args if isinstance(arg, str)]
    self.__base_text__ = ' '.join(strArgs)
    self.leftMargin = '# ) '
    self.rightMargin = ' ('
    self.topMargin = ' '
    self.bottomMargin = ' '

  def fitWidth(self, width: int) -> list[str]:
    """Returns the segment text fitted to the specified width."""
    baseLines = wordWrap(width, self.__base_text__)
    lines = []
    for line in baseLines:
      while len(line) > width:
        ' '.join(line.split()[:-1])
      while len(line) < width:
        line += ' '
      lines.append(line)
    return lines

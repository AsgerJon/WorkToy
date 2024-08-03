"""AbstractSegment provides an abstract base class for defining different
types of segments. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod

from worktoy.desc import AttriBox
from worktoy.meta import BaseObject
from worktoy.text import wordWrap, monoSpace


class AbstractSegment(BaseObject):
  """AbstractSegment provides an abstract base class for defining different
  types of segments. """
  leftMargin = AttriBox[str]('#')
  rightMargin = AttriBox[str]('#')
  topMargin = AttriBox[str]('#')
  bottomMargin = AttriBox[str]('#')

  @abstractmethod
  def fitWidth(self, width: int) -> str:
    """Returns the segment text fitted to the specified width."""


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
    innerWidth = width - len(self.leftMargin) - len(self.rightMargin)
    lines = wordWrap(innerWidth, self.__base_text__)
    out = []
    for line in lines:
      out.append('%s%s%s' % (self.leftMargin, line, self.rightMargin))
    return out


class CodeSegment(AbstractSegment):
  """CodeSegment class represents a segment of code. """

  __base_code__ = None
  spaceSymbol = AttriBox[str](' ')
  codeLines = AttriBox[list]([])

  def __init__(self, *lines) -> None:
    """CodeSegment constructor"""
    strArgs = [arg for arg in lines if isinstance(arg, str)]
    self.leftMargin = '#    | '
    self.rightMargin = ' |   #'
    self.topMargin = '_'
    self.bottomMargin = '¨'

  def addLine(self, line: str) -> None:
    """Adds the given line to the code lines"""
    self.codeLines.append(line.replace('\n', ''))

  def fitWidth(self, width: int) -> list[str]:
    """Returns the segment code fitted to the specified width."""
    lines = []
    innerWidth = width - len(self.leftMargin) - len(self.rightMargin)
    for line in self.codeLines:
      if not line:
        continue
      while len(line) < innerWidth:
        line += ' '
      line = '%s%s%s' % (self.leftMargin, line, self.rightMargin)
      if len(line) > width:
        e = """Encountered line of length: %d, but width is: %d"""
        raise ValueError(e % (len(line), width))
      lines.append(line)
    left = (len(self.leftMargin) - 2) * ' '
    right = (len(self.rightMargin) - 2) * ' '
    top = '#%s%s%s#' % (left, (innerWidth + 2) * self.topMargin, right)
    bottom = '#%s%s%s#' % (left, (innerWidth + 2) * self.bottomMargin, right)
    return [top, *lines, bottom]

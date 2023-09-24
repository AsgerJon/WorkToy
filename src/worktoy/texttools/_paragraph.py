"""WorkToy - Core - Paragraph 
Code writing assistant"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import os

from PySide6.QtCore import Qt
from icecream import ic

from worktoy.descriptors import Attribute
from worktoy.settings import AlignLeft, AlignRight, AlignFlag
# from worktoy.settings.alignments import Align
from worktoy.worktoyclass import WorkToyClass

ic.configureOutput(includeContext=True)


class Paragraph(WorkToyClass):
  """This class contains a string which it renders on as many text lines 
  as is necessary"""

  #  Static attributes
  alignment = Attribute()
  leftMargin = Attribute('  #:')
  leftBorder = Attribute('|')
  leftPadding = Attribute(' ')
  rightPadding = Attribute(' ')
  rightBorder = Attribute('|')
  rightMargin = Attribute(':#  ')
  lineLen = Attribute(77)

  #  Dynamic attributes
  innerWidth = Attribute()
  left = Attribute()
  right = Attribute()

  #  Content Attribute
  currentText = Attribute('hello world')

  def __init__(self, text: str = None, *args, **kwargs) -> None:
    WorkToyClass.__init__(self, *args, **kwargs)
    self.currentText = self.maybe(text, 'lmao')
    self.__horizontal_alignment__ = AlignLeft

  @alignment.GET
  def getAlignment(self) -> AlignFlag:
    """Getter-function for the alignment flag"""
    return self.__horizontal_alignment__

  @alignment.SET
  def setAlignment(self, align: AlignFlag) -> None:
    """Setter-function for the alignment flag"""
    self.__horizontal_alignment__ = align

  @left.GET
  def getLeft(self) -> str:
    """Getter-function for the left side of the text"""
    return '%s%s%s' % (self.leftMargin, self.leftBorder, self.leftPadding)

  @right.GET
  def getRight(self) -> str:
    """Getter-function for the left side of the text"""
    return '%s%s%s' % (self.rightPadding, self.rightBorder, self.rightMargin)

  @innerWidth.GET
  def getInnerWidth(self) -> int:
    """Getter-function for the inner width. This is the space entirely
    available for text."""
    out = self.lineLen
    out -= len(self.leftMargin)
    out -= len(self.leftBorder)
    out -= len(self.leftPadding)
    out -= len(self.rightMargin)
    out -= len(self.rightBorder)
    out -= len(self.rightPadding)
    return out

  def applyFill(self, line: str) -> str:
    """Returns the line padded"""
    n = self.innerWidth - len(line)
    if self.alignment == AlignLeft:
      return line + (n * ' ')
    if self.alignment == AlignRight:
      return (n * ' ') + line
    left, right = int(n // 2), int(n // 2) + n % 2
    return (left * ' ') + line + (right * ' ')

  def applyAlignment(self, line: str, ) -> str:
    """Returns the line with alignment"""

  def getLines(self) -> list[str]:
    """Takes the current text and returns a list of strings with each
    string not exceeding the inner width."""
    words = self.currentText.split(' ')
    lines = []
    line = []
    for word in [*words, None]:
      if word is None or len(' '.join([*line, word])) >= self.innerWidth:
        textLine = self.applyFill(' '.join(line))
        lines.append('%s%s%s' % (self.left, textLine, self.right))
        line = []
        if word is None:
          break
      line.append(word)
    return lines

  def loadLorem(self) -> str:
    """Loads the lorem from disk"""
    here = os.path.dirname(__file__)
    fileName = 'lorem.txt'
    filePath = os.path.join(here, fileName)
    with open(filePath, 'r') as f:
      data = f.read()
    return data

  def testLorem(self) -> str:
    """Loads the lorem text and renders it."""
    self.currentText = self.loadLorem()
    return str(self)

  def getContentLines(self) -> str:
    """Getter-function for the lines containing content."""
    return '\n'.join(self.getLines())

  def __str__(self) -> str:
    return self.getContentLines()

"""ASCIIText class allows formatting of text using ASCII characters."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Self

from worktoy.desc import Field, AttriBox
from worktoy.meta import BaseObject
from worktoy.yolo import AbstractSegment, LoremSegment, CodeSegment


class TextSegment(BaseObject):
  """TextSegment class represents a segment of text. """


class TermText(BaseObject):
  """ASCIIText class allows formatting of text using ASCII characters."""

  __iter_contents__ = None

  outerWidth = AttriBox[int](77)
  textSegments = AttriBox[list]([])

  def addSegment(self, segment: AbstractSegment) -> None:
    """Adds a segment to the text."""
    self.textSegments.append(segment)

  def __iter__(self, ) -> Self:
    """Implementation of iteration"""
    self.__iter_contents__ = [*self.textSegments, ]
    return self

  def __next__(self) -> AbstractSegment:
    """Implementation of next"""
    if self.__iter_contents__:
      return self.__iter_contents__.pop(0)
    raise StopIteration

  def __str__(self, ) -> str:
    """String representation"""
    width = None
    out = []
    for segment in self.textSegments:
      if isinstance(segment, LoremSegment):
        width = self.outerWidth - 4
      elif isinstance(segment, TextSegment):
        width = self.outerWidth - 4
      elif isinstance(segment, CodeSegment):
        width = self.outerWidth - 8
      for line in segment.fitWidth(width):
        if line:
          out.append('#%s#' % str.center(line, self.outerWidth - 2))
    return '\n'.join(out)

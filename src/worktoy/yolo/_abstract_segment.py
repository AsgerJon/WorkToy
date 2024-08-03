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

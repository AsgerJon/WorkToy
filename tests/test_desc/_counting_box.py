"""
CountingBox is an 'AttriBox' that counts the frames it pushes.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.desc import AttriBox

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any, Self


class CountingBox(AttriBox):
  """
  A read of a stored value with no read hook to run is handed out by
  the box without a frame and without the hook phases, and nothing a
  caller sees tells that read from the full one. 'CountingBox' makes
  the difference countable: every access that goes the full way pushes
  one frame through 'createContext', and the box counts them in
  'frames', on the box itself.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Public Variables
  frames: int = 0

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PARENT METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def createContext(self, instance: Any, owner: type, ) -> Self:
    """Counts the frame and pushes it as 'AttriBox' does."""
    object.__setattr__(self, 'frames', self.frames + 1)
    return AttriBox.createContext(self, instance, owner)

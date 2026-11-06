"""
Shrunk is a 'Geometry' redeclaring the box and adding an overload.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox
from worktoy.dispatch import overload

from . import Geometry


class Shrunk(Geometry):
  """
  An alias finds the descriptor of the real name afresh at each access,
  so it follows a subclass redeclaring the attribute and the overloads
  a subclass adds. 'Shrunk' redeclares 'width' and adds a text overload
  of 'scale'.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Public Variables
  width = AttriBox[int](10)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(str)
  def scale(self, s: str) -> str:
    return s * self.width

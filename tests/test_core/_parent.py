"""
Parent is a subclass of 'Grand' with a box of its own.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox

from . import Grand


class Parent(Grand):
  """
  'THIS[Parent].x' and 'THIS[Grand].x' must be one reference, since
  'Parent' inherits 'x' from 'Grand', while 'THIS[Parent].y' is held by
  'Parent' itself. 'Parent' adds the box 'y'.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Public Variables
  y = AttriBox[str]('a')

"""
Grand is a plain class holding an 'AttriBox', for the tests of 'THIS'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox

from . import NoReference


class Grand:
  """
  'THIS[Parent].x' takes its clone from the first class along the
  resolution order of 'Parent' that holds 'x' itself. 'Grand' is that
  holder: a plain class with the box 'x', a plain value 'plain' and the
  'blocked' value that refuses the reference.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  plain = 7
  blocked = NoReference()

  #  Public Variables
  x = AttriBox[int](1)

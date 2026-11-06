"""
Vessel is a worktoy class holding boxes of a builtin, of an 'Object' and
of a text, for the copy and pickle tests.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox
from worktoy.mcls import BaseObject

from . import Part


class Vessel(BaseObject):
  """
  Pickling an instance whose fields a box built must bring the values
  back with their tags naming the box the class declares, which needs
  an owner class importable by name. 'Vessel' is that class.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Public Variables
  count = AttriBox[int](0)
  part = AttriBox[Part]()
  label = AttriBox[str]('vessel')

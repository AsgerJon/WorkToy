"""Testing AttriBoxed KeeNums"""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import OLDAttriBox
from worktoy.keenum import KeeNum, auto


class Flag(KeeNum):
  """Enumeration of boolean states"""

  TRUE = auto()
  FALSE = auto()


class Test:
  """Owner of KeeNum AttriBox"""

  lmao = OLDAttriBox[Flag]('true')

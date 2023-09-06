"""WorkSide - Style - Font - FontSizeSym
Symbolic class representation of point sizes"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.base import DefaultClass
from worktoy.fields import ReadOnly
from worktoy.sym import SYM, BaseSym


class FontSizeSym(BaseSym):
  """WorkSide - Style - Font - FontSizeSym
  Symbolic class representation of point sizes"""

  ptSize = ReadOnly()
  value = ReadOnly()

  paragraph = SYM.auto()
  paragraph.ptSize = 12
  paragraph.value = 0
  paraHead = SYM.auto()
  paraHead.ptSize = 14
  paragraph.value = 1
  secHead = SYM.auto()
  secHead.ptSize = 16
  paragraph.value = 2
  chapHead = SYM.auto()
  chapHead.ptSize = 18
  paragraph.value = 3
  titleHead = SYM.auto()
  titleHead.ptSize = 24
  paragraph.value = 4

"""WorkSide - Style - AlignmentSym
Symbolic class representing alignments."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.fields import BoolField
from worktoy.sym import SYM, BaseSym


class AlignmentSym(BaseSym):
  """WorkSide - Style - AlignmentSym
  Symbolic class representing alignments."""

  horizontal = BoolField(False)
  vertical = BoolField(False)

  center = SYM.auto()
  center.horizontal = True
  center.vertical = True
  left = SYM.auto()
  left.horizontal = True
  left.vertical = False
  right = SYM.auto()
  right.horizontal = True
  right.vertical = False
  top = SYM.auto()
  top.horizontal = False
  top.vertical = True
  bottom = SYM.auto()
  bottom.horizontal = False
  bottom.vertical = True
  justify = SYM.auto()
  justify.horizontal = True
  justify.vertical = False
  low = SYM.auto()
  low.horizontal = True
  low.vertical = True
  high = SYM.auto()
  high.horizontal = True
  high.vertical = True
  tight = SYM.auto()
  tight.horizontal = True
  tight.vertical = True
  spread = SYM.auto()
  spread.horizontal = True
  spread.vertical = True

"""WorkSide - Style - FontWeight
Symbolic class representing text weights for use by QFont."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.fields import ReadOnly
from worktoy.sym import BaseSym, SYM


class FontWeightSym(BaseSym, ):
  """WorkSide - Style - FontWeight
  Symbolic class representing text weights for use by QFont."""

  value = ReadOnly(3)

  thin = SYM.auto()
  thin.value = 0
  extraLight = SYM.auto()
  extraLight.value = 1
  light = SYM.auto()
  light.value = 2
  normal = SYM.auto()
  normal.value = 3
  medium = SYM.auto()
  medium.value = 4
  demiBold = SYM.auto()
  demiBold.value = 5
  bold = SYM.auto()
  bold.value = 6
  extraBold = SYM.auto()
  extraBold.value = 7
  black = SYM.auto()
  black.value = 8

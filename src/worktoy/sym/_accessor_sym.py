"""WorkToy - SYM - AccessorSym
Symbolic class representing accessors."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from worktoy.fields import ReadOnly
from worktoy.sym import BaseSym, SYM


class AccessorSym(BaseSym):
  """WorkToy - SYM - AccessorSym
  Symbolic class representing accessors."""

  value = ReadOnly()
  name = ReadOnly()

  GET = SYM.auto()
  GET.value = 0
  GET.name = 'Getter'

  SET = SYM.auto()
  SET.value = 1
  SET.name = 'Setter'

  DEL = SYM.auto()
  DEL.value = 2
  DEL.name = 'Deleter'

"""WorkToy - SYM - Weekday
Symbolic sample class representation of weekdays with day 0 being monday."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.sym import SyMeta, SYM


class Weekday(SyMeta):
  """WorkToy - SYM - Weekday
  Symbolic sample class representation of weekdays with day 0 being
  monday."""

  monday = SYM.auto()
  tuesday = SYM.auto()
  wednesday = SYM.auto()
  thursday = SYM.auto()
  friday = SYM.auto()
  saturday = SYM.auto()
  sunday = SYM.auto()

"""
WeekDay enumerates the days of the week.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.keenum import KeeNum, Kee

if TYPE_CHECKING:  # pragma: no cover
  pass


class WeekDay(KeeNum):
  """WeekDay enumerates the days of the week."""
  MONDAY = Kee[str]("""Mandag""")
  TUESDAY = Kee[str]("""Tirsdag""")
  WEDNESDAY = Kee[str]("""Onsdag""")
  THURSDAY = Kee[str]("""Torsdag""")
  FRIDAY = Kee[str]("""Fredag""")
  SATURDAY = Kee[str]("""Lørdag""")
  SUNDAY = Kee[str]("""Søndag""")

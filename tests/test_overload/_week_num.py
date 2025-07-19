"""
WeekNum enumerates week days with KeeNum.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeNum, Kee


class WeekNum(KeeNum):
  """
  WeekNum enumerates week days with KeeNum.
  """

  MONDAY = Kee[str]('Mandag')
  TUESDAY = Kee[str]('Tirsdag')
  WEDNESDAY = Kee[str]('Onsdag')
  THURSDAY = Kee[str]('Torsdag')
  FRIDAY = Kee[str]('Fredag')
  SATURDAY = Kee[str]('Lørdag')
  SUNDAY = Kee[str]('Søndag')

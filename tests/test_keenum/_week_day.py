"""
WeekDay is an enumeration of the seven days with Danish names as values.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeNum, Kee


class WeekDay(KeeNum):
  """
  The everyday enumeration: seven members of one value type, declared
  in order, with a plain class attribute beside them that stays what it
  is. 'WeekDay' is importable, so its members pickle by name.
  """

  MONDAY = Kee[str]('mandag')
  TUESDAY = Kee[str]('tirsdag')
  WEDNESDAY = Kee[str]('onsdag')
  THURSDAY = Kee[str]('torsdag')
  FRIDAY = Kee[str]('fredag')
  SATURDAY = Kee[str]('loerdag')
  SUNDAY = Kee[str]('soendag')

  language = 'danish'

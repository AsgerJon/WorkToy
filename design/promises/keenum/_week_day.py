"""
The private file '_week_day' holds 'WeekDay', an enumeration defined at
the top of a file, as pickling requires.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeNum, Kee


class WeekDay(KeeNum):
  """
  'WeekDay' is the days of a week, by their Danish names.
  """

  MONDAY = Kee[str]('Mandag')
  TUESDAY = Kee[str]('Tirsdag')
  WEDNESDAY = Kee[str]('Onsdag')

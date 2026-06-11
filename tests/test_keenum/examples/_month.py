"""
Month enumerates the months of the year.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeNum, Kee


class Month(KeeNum):
  """Month enumerates the months of the year. """
  JANUARY = Kee[str]("""Januar""")
  FEBRUARY = Kee[str]("""Februar""")
  MARCH = Kee[str]("""Marts""")
  APRIL = Kee[str]("""April""")
  MAY = Kee[str]("""Maj""")
  JUNE = Kee[str]("""Juni""")
  JULY = Kee[str]("""Juli""")
  AUGUST = Kee[str]("""August""")
  SEPTEMBER = Kee[str]("""September""")
  OCTOBER = Kee[str]("""Oktober""")
  NOVEMBER = Kee[str]("""November""")
  DECEMBER = Kee[str]("""December""")

"""WorkToy - SYM - Month
Symbolic representation of months with 0 being January"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.sym import BaseSym, SYM


class Month(BaseSym):
  """WorkToy - SYM - Month
  Symbolic representation of months with 0 being January"""

  numDays = 30

  january = SYM.auto()
  january.numDays = 31
  february = SYM.auto()
  february.numDays = 28
  march = SYM.auto()
  march.numDays = 31
  april = SYM.auto()
  april.numDays = 30
  may = SYM.auto()
  may.numDays = 31
  june = SYM.auto()
  june.numDays = 30
  july = SYM.auto()
  july.numDays = 31
  august = SYM.auto()
  august.numDays = 31
  september = SYM.auto()
  september.numDays = 30
  october = SYM.auto()
  october.numDays = 31
  november = SYM.auto()
  november.numDays = 30
  december = SYM.auto()
  december.numDays = 31

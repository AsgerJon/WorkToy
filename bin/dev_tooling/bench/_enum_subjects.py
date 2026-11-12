"""The enumeration cohort: a week of seven days and three permission
flags, as 'enum' declares them and as 'worktoy.keenum' does, and a
field over the week as a plain attribute and as an 'AttriBox'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import enum

from worktoy.desc import AttriBox
from worktoy.keenum import KeeNum, Kee, KeeFlags
from worktoy.mcls import BaseObject


class PyDay(enum.Enum):
  """Baseline: 'enum.Enum'."""

  MONDAY = 'mandag'
  TUESDAY = 'tirsdag'
  WEDNESDAY = 'onsdag'
  THURSDAY = 'torsdag'
  FRIDAY = 'fredag'
  SATURDAY = 'loerdag'
  SUNDAY = 'soendag'


class KeeDay(KeeNum):
  """worktoy: 'KeeNum'."""

  MONDAY = Kee[str]('mandag')
  TUESDAY = Kee[str]('tirsdag')
  WEDNESDAY = Kee[str]('onsdag')
  THURSDAY = Kee[str]('torsdag')
  FRIDAY = Kee[str]('fredag')
  SATURDAY = Kee[str]('loerdag')
  SUNDAY = Kee[str]('soendag')


class PyAccess(enum.Flag):
  """Baseline: 'enum.Flag'."""

  READ = enum.auto()
  WRITE = enum.auto()
  EXEC = enum.auto()


class KeeAccess(KeeFlags):
  """worktoy: 'KeeFlags'."""

  READ = Kee[str]()
  WRITE = Kee[str]()
  EXEC = Kee[str]()


class PlainHolder:
  """Baseline: a plain attribute holding a member."""

  def __init__(self) -> None:
    self.day = KeeDay.MONDAY


class BoxHolder(BaseObject):
  """worktoy: an 'AttriBox' over the enumeration."""

  day = AttriBox[KeeDay](KeeDay.MONDAY)


"""The creation cohort: functions that each run one class statement, so
that the cost of building a class is what is timed.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import enum
import types
from dataclasses import dataclass
from itertools import count

from worktoy.desc import AttriBox
from worktoy.ezdata import EZData, EZField
from worktoy.keenum import KeeNum, Kee, KeeFlags
from worktoy.mcls import BaseObject

_COUNTER = count()
_LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def makePlain() -> type:
  """Baseline: a plain class of two attributes."""

  class Point:
    def __init__(self, x: float, y: float) -> None:
      self.x = x
      self.y = y

  return Point


def makeData() -> type:
  """Baseline: a dataclass of two fields."""

  @dataclass
  class Point:
    x: float
    y: float

  return Point


def makeBase() -> type:
  """worktoy: a 'BaseObject' of two boxes."""

  class Point(BaseObject):
    x = AttriBox[float](0.0)
    y = AttriBox[float](0.0)

  return Point


def makeEZ() -> type:
  """worktoy: an 'EZData' of two fields."""

  class Point(EZData):
    x = EZField[float](0.0)
    y = EZField[float](0.0)

  return Point


def makeEnum() -> type:
  """Baseline: an 'enum.Enum' of seven members."""

  class Day(enum.Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7

  return Day


def makeKee() -> type:
  """worktoy: a 'KeeNum' of seven members."""

  class Day(KeeNum):
    MONDAY = Kee[int](1)
    TUESDAY = Kee[int](2)
    WEDNESDAY = Kee[int](3)
    THURSDAY = Kee[int](4)
    FRIDAY = Kee[int](5)
    SATURDAY = Kee[int](6)
    SUNDAY = Kee[int](7)

  return Day


def _spell(number: int) -> str:
  """A name of five capital letters unique to 'number'."""
  letters = []
  for _ in range(5):
    number, digit = divmod(number, 26)
    letters.append(_LETTERS[digit])
  return ''.join(letters)


def freshNames(size: int) -> list:
  """Flag names no class of this process has used before. worktoy keeps
  one member for each set of flags for the life of the process, so only
  names never seen build every member anew."""
  return [_spell(next(_COUNTER)) for _ in range(size)]


def makeFlag(names: list) -> type:
  """Baseline: an 'enum.Flag' of the named flags. 'enum' builds the
  combinations as they are first asked for, not here."""
  return enum.Flag('Access', names)


def makeKeeFlags(names: list) -> type:
  """worktoy: a 'KeeFlags' of the named flags, with every combination
  built as a member, 2 ** N of them."""

  def body(space: dict) -> None:
    for name in names:
      space[name] = Kee[str]()

  return types.new_class('Access', (KeeFlags,), {}, body)

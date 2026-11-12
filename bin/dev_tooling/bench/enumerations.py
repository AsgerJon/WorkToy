"""The 'enumerations' benchmark: the everyday operations on an
enumeration and on flags, 'worktoy.keenum' beside 'enum', and a field
over an enumeration as a plain attribute and as an 'AttriBox'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from bench._harness import runGrid

_DAYS = """from bench._enum_subjects import %s as Day
m = Day.TUESDAY
d = {m: 1}"""

_FLAGS = """from bench._enum_subjects import %s as Access
a = Access.READ
b = Access.WRITE
ab = a | b"""

_HOLD = """from bench._enum_subjects import %s as Holder, KeeDay
h = Holder()
_ = h.day
TUE = KeeDay.TUESDAY"""


def run() -> str:
  """Time members, flags and fields."""
  cols = ['Day.TUESDAY', "Day['TUESDAY']", "Day('tirsdag')", 'm.value',
    'd[m]', 'list(Day)']
  stmts = {col: col for col in cols}
  rows = [
    ('enum.Enum', _DAYS % 'PyDay', stmts),
    ('KeeNum', _DAYS % 'KeeDay', stmts),
  ]
  first = runGrid('An enumeration of seven members', rows, cols,
    'enum.Enum')
  cols = ['a | b', 'ab & a', 'ab ^ a', '~a', 'bool(a)']
  stmts = {col: col for col in cols}
  rows = [
    ('enum.Flag', _FLAGS % 'PyAccess', stmts),
    ('KeeFlags', _FLAGS % 'KeeAccess', stmts),
  ]
  second = runGrid('Three flags', rows, cols, 'enum.Flag')
  stmts = {
    'first read'   : 'Holder().day',
    'later read'   : 'h.day',
    'assign member': 'h.day = TUE',
    'assign name'  : "h.day = 'tuesday'",
  }
  plain = {k: v for k, v in stmts.items() if k != 'assign name'}
  rows = [
    ('plain attribute', _HOLD % 'PlainHolder', plain),
    ('AttriBox', _HOLD % 'BoxHolder', stmts),
  ]
  third = runGrid('A field over an enumeration', rows, [*stmts],
    'plain attribute')
  return '\n'.join([first, second, third])

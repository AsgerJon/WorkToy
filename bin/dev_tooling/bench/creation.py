"""The 'creation' benchmark: what a class statement costs, for the
classes worktoy builds beside the ones Python builds, and for a flags
class by the number of its flags, up to six.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from bench._harness import runGrid, measureOnce, formatTable

_IMPORT = 'from bench._creation_subjects import %s as make'

_FRESH = """from bench._creation_subjects import %s as make, freshNames
names = freshNames(%d)"""


def run() -> str:
  """Time class statements, then flags classes of 2, 4 and 6 flags.
  Six flags is the limit of what is reasonable in one class."""
  rows = []
  for label, name in (
      ('plain class', 'makePlain'),
      ('dataclass', 'makeData'),
      ('BaseObject, two boxes', 'makeBase'),
      ('EZData, two fields', 'makeEZ'),
      ('enum.Enum, seven', 'makeEnum'),
      ('KeeNum, seven', 'makeKee'),
  ):
    rows.append((label, _IMPORT % name, {'class statement': 'make()'}))
  first = runGrid('One class statement', rows, ['class statement'],
    'plain class')
  sizes = (2, 4, 6)
  cols = ['%d flags' % size for size in sizes]
  stmts = {col: 'make(names)' for col in cols}
  out = [first]
  for title, spec in (
      ('A flags class', _FRESH),
  ):
    cells = []
    for label, name in (
        ('enum.Flag', 'makeFlag'),
        ('KeeFlags', 'makeKeeFlags'),
    ):
      for col, size in zip(cols, sizes):
        setup = spec % (name, size)
        cells.append((label, col, setup))
    out.append(_flagsGrid(title, cols, cells))
  return '\n'.join(out)


def _flagsGrid(title: str, cols: list, cells: list) -> str:
  """One table of flags classes, each timed once after a setup of its
  own, since the number of flags is part of the setup and a class of
  new flags cannot be built twice."""
  timed = {}
  labels = []
  for label, col, setup in cells:
    if label not in labels:
      labels.append(label)
    timed[(label, col)] = measureOnce('make(names)', setup)
  table = formatTable(labels, cols, timed, 'enum.Flag')
  return '\n'.join([title, '=' * len(title), table, ''])

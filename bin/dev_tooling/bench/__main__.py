"""Entry point: run the cohort through every operation and print the
ratio table. Invoke with './bench.sh' or 'python -m bench'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import os
import sys

#  Put the src layout on the path before importing worktoy-backed
#  subjects, so the bench runs without an editable install. The repo
#  root is found by walking up to the directory holding 'pyproject.toml',
#  so the bench works wherever it is nested under the root.
_HERE = os.path.dirname(os.path.abspath(__file__))


def _repoRoot(start: str) -> str:
  """Walk up from 'start' to the directory holding 'pyproject.toml'."""
  current = start
  while current != os.path.dirname(current):
    if os.path.isfile(os.path.join(current, 'pyproject.toml')):
      return current
    current = os.path.dirname(current)
  return start


_SRC = os.path.join(_repoRoot(_HERE), 'src')
if _SRC not in sys.path:
  sys.path.insert(0, _SRC)

from bench._harness import measure, formatTable  # noqa: E402

#  Label -> subject class name in 'bench._subjects'. Display order.
COHORT = {
  'plain'    : 'PlainPoint',
  'slots'    : 'SlotsPoint',
  'dataclass': 'DataPoint',
  'ezdata'   : 'EZPoint',
  'attribox' : 'BoxPoint',
  'field'    : 'FieldPoint',
  'fastbox'  : 'FastPoint',
}

OPS = ('construct', 'read', 'write')

#  Ratios are taken against the plainest hand-written class, matching
#  the 'versus a normal Python class' framing.
BASELINE = 'plain'


def stmtFor(op: str) -> str:
  """Return the timed statement for the given operation."""
  return {
    'construct': 'Cls(1.0, 2.0)',
    'read'     : 'p.x',
    'write'    : 'p.x = 1.0',
  }[op]


def setupFor(clsName: str, op: str) -> str:
  """Return the timeit setup: import the subject, and for read/write
  build the instance the statement operates on."""
  lines = ['from bench._subjects import %s as Cls' % clsName]
  if op in ('read', 'write'):
    lines.append('p = Cls(1.0, 2.0)')
  return '\n'.join(lines)


def main() -> int:
  """Time every (implementation, operation) pair and print the table."""
  cells = {}
  for label, clsName in COHORT.items():
    for op in OPS:
      cells[(label, op)] = measure(stmtFor(op), setupFor(clsName, op))
  rows = [*COHORT.keys()]
  print(formatTable(rows, [*OPS], cells, BASELINE))
  return 0


if __name__ == '__main__':
  sys.exit(main())

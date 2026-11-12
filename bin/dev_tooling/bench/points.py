"""The 'points' benchmark: one 2D point implemented seven ways, timed
for construction, a read and a write. The cohort is in '_subjects'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from bench._harness import runGrid

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

STMTS = {
  'construct': 'Cls(1.0, 2.0)',
  'read'     : 'p.x',
  'write'    : 'p.x = 1.0',
}


def run() -> str:
  """Time every (implementation, operation) pair. Ratios are taken
  against the plainest hand-written class."""
  rows = []
  for label, clsName in COHORT.items():
    setup = 'from bench._subjects import %s as Cls' % clsName
    setup = '%s\np = Cls(1.0, 2.0)' % setup
    rows.append((label, setup, STMTS))
  title = 'A point with two float attributes'
  return runGrid(title, rows, [*STMTS], 'plain')

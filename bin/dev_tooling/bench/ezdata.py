"""The 'ezdata' benchmark: a dataclass at work, 'worktoy.ezdata' beside
'dataclasses', and beside the same classes written with boxes, an
'AttriBox' for each attribute or a 'FixBox', which is set once. Four
tables: making an instance, using one, comparing two, and a default
that is built anew for each instance. The cohort is in
'_ezdata_subjects'. The class statement itself is timed by the
'creation' benchmark, and a point beside five other ways of writing
one by 'points'.

The boxes generate no method, so the box rows stand where a class of
boxes has the operation: making an instance through the constructor it
writes itself, a read, a write and a built default. A 'FixBox' takes
no second write, so it has no write either.

Some columns compare what a builder writes, not equal work.
'dataclasses.asdict' and 'dataclasses.astuple' copy deeply and recurse
into a nested dataclass, where 'asDict' and 'asTuple' are shallow. An
'EZData' and a box convert an 'int' given for a 'float', where a
dataclass stores it as it came. And a box builds its default at the
first read, not as the instance is made, so 'defaults' is cheap for
the box rows and the cost shows in the last table, which makes an
instance and reads the default once. Two columns have no dataclass
beside them: a dataclass does not unpack, and it cannot be frozen in a
subclass of one that is not.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from bench._harness import runGrid

_SETUP = """from dataclasses import asdict, astuple, replace
from bench._ezdata_subjects import %(point)s as Point
from bench._ezdata_subjects import %(frozen)s as Frozen
from bench._ezdata_subjects import %(account)s as Account
from bench._ezdata_subjects import %(version)s as Version
from bench._ezdata_subjects import %(bag)s as Bag
from bench._ezdata_subjects import %(circle)s as Circle
p = Point(1.0, 2.0)
q = Point(1.0, 2.0)
r = Point(3.0, 2.0)
f = Frozen(1.0, 2.0)
a = Version(1, 2)
b = Version(1, 3)
many = [Version(i %% 7, i) for i in range(100)]"""

_BOX_SETUP = """from bench._ezdata_subjects import %(point)s as Point
from bench._ezdata_subjects import %(account)s as Account
from bench._ezdata_subjects import %(bag)s as Bag
from bench._ezdata_subjects import %(circle)s as Circle
p = Point(1.0, 2.0)"""

#  Role -> subject class name in 'bench._ezdata_subjects'.
_DATA = {
  'point'  : 'DataPoint',
  'frozen' : 'FrozenDataPoint',
  'account': 'DataAccount',
  'version': 'DataVersion',
  'bag'    : 'DataBag',
  'circle' : 'DataCircle',
}

_EZ = {
  'point'  : 'EZPoint',
  'frozen' : 'FrozenEZPoint',
  'account': 'EZAccount',
  'version': 'EZVersion',
  'bag'    : 'EZBag',
  'circle' : 'EZCircle',
}

_BOX = {
  'point'  : 'BoxPoint',
  'account': 'BoxAccount',
  'bag'    : 'BoxBag',
  'circle' : 'BoxCircle',
}

_FIX = {
  'point'  : 'FixPoint',
  'account': 'FixAccount',
  'bag'    : 'FixBag',
  'circle' : 'FixCircle',
}


def _grid(
    title: str,
    cols: list,
    data: dict,
    ez: dict,
    box: dict = None,
    fix: dict = None,
) -> str:
  """One table of the cohorts, ratios against the dataclass. 'box' and
  'fix' are the statements of the two box rows, each left out of a
  table where it has none."""
  rows = [
    ('dataclass', _SETUP % _DATA, data),
    ('EZData', _SETUP % _EZ, ez),
  ]
  if box is not None:
    rows.append(('AttriBox', _BOX_SETUP % _BOX, box))
  if fix is not None:
    rows.append(('FixBox', _BOX_SETUP % _FIX, fix))
  return runGrid(title, rows, cols, 'dataclass')


def _making() -> str:
  """The constructor, by each way of calling it."""
  stmts = {
    'by position'  : 'Point(1.0, 2.0)',
    'by keyword'   : 'Point(x=1.0, y=2.0)',
    'defaults'     : 'Point()',
    'int for float': 'Point(1, 2)',
    'frozen'       : 'Frozen(1.0, 2.0)',
    'post init'    : 'Account(5.0)',
  }
  written = ('by position', 'defaults', 'int for float', 'post init')
  boxed = {key: stmts[key] for key in written}
  return _grid('Making an instance', [*stmts], stmts, stmts,
    box=boxed, fix=boxed)


def _using() -> str:
  """What is done with one instance."""
  cols = ['read', 'write', 'unpack', 'as a dict', 'as a tuple',
    'replace', 'repr']
  data = {
    'read'      : 'p.x',
    'write'     : 'p.x = 1.0',
    'as a dict' : 'asdict(p)',
    'as a tuple': 'astuple(p)',
    'replace'   : 'replace(p, y=5.0)',
    'repr'      : 'repr(p)',
  }
  ez = {
    'read'      : 'p.x',
    'write'     : 'p.x = 1.0',
    'unpack'    : 'x, y = p',
    'as a dict' : 'p.asDict()',
    'as a tuple': 'p.asTuple()',
    'replace'   : 'p.replace(y=5.0)',
    'repr'      : 'repr(p)',
  }
  box = {'read': 'p.x', 'write': 'p.x = 1.0'}
  fix = {'read': 'p.x'}
  return _grid('Using an instance', cols, data, ez, box=box, fix=fix)


def _comparing() -> str:
  """Equality, hashing and ordering, which the boxes do not generate."""
  cols = ['equal', 'unequal', 'a frozen subclass', 'hash', 'less than',
    'sorted, 100']
  data = {
    'equal'      : 'p == q',
    'unequal'    : 'p == r',
    'hash'       : 'hash(f)',
    'less than'  : 'a < b',
    'sorted, 100': 'sorted(many)',
  }
  ez = dict(data)
  ez['a frozen subclass'] = 'p == f'
  return _grid('Comparing two instances', cols, data, ez)


def _defaults() -> str:
  """A default that is an object of its own for every instance: the
  instance is made and the default read once, which is when a box
  builds it."""
  stmts = {
    'a list'         : 'Bag().items',
    'a nested object': 'Circle().center',
  }
  title = 'An instance and the first read of a built default'
  return _grid(title, [*stmts], stmts, stmts, box=stmts, fix=stmts)


def run() -> str:
  """Time the four tables."""
  return '\n'.join([_making(), _using(), _comparing(), _defaults()])

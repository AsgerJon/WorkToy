"""The 'dispatching' benchmark: what one call of an overloaded method
costs, beside a plain method, a chain of 'isinstance' tests written by
hand and 'functools.singledispatch', and what the everyday routes of
the dispatcher cost beside its fastest: an exact type, a subclass, and
an 'int' where a 'float' is declared. The last-resort cast is left
out, since a call leaning on it is no everyday call.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from bench._harness import runGrid

_SETUP = """from bench._dispatch_subjects import Plain, ByHand, single
from bench._dispatch_subjects import Loaded
p = Plain()
h = ByHand()
o = Loaded()"""


def run() -> str:
  """Time one call for each way of dispatching, then each route of an
  overload."""
  cols = ['int', 'float', 'bool, a subclass']
  args = ['3', '2.5', 'True']
  rows = []
  for label, call in (
      ('plain method', 'p.f(%s)'),
      ('isinstance by hand', 'h.f(%s)'),
      ('singledispatch', 'single(%s)'),
      ('overload', 'o.f(%s)'),
  ):
    stmts = {col: call % arg for col, arg in zip(cols, args)}
    rows.append((label, _SETUP, stmts))
  first = runGrid('One call, by the type of its argument', rows, cols,
    'plain method')
  routes = [
    ('exact type', _SETUP, {'call': 'o.f(3)'}),
    ('subclass (bool for int)', _SETUP, {'call': 'o.f(True)'}),
    ('widened (int for float)', _SETUP, {'call': 'o.g(3)'}),
    ('two arguments, exact', _SETUP, {'call': "o.f('a', 'b')"}),
  ]
  second = runGrid('The routes of an overload', routes, ['call'],
    'exact type')
  return '\n'.join([first, second])

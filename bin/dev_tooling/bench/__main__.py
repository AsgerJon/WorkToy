"""Entry point: run the benchmarks and print their tables. Invoke with
'./bench.sh' or 'python -m bench', from 'bin/dev_tooling'.

  python -m bench                 every benchmark
  python -m bench dispatching     the named ones, in the order given
  python -m bench --list          the names
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import importlib
import os
import platform
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

#  Name -> what it measures. Display and running order. Each name is a
#  file of this folder with a 'run' function returning its tables.
BENCHES = {
  'points'      : 'a point of two attributes, seven ways',
  'dispatching' : 'a call of an overloaded method',
  'enumerations': 'members, flags and a field over an enumeration',
  'creation'    : 'the class statement',
  'startup'     : 'the import',
}


def _header() -> str:
  """One line naming the library and the interpreter measured."""
  import worktoy
  return 'worktoy %s on Python %s' % (
    worktoy.__version__, platform.python_version())


def main(*names) -> int:
  """Run the named benchmarks, every one when none is named."""
  if '--list' in names:
    for name, what in BENCHES.items():
      print('%-13s %s' % (name, what))
    return 0
  unknown = [name for name in names if name not in BENCHES]
  if unknown:
    print('No benchmark named: %s' % ', '.join(unknown))
    print('The names: %s' % ', '.join(BENCHES))
    return 1
  print(_header())
  print()
  for name in names or BENCHES:
    module = importlib.import_module('bench.%s' % name)
    print(module.run())
    sys.stdout.flush()
  return 0


if __name__ == '__main__':
  sys.exit(main(*sys.argv[1:]))

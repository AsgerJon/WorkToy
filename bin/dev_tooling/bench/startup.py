"""The 'startup' benchmark: what importing worktoy costs a program at
its start, beside starting the interpreter and importing the standard
library packages worktoy is compared with.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
import time

from bench._harness import formatTable

_STDLIB = 'import enum, dataclasses, functools'
_WORKTOY = 'import worktoy'


def _best(code: str, env: dict, repeat: int) -> float:
  """The fastest of 'repeat' fresh interpreters running 'code'."""
  best = None
  for _ in range(repeat):
    start = time.perf_counter()
    subprocess.run([sys.executable, '-c', code], env=env, check=True)
    taken = time.perf_counter() - start
    if best is None or taken < best:
      best = taken
  return best


def run() -> str:
  """Time fresh interpreters, without a bytecode cache and, where the
  interpreter can keep one outside the source tree, with one."""
  src = [path for path in sys.path if path.endswith('src')][0]
  cold = dict(os.environ, PYTHONPATH=src, PYTHONDONTWRITEBYTECODE='1')
  rows = ['interpreter alone', 'standard library', 'worktoy']
  codes = ['pass', _STDLIB, _WORKTOY]
  cols = ['no bytecode cache']
  cells = {}
  for row, code in zip(rows, codes):
    cells[(row, cols[0])] = _best(code, cold, 7)
  if sys.version_info >= (3, 8):
    #  'PYTHONPYCACHEPREFIX' keeps the cache in a folder of its own, so
    #  no '__pycache__' is written beside the sources.
    cols.append('bytecode cached')
    prefix = tempfile.mkdtemp(prefix='worktoy_bench_')
    try:
      warm = dict(os.environ, PYTHONPATH=src, PYTHONPYCACHEPREFIX=prefix)
      if 'PYTHONDONTWRITEBYTECODE' in warm:
        del warm['PYTHONDONTWRITEBYTECODE']
      for code in codes:
        _best(code, warm, 1)
      for row, code in zip(rows, codes):
        cells[(row, cols[1])] = _best(code, warm, 7)
    finally:
      shutil.rmtree(prefix, ignore_errors=True)
  title = 'A fresh interpreter, to the end of the import'
  table = formatTable(rows, cols, cells, 'interpreter alone')
  return '\n'.join([title, '=' * len(title), table, ''])

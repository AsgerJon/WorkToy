"""Timing core and table renderer for the benchmarks.

Methodology, so the numbers survive a hostile reading:

- Each operation is timed with 'timeit.Timer' using a string 'stmt',
  so the work runs inside timeit's own loop with no per-iteration
  Python function-call wrapper to distort cheap operations.
- 'Timer.autorange' picks an iteration count large enough that the
  total run dominates clock granularity.
- The reported time is the MINIMUM across repeats. For a micro-
  benchmark noise is one-sided (scheduling, GC, cache), so the min is
  the cleanest estimate of the true cost, not the mean.
- Results are reported as a ratio against a chosen baseline, because
  absolute nanoseconds are machine-specific but the ratio is the part
  that actually transfers between machines.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from timeit import Timer
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias

  Seconds: TypeAlias = float
  Cells: TypeAlias = dict[tuple[str, str], Seconds]


def measure(stmt: str, setup: str, **kwargs) -> float:
  """Return the per-operation time in seconds for 'stmt'.

  Parameters
  ----------
  stmt : str
      The operation to time, executed once per timeit iteration.
  setup : str
      Code run once before timing to import the subject and build any
      instance the 'stmt' reads.
  **kwargs
      repeat : int, optional
          Number of timing repeats; the minimum is kept. Defaults to 7.

  Returns
  -------
  float
      Best-case seconds for a single execution of 'stmt'.
  """
  repeat = kwargs.get('repeat', 7)
  timer = Timer(stmt, setup)
  number, _ = timer.autorange()
  best = min(timer.repeat(repeat, number))
  return best / number


def formatTable(rows: list[str], cols: list[str], cells: Cells,
                baseline: str) -> str:
  """Render the timing grid as a fixed-width table.

  Each cell shows nanoseconds and the ratio against the baseline row
  for that column. The baseline row itself shows a ratio of 1.

  Parameters
  ----------
  rows : list of str
      Implementation labels, in display order.
  cols : list of str
      Operation names, in display order.
  cells : dict
      Maps '(row, col)' to seconds, as returned by 'measure'.
  baseline : str
      The row label every ratio is taken against.

  Returns
  -------
  str
      The assembled, newline-joined table.
  """
  labelWidth = max(len(r) for r in [*rows, 'impl'])
  cellWidth = 20
  out = []
  header = 'impl'.ljust(labelWidth)
  for col in cols:
    header = '%s  %s' % (header, col.center(cellWidth))
  out.append(header)
  out.append('-' * len(header))
  for row in rows:
    line = row.ljust(labelWidth)
    for col in cols:
      seconds = cells[(row, col)]
      ratio = seconds / cells[(baseline, col)]
      ns = seconds * 1e9
      cell = '%8.1f ns  x%5.1f' % (ns, ratio)
      line = '%s  %s' % (line, cell.center(cellWidth))
    out.append(line)
  out.append('')
  out.append('ratios are against the %r row.' % baseline)
  return '\n'.join(out)

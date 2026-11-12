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
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from timeit import Timer
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover, no mutate
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


def measureOnce(stmt: str, setup: str, **kwargs) -> float:
  """Return the time in seconds of one execution of 'stmt', for work
  that cannot be repeated in a loop, such as building a class whose
  parts the library keeps for the life of the process.

  The setup runs afresh before every execution, and the minimum is
  kept, as in 'measure'.

  Parameters
  ----------
  stmt : str
      The operation to time, executed once after each setup.
  setup : str
      Code run before every execution.
  **kwargs
      repeat : int, optional
          Number of executions; the minimum is kept. Defaults to 5.

  Returns
  -------
  float
      Best-case seconds for a single execution of 'stmt'.
  """
  repeat = kwargs.get('repeat', 5)
  return min(Timer(stmt, setup).repeat(repeat, 1))


def formatTime(seconds: float) -> str:
  """Render a time in the unit that keeps it readable: nanoseconds
  below a microsecond, microseconds below a millisecond, else
  milliseconds."""
  if seconds < 1e-6:
    return '%8.1f ns' % (seconds * 1e9)
  if seconds < 1e-3:
    return '%8.2f us' % (seconds * 1e6)
  return '%8.2f ms' % (seconds * 1e3)


def runGrid(title: str, rows: list, cols: list, baseline: str,
    **kwargs) -> str:
  """Time a grid of statements and render it under a title.

  Parameters
  ----------
  title : str
      The heading printed above the table.
  rows : list
      One '(label, setup, stmts)' per implementation, where 'stmts'
      maps a column name to the statement timed for it. A column a row
      leaves out stays blank. Rows sharing a label are one row of the
      table, which is how a row gets a setup of its own for a column.
  cols : list of str
      Column names, in display order.
  baseline : str
      The row label every ratio is taken against.
  **kwargs
      once : bool, optional
          Time each statement with 'measureOnce' instead of 'measure'.
          Defaults to False.

  Returns
  -------
  str
      The title, an underline and the table.
  """
  once = kwargs.get('once', False)
  cells = {}
  for label, setup, stmts in rows:
    for col in cols:
      if col not in stmts:
        continue
      if once:
        cells[(label, col)] = measureOnce(stmts[col], setup)
      else:
        cells[(label, col)] = measure(stmts[col], setup)
  labels = []
  for label, _, _ in rows:
    if label not in labels:
      labels.append(label)
  table = formatTable(labels, cols, cells, baseline)
  return '\n'.join([title, '=' * len(title), table, ''])


def formatTable(
    rows: list[str], cols: list[str], cells: Cells,
    baseline: str
    ) -> str:
  """Render the timing grid as a fixed-width table.

  Each cell shows the time and the ratio against the baseline row for
  that column. The baseline row itself shows a ratio of 1. A cell that
  was not measured stays blank, and a column the baseline row leaves
  out shows times without ratios.

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
  cellWidth = 22
  out = []
  header = 'impl'.ljust(labelWidth)
  for col in cols:
    header = '%s  %s' % (header, col.center(cellWidth))
  out.append(header)
  out.append('-' * len(header))
  for row in rows:
    line = row.ljust(labelWidth)
    for col in cols:
      if (row, col) not in cells:
        line = '%s  %s' % (line, ''.center(cellWidth))
        continue
      seconds = cells[(row, col)]
      if (baseline, col) in cells:
        ratio = seconds / cells[(baseline, col)]
        cell = '%s  x%6.1f' % (formatTime(seconds), ratio)
      else:
        cell = formatTime(seconds)
      line = '%s  %s' % (line, cell.center(cellWidth))
    out.append(line)
  out.append('')
  out.append('ratios are against the %r row.' % baseline)
  return '\n'.join(out)

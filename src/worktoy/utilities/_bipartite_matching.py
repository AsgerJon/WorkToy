"""
The 'bipartiteMatching' function matches each slot to a distinct candidate
index.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, TypeAlias

  SlotInts: TypeAlias = dict[Any, tuple[int, ...]]
  SlotMap: TypeAlias = dict[Any, int]


def bipartiteMatching(slots: list[tuple[int, ...]]) -> list[int]:
  """Solve bipartite matching by recursive backtracking.

  At each step, the slot with the fewest remaining candidates is
  expanded first (MRV heuristic); each chosen value is removed
  from every other slot's candidate set before recursing.

  Parameters
  ----------
  slots : list of tuple of int
      'slots[i]' lists the indices that may be assigned to
      slot 'i'.

  Returns
  -------
  list of int
      Assigned index per slot, in the original slot order. Each
      returned index is unique across the list.

  Raises
  ------
  ValueError
      If no consistent assignment exists.

  Examples
  --------
  >>> bipartiteMatching([(0, 1), (0,), (1, 2)])
  [1, 0, 2]
  """
  # Base case: success
  if not slots:
    return []

  # Step 1: fail if any empty
  for opts in slots:
    if not opts:
      raise ValueError('No valid assignment for slot')

  # Step 2: pick slot with fewest options
  idx, opts = min(enumerate(slots), key=lambda x: len(x[1]))

  # Step 3: try each option
  for value in opts:
    # Build reduced slots
    reduced = []
    for j, otherOpts in enumerate(slots):
      if j == idx:
        continue
      reducedOpts = tuple(v for v in otherOpts if v != value)
      reduced.append(reducedOpts)
    try:
      result = bipartiteMatching(reduced)
    except ValueError:
      continue
    # Rebuild full result
    result = result[:idx] + [value] + result[idx:]
    return result

  raise ValueError('No valid assignment for slot %d' % idx)

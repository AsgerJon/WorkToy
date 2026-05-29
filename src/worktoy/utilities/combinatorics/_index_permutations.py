"""
The 'indexPermutations' function yields the permutations of
'(0, 1, ..., n - 1)'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Iterator

  Indices: TypeAlias = tuple[int, ...]


def indexPermutations(n: int) -> Iterator[Indices]:
  """Yield every permutation of '(0, 1, ..., n - 1)'.

  Parameters
  ----------
  n : int
      The number of positions. Must be non-negative.

  Yields
  ------
  ordering : tuple of int
      A permutation of '(0, 1, ..., n - 1)'. There are 'n!' of them,
      yielded in lexicographic order.

  Raises
  ------
  ValueError
      If 'n' is negative.

  Examples
  --------
  >>> list(indexPermutations(3))
  [(0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0)]
  """
  if n < 0:
    raise ValueError('n must be non-negative')

  def _go(src: tuple[int, ...]) -> Iterator[Indices]:
    if not src:
      yield ()
      return
    for j, t in enumerate(src):
      sub = (*src[:j], *src[j + 1:])
      for recursive in _go(sub):
        yield (t, *recursive)

  yield from _go((*range(n),))

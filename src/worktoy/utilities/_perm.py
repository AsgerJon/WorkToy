"""
perm: Efficient unique permutation generator.

This module provides the function `perm`, which yields all unique
permutations of its input arguments. The function works efficiently even
when the input contains duplicate elements, producing each unique ordering
exactly once.

Usage example:
  for p in perm('Tom', 'Tom', 'Harry'):
    print(p)
  # Outputs:
  # ('Tom', 'Tom', 'Harry')
  # ('Tom', 'Harry', 'Tom')
  # ('Harry', 'Tom', 'Tom')

The generator approach allows iteration over permutations without building
the entire result list in memory, making it suitable for large or memory-
constrained applications.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Iterator, TypeAlias, Union, Optional

  Permutations: TypeAlias = tuple[Any, ...]
  Indices: TypeAlias = tuple[int, ...]
  IndexedPermutation: TypeAlias = tuple[Permutations, Indices]
  IndexedPermutations: TypeAlias = tuple[IndexedPermutation, ...]
  _PermutationsIndices: TypeAlias = Iterator[IndexedPermutation]


def _permutationsIndices(*items: Any) -> _PermutationsIndices:
  if not items:
    yield (), ()
  seen = []
  if len(items) == 1:
    seen.append(items)
    yield items, (0,)
  for j, t in enumerate(items):
    recursive = _permutationsIndices(*items[:j], *items[j + 1:])
    for r in recursive:
      p0, i0 = r
      shifted = tuple((k + 1) if k >= j else k for k in i0)
      p = (t, *p0)
      i = (j, *shifted)
      if p in seen:
        continue
      seen.append(p)
      yield p, i


def _intPerm(n: int) -> Iterator[Indices]:
  def _go(src: tuple[int, ...]) -> Iterator[Indices]:
    if not src:
      yield ()
      return
    for j, t in enumerate(src):
      sub = (*src[:j], *src[j + 1:])
      for recursive in _go(sub):
        yield (t, *recursive)

  yield from _go((*range(n),))


def perm(*items: Any) -> Permutations:
  """Yield unique permutations of items.

  For inputs containing repeated elements, identical values are not
  double-counted: the number of yielded permutations equals the multinomial
  coefficient `N! / (k_1! * k_2! * ... * k_n!)` where `k_i` is the
  multiplicity of the `i`-th distinct value.

  Parameters
  ----------
  *items : Any
      The elements to permute. Hashable values are required for
      deduplication.

  Yields
  ------
  permutation : tuple of Any
      A permutation of `items`, of length `len(items)`.
  """
  allIndices = _intPerm(len(items))
  out = []
  seen = []
  for indices in allIndices:
    permutation = (*(items[i] for i in indices),)
    if permutation in seen:
      continue
    seen.append(permutation)
    out.append(permutation)
  return (*out,)


def permTraced(*items: Any) -> IndexedPermutations:
  """Yield unique permutations of items paired with original-index mappings.

  For inputs containing repeated elements, identical values are not
  double-counted: the number of yielded permutations equals the multinomial
  coefficient `N! / (k_1! * k_2! * ... * k_n!)` where `k_i` is the
  multiplicity of the `i`-th distinct value. The accompanying index tuple
  will disambiguate which original position contributed each slot, even when
  element values coincide.

  Parameters
  ----------
  *items : Any
      The elements to permute. Hashable values are required for
      deduplication.

  Yields
  ------
  permutation : tuple of Any
      A permutation of `items`, of length `len(items)`.
  indices : tuple of int
      The original positions in `items` corresponding to each slot of
      `permutation`. Satisfies `items[indices[k]] is permutation[k]` for
      every `k`, and `sorted(indices) == list(range(len(items)))`.

  See Also
  --------
  perm : Yields permutations only, discarding the index tuples.

  Examples
  --------
  >>> list(permTraced('A', 'A', 'B'))
  [(('A', 'A', 'B'), (0, 1, 2)),
   (('A', 'B', 'A'), (0, 2, 1)),
   (('B', 'A', 'A'), (2, 0, 1))]
  """
  allIndices = _intPerm(len(items))
  out = []
  seen = []
  for indices in allIndices:
    permutation = (*(items[i] for i in indices),)
    if permutation in seen:
      continue
    seen.append(permutation)
    out.append((permutation, indices))
  return (*out,)

"""Combinatorial utilities for ``worktoy``.

Provides ``indexPermutations`` for raw index-tuple permutations,
``Arrangement`` for a single permutation paired with its inverse,
and ``Arrangements`` for the deduplicated set of all permutations
of a ground tuple."""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from ._index_permutations import indexPermutations
from ._arrangement import Arrangement
from ._arrangements import Arrangements

__all__ = (
  'indexPermutations',
  'Arrangement',
  'Arrangements',
)

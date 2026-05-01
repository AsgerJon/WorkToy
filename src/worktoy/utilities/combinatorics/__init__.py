"""
The 'worktoy.utilities.combinatorics' package provides combinatorial
utilities for the 'worktoy' library, including functions for generating
permutations and combinations of elements, as well as related tools for
working with combinatorial structures.
"""
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

"""
The 'worktoy.core' module provides the most primitive objects used by the
'worktoy' library.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from ._some import Some
from ._factorial import factorial
from ._permutate import permutate
from ._unpack import unpack
from ._bipartite_matching import bipartiteMatching

__all__ = [
    'Some',
    'factorial',
    'permutate',
    'unpack',
    'bipartiteMatching',
]

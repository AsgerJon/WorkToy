"""
The 'worktoy.dispatch' package provides the overload functionality used
across the 'worktoy' library. It provides the central 'Dispatcher'
class which facilitates mapping from type signatures to function
objects.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from ._flex_call import flexCall, isFlex
from ._call_me_maybe import CallMeMaybe
from ._permuter import Permuter
from ._permuter_method import PermuterMethod
from ._type_sig import TypeSig
from ._dispatcher import Dispatcher
from ._overload import overload

__all__ = [
  'flexCall',
  'isFlex',
  'CallMeMaybe',
  'Permuter',
  'PermuterMethod',
  'TypeSig',
  'Dispatcher',
  'overload',
]

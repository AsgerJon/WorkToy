"""
The 'worktoy.dispatch' package provides the machinery for type-signature
based function overloading, not a ready-to-use overloading facility on its
own. The 'overload' decorator only records signatures; turning those into
live dispatch happens one layer up, where 'BaseMeta' in 'worktoy.mcls'
compiles them into a 'Dispatcher' during class construction. Use these
tools through a 'BaseObject' subclass, or wire a 'Dispatcher' onto a class
by hand.

- flexCall, isFlex
- CallMeMaybe
- Permuter, PermuterMethod
- TypeSig
- Dispatcher
- overload
"""
#  Apache-2.0 license
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

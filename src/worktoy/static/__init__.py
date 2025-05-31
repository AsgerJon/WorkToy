"""The 'worktoy.static' module provides low level parsing and casting
utilities. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

#  Private classes
from ._current_instance import _CurrentInstance
from ._current_owner import _CurrentOwner

#  Public classes
from ._item_call import ItemCall
from ._hist_dict import HistDict

#  Sub modules
from . import casting
from . import zeroton

#  Public classes
from ._abstract_object import AbstractObject  # Depends on zeroton
from ._alias import Alias
from ._pre_class import PreClass

#  Overloading classes
from ._type_sig import TypeSig
from ._dispatch import Dispatch
from ._overload import overload

__all__ = [
    'ItemCall',
    'HistDict',
    'AbstractObject',
    'Alias',
    'PreClass',
    'casting',
    'zeroton',
    'TypeSig',
    'Dispatch',
    'overload',
]

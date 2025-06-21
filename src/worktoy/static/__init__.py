"""The 'worktoy.static' module provides low level parsing and casting
utilities. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

#  Private classes
from ._current_instance import _CurrentInstance, _InstanceAddress
from ._current_owner import _CurrentOwner, _OwnerAddress
from ._current_module import _CurrentModule
from ._current_class import _CurrentClass

#  Public classes
from ._item_call import ItemCall
from ._hist_dict import HistDict

#  Submodules
# from . import casting
from . import zeroton

#  Public classes
from ._abstract_object import AbstractObject  # Depends on zeroton

#  Private classes
from ._attribute import _Attribute  # Depends on AbstractObject
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
    'zeroton',
    'TypeSig',
    'Dispatch',
    'overload',
]

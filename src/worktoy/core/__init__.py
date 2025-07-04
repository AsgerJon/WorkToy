"""
The 'worktoy.core' module provides the most primitive objects used by the
'worktoy' library.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from . import sentinels
from ._instance import ContextInstance
from ._owner import ContextOwner
from ._caller import ContextCaller
from ._meta_type import MetaType
from ._meta_object import MetaObject
from ._object import Object

__all__ = [
    'sentinels',
    'ContextInstance',
    'ContextOwner',
    'ContextCaller',
    'MetaType',
    'MetaObject',
    'Object',
]

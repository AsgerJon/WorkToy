"""
The 'worktoy.core' package provides the primitive runtime types that the
metaclass framework and the descriptor layer build on.

- MetaType
- Object
- ContextInstance, ContextOwner
- sentinels
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from . import sentinels
from ._instance_owner import ContextInstance, ContextOwner
from ._meta_type import MetaType
from ._object import Object

__all__ = [
  'sentinels',
  'ContextInstance',
  'ContextOwner',
  'MetaType',
  'Object',
]

"""The 'worktoy.attr' module implements the descriptor protocol."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

#  Private descriptors for top-level instance and owner
from ._top_objects import _TopInstance, _TopOwner

#  Public descriptors for AttriBox and Field
from ._field import Field
from ._attri_box import AttriBox
from ._nest_box import NestBox

__all__ = [
    'Field',
    'AttriBox',
    'NestBox',
]

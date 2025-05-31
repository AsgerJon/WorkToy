"""The 'worktoy.attr' module implements the descriptor protocol."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from ._field_properties import _FieldProperties, _flexSet, _flexDelete
from ._field import Field
from ._wait_for_it import WaitForIt
from ._abstract_box import AbstractBox
from ._attri_box import AttriBox
from ._flex_box import FlexBox

__all__ = [
    'Field',
    'WaitForIt',
    'AbstractBox',
    'AttriBox',
    'FlexBox',
]

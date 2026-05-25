"""
The 'worktoy.desc' module provides the base descriptor classes. This
module introduces a novel concept: descriptor-context.

When a descriptor is accessed through the owning class, the descriptor
object itself returns. When through an instance, the descriptor usually
performs the relevant accessor function as appropriate for the instance
received. This module expands this concept by introducing the
descriptor-context.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from ._fast_box import FastBox
from ._base_descriptor import BaseDescriptor
from ._alias import Alias
from ._field import Field
from ._attri_box import AttriBox
from ._fix_box import FixBox
from ._symbolic_name import SymbolicName

__all__ = [
  'FastBox',
  'BaseDescriptor',
  'Alias',
  'Field',
  'AttriBox',
  'FixBox',
  'SymbolicName',
]

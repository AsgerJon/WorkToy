"""
The 'worktoy.desc' package provides the base descriptor classes. It
introduces the descriptor-context: during an access the active
'(instance, owner)' pair is recorded on the descriptor, so accessor
hooks can read the current instance and owner instead of receiving
them as arguments.

Accessed through the owning class, a descriptor returns itself.
Accessed through an instance, it runs the accessor appropriate for
that instance. See 'Object' in 'worktoy.core' for the full
descriptor-context machinery.

- FastBox
- BaseDescriptor
- Alias
- Field
- AttriBox
- FixBox
- SymbolicName
"""
#  Apache-2.0 license
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

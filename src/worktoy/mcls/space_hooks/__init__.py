"""
The 'worktoy.mcls.space_hooks' package provides the hooks that make the
worktoy namespace programmable. A hook is declared in a namespace
subclass body and opts into one or more phases of class construction:
prepare, set-item, get-item, pre-compile, post-compile, and new-class.
'AbstractSpaceHook' defines the phase protocol; the concrete hooks each
handle one job, and 'LoadSpaceHook' is where stacked 'overload'
declarations are assembled into 'Dispatcher' objects.

- SpaceDesc
- ReservedNames
- AbstractSpaceHook
- FlexCallHook
- ReservedNamespaceHook
- NamespaceHook
- LoadSpaceHook
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from ._space_desc import SpaceDesc
from ._reserved_names import ReservedNames
from ._abstract_space_hook import AbstractSpaceHook
from ._flex_call_hook import FlexCallHook
from ._reserved_namespace_hook import ReservedNamespaceHook
from ._name_hook import NamespaceHook
from ._load_space_hook import LoadSpaceHook

__all__ = [
  'SpaceDesc',
  'ReservedNames',
  'AbstractSpaceHook',
  'FlexCallHook',
  'ReservedNamespaceHook',
  'NamespaceHook',
  'LoadSpaceHook',
]

"""
The 'worktoy.mcls.space_hooks' package provides the hooks used by the
Namespace system.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from ._reserved_names import ReservedNames
from ._abstract_space_hook import AbstractSpaceHook
from ._reserved_name_hook import ReservedNameSpaceHook
from ._pre_class_hook import PreClassSpaceHook
from ._overload_hook import OverloadSpaceHook
from ._name_hook import NameSpaceHook

__all__ = [
    'ReservedNames',
    'AbstractSpaceHook',
    'ReservedNameSpaceHook',
    'PreClassSpaceHook',
    'OverloadSpaceHook',
    'NameSpaceHook',
]

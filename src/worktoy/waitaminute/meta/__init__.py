"""The 'worktoy.waitaminute.meta' package collects the exceptions raised
during class creation by the metaclass machinery in 'worktoy.mcls' (and
the primitive metaclasses in 'worktoy.core'). They cover near-miss dunder
names, illegal '__del__', reserved names, hook conflicts, and illegal
instantiation.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from ._illegal_instantiation import IllegalInstantiation
from ._hook_exception import HookException
from ._duplicate_hook import DuplicateHook
from ._del_exception import DelException
from ._questionable_syntax import QuestionableSyntax
from ._reserved_name import ReservedName

__all__ = [
  'DuplicateHook',
  'IllegalInstantiation',
  'HookException',
  'DelException',
  'QuestionableSyntax',
  'ReservedName',
]

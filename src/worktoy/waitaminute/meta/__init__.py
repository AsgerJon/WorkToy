"""The 'worktoy.waitaminute.meta' package collects the exceptions raised
during class creation by the metaclass machinery in 'worktoy.mcls' (and
the primitive metaclasses in 'worktoy.core'). They cover near-miss dunder
names, illegal '__del__', reserved names, hook conflicts, a name both
overloaded and defined plainly in one class body, the deletion of a name
a hook claimed, a class hook the metaclass never calls, a second
sentinel at a taken name, illegal instantiation, and a disallowed
attribute in the class body of a control-flow signal.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from ._illegal_instantiation import IllegalInstantiation
from ._hook_exception import HookException
from ._duplicate_hook import DuplicateHook
from ._del_exception import DelException
from ._questionable_syntax import QuestionableSyntax
from ._reserved_name import ReservedName
from ._unbound_class_hook import UnboundClassHook
from ._overload_conflict import OverloadConflict
from ._claimed_name import ClaimedName
from ._shadowed_class_hook import ShadowedClassHook
from ._duplicate_sentinel import DuplicateSentinel
from ._control_class_error import ControlClassError

__all__ = [
  'DuplicateHook',
  'IllegalInstantiation',
  'HookException',
  'DelException',
  'QuestionableSyntax',
  'ReservedName',
  'UnboundClassHook',
  'OverloadConflict',
  'ClaimedName',
  'ShadowedClassHook',
  'DuplicateSentinel',
  'ControlClassError',
]

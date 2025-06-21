"""
The 'worktoy.attr.accessor_hooks' module provides notifying hooks for the
descriptors based on the 'worktoy.attr.AbstractDescriptor' base class and
its subclasses.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from ._hook_phases import HookPhase

from ._abstract_descriptor_hook import AbstractDescriptorHook
from ._caching_hook import CachingHook
from ._weak_box import WeakBox
from ._strong_box import StrongBox

__all__ = [
    'HookPhase',
    'AbstractDescriptorHook',
    'CachingHook',
    'WeakBox',
    'StrongBox',
]

"""
The 'worktoy.attr.accessor_hooks' module provides notifying hooks for the
descriptors based on the 'worktoy.attr.AbstractDescriptor' base class and
its subclasses.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from ._priority import _Priority  # Private
from ._abstract_descriptor_hook import AbstractDescriptorHook

__all__ = [
    'AbstractDescriptorHook',
]

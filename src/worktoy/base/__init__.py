"""The 'worktoy.base' package exposes advanced functionality from the
remaining worktoy packages through base classes. The suggested use case is
to inherit from the classes: BaseObject and FastObject.

The BaseObject class expands the standard 'object' base class with support
for function overloading. Any class should be able to inherit from this
class instead of from 'object'.

The FastObject similarly supports function overloading, but restricts the
use of attributes to instances of AttriBox. This allows for significant
performance improvements, whilst retaining the deferred attribute
instantiation provided by AttriBox. Please note however, that FastObject
classes do not in fact own instances of AttriBox after creation. The
metaclass protocol uses the AttriBox instances when creating the classes,
but does not actually pass them on to the created classes.
"""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from ._illegal_attribute_exception import IllegalAttributeException

from ._base_object import BaseObject
from ._fast_space import FastSpace
from ._fast_meta import FastMeta
from ._fast_object import FastObject
from ._overload import overload

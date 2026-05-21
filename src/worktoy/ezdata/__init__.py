"""
The 'worktoy.ezdata' package provides 'EZData', a dataclass-style
base class with auto-generated construction, equality, iteration,
hashing, ordering, and conversion methods, plus a '__post_init__'
hook.

Public surface:

- 'EZData' : the base class users subclass to declare a dataclass.
- 'EZField' : the per-field descriptor; spell as 'EZField[T](...)'.
- 'fields(obj)' : free function returning the EZField tuple for a
  class or instance, mirroring 'dataclasses.fields'.
- 'EZMeta', 'EZSpace', 'EZHook' : the metaclass, namespace, and
  space hook that drive class construction. Exposed for users
  building their own auto-generating bases against the same shape.

See 'worktoy.waitaminute.ezdata' for the typed exceptions raised
by the package.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from ._ez_field import EZField
from ._ez_hook import EZHook
from ._ez_space import EZSpace
from ._ez_meta import EZMeta
from ._ez_data import EZData
from ._fields import fields

__all__ = (
  'EZField',
  'EZHook',
  'EZSpace',
  'EZMeta',
  'EZData',
  'fields',
)

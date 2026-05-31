"""
The 'worktoy.mcls' package provides the base custom metaclass and
namespace uses across the 'worktoy' library. The pattern used is for the
namespace class to implement a method called 'compile' which decides the
actual namespace to be used in the class creation based on the code found
during execution of the class body.

The metaclass instantiates the namespace class and returns the created
namespace object from the '__prepare__' method. Upon completion of the
class body execution this namespace object is passed back to the metaclass
in the '__new__' method. The namespace object is required to implement a
method called 'compile' which returns an instance of 'dict'. The
metaclass passes that 'dict' to 'type.__new__'; per-name validation
(reserved names, near-miss dunders) happens earlier, during class-body
execution, through the namespace hooks. Before returning the created
class, the
metaclass calls '__subclasshook__' on each base class, passing the
created class. The return value is ignored, so a base cannot modify
the class; it can only reject the class by raising an exception from
'__subclasshook__'. Finally, the metaclass returns the created class
object.

- space_hooks
- AbstractNamespace
- AbstractMetaclass
- BaseSpace
- BaseMeta
- BaseObject
"""
#  Apache-2.0 license
#  Copyright (c) 2024-2026 Asger Jon Vistisen
from __future__ import annotations

from . import space_hooks  # Public sub package
from ._abstract_namespace import AbstractNamespace
from ._abstract_metaclass import AbstractMetaclass
from ._base_space import BaseSpace
from ._base_meta import BaseMeta
from ._base_object import BaseObject

__all__ = [
  'space_hooks',
  'AbstractNamespace',
  'AbstractMetaclass',
  'BaseSpace',
  'BaseMeta',
  'BaseObject',
]

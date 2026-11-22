"""
The 'worktoy.mcls' package provides the base custom metaclass and
namespace used across the 'worktoy' library. The pattern used is for the
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
class, the metaclass calls '__subclasshook__' on each base class,
passing the created class. The return value is ignored, so a base cannot
modify the class; it can only reject the class by raising an exception
from '__subclasshook__'. Finally, the metaclass returns the created
class object.

A class whose metaclass comes from another library takes a metaclass
combined with one of these. A base built by Python's 'abc.ABCMeta', such
as 'abc.ABC', listed beside 'BaseObject' raises Python's metaclass
conflict, since that metaclass is outside the 'MetaType' family; a
metaclass based on both, as 'class Both(BaseMeta, abc.ABCMeta)', builds
the class, with the abstract methods of 'abc' and its overloads.

The 'ABCMeta' of this package is worktoy's own, and no relative of that
one. It builds the classes that declare methods with '@abstract' of
'worktoy.dispatch', holds each subclass to what is declared, one
signature of an overloaded name at a time, and refuses to make an
object of a class that still lacks an implementation.

- space_hooks
- AbstractNamespace
- AbstractMetaclass
- BaseSpace
- BaseMeta
- BaseObject
- ABCSpace
- ABCMeta
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
from ._abc_space import ABCSpace
from ._abc_meta import ABCMeta

__all__ = [
  'space_hooks',
  'AbstractNamespace',
  'AbstractMetaclass',
  'BaseSpace',
  'BaseMeta',
  'BaseObject',
  'ABCSpace',
  'ABCMeta',
]

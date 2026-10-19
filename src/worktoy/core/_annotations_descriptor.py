"""
_AnnotationsDescriptor is a private class for the 'worktoy.core' package
used by 'MetaType' to ensure compatibility with the behaviour of the
'type.__dict__['__annotations__'].__get__' method.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from types import GetSetDescriptorType as GSD

from ..utilities import maybe

if TYPE_CHECKING:
  from typing import Any, Optional, Type, TypeAlias

  Annotations: TypeAlias = Optional[dict[str, Any]]

#  'type' carries a descriptor for '__annotations__' from Python 3.10 on;
#  before that 'cls.__annotations__' is a plain lookup through the class's
#  own resolution order, falling through to a base for every class, and
#  'MetaType' installs nothing.
typeAnnDesc: Any = type.__dict__.get('__annotations__', None)
HAS_TYPE_ANNOTATIONS: bool = True if typeAnnDesc is not None else False


class _AnnotationsDescriptor:
  """
  _AnnotationsDescriptor is a private class for the 'worktoy.core' package
  used by 'MetaType' to ensure compatibility with the behaviour of the
  'type.__dict__['__annotations__'].__get__' method. 'MetaType.__new__'
  installs it on every metaclass whose body carries annotations, in
  place of the eager dict the future import leaves there: read on a
  class it defers to the descriptor of 'type', so the class answers for
  itself, and read on the metaclass it answers the metaclass's own
  annotations, which 'type' honours by calling '__get__' with no class.
  """

  __meta_annotations__: Annotations = None

  def __init__(self, metaAnnotations: Annotations = None) -> None:
    self.__meta_annotations__ = metaAnnotations

  def __get__(self, cls: Any, owner: Optional[Type] = None) -> Any:
    """
    This method is a descriptor that returns the annotations of the owner
    class when accessed through an instance or the class itself.
    """
    if cls is None:
      return self.__meta_annotations__
    mcls: type = maybe(owner, type(cls))
    return GSD.__get__(typeAnnDesc, cls, mcls)

  def __set__(self, cls: Any, value: Annotations) -> None:
    """
    This method is a descriptor that sets the annotations of the owner
    class when accessed through an instance or the class itself.
    """
    GSD.__set__(typeAnnDesc, cls, value)

  def __delete__(self, cls: Any) -> None:
    """
    This method is a descriptor that deletes the annotations of the owner
    class when accessed through an instance or the class itself.
    """
    GSD.__delete__(typeAnnDesc, cls)

  __objclass__: Optional[Type] = type

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

typeAnnDesc: GSD = type.__dict__['__annotations__']


class _AnnotationsDescriptor:
  """
  _AnnotationsDescriptor is a private class for the 'worktoy.core' package
  used by 'MetaType' to ensure compatibility with the behaviour of the
  'type.__dict__['__annotations__'].__get__' method.
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

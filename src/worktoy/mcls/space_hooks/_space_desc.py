"""
SpaceDesc is the descriptor exposing the namespace to an
'AbstractSpaceHook'.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, overload, Generic, TypeVar

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any, Union, Self

  from . import AbstractSpaceHook as Hook

NamespaceT = TypeVar('NamespaceT')


class SpaceDesc(Generic[NamespaceT]):
  """
  A hook method must reach the namespace whose class body it is working
  on, and one hook object serves every namespace of its class.

  Implementation
  --------------

  Through a hook, the descriptor returns '__space_object__', the
  namespace that last read the hook; through the class, itself.
  """

  # @formatter:off
  @overload
  def __get__(self, instance: None, owner: type) -> Self: ...
  @overload
  def __get__(self, instance: Hook, owner: type) -> NamespaceT: ...
  # @formatter:on

  def __get__(self, instance: Any, owner: type) -> Union[Self, NamespaceT]:
    """
    Accessed on a hook instance, '__get__' returns the namespace object
    bound to that hook; accessed on the class, it returns the descriptor
    itself.
    """
    if instance is None:
      return self
    return object.__getattribute__(instance, '__space_object__')

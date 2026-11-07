"""
SpaceDesc is the descriptor exposing the namespace to an
'AbstractSpaceHook'.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

import threading
from typing import TYPE_CHECKING, overload, Generic, TypeVar

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any, Optional, Union, Self

  from . import AbstractSpaceHook as Hook

NamespaceT = TypeVar('NamespaceT')


class _ThreadSpaces(threading.local):
  """
  The namespace each hook is bound to, kept per thread. A hook is one
  object on its namespace class, shared by every class statement that
  runs under that class, and the namespace reads it anew before every
  phase, binding it to itself. Two threads running class statements at
  once would otherwise bind the same hook in turn, and a phase of one
  thread would read the namespace of the other, finding names it never
  bound and registering overloads in a body not its own. Kept per
  thread, a binding is seen only by the thread that made it.

  Implementation
  --------------

  'bound' maps 'id(hook)' to '(hook, namespace)'. The hook is held in the
  entry so that its 'id' stays taken for as long as the entry exists,
  and a new hook can never find the namespace of a dead one under a
  reused 'id'; nothing reads the held hook. Entries are replaced at every
  binding and never dropped, as the binding on the hook itself was never
  cleared before: a hook keeps the last namespace it worked for, per
  thread now rather than once for all threads.
  """

  def __init__(self) -> None:
    """Give the thread an empty mapping on its first use"""
    self.bound: dict[int, tuple[Any, Any]] = {}


_THREAD = _ThreadSpaces()


class SpaceDesc(Generic[NamespaceT]):
  """
  A hook method must reach the namespace whose class body it is working
  on, and one hook object serves every namespace of its class, from
  whichever thread a class statement runs in.

  Implementation
  --------------

  Through a hook, the descriptor returns the namespace the hook was last
  bound to in the current thread, or 'None' before any binding; through
  the class, itself. A write through a hook binds it, in the current
  thread alone.
  """

  # @formatter:off
  @overload
  def __get__(self, instance: None, owner: type) -> Self: ...
  @overload
  def __get__(self, instance: Hook, owner: type) -> NamespaceT: ...
  # @formatter:on

  def __get__(self, instance: Any, owner: type) -> Union[Self, NamespaceT]:
    """
    Accessed on a hook instance, '__get__' returns the namespace bound to
    that hook in the current thread; accessed on the class, it returns
    the descriptor itself.
    """
    if instance is None:
      return self
    entry: Optional[tuple[Any, Any]] = _THREAD.bound.get(id(instance))
    if entry is None:
      return None
    return entry[1]

  def __set__(self, instance: Hook, value: NamespaceT) -> None:
    """
    A write binds the hook to the namespace, in the current thread.
    """
    _THREAD.bound[id(instance)] = (instance, value)

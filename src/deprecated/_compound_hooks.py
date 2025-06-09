"""
CompoundHooks provides an array of 'AbstractDescriptorHook' objects owned
by 'AbstractDescriptor' objects.

"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from random import shuffle

from ...parse import maybe
from ...static import AbstractObject
from . import AbstractDescriptorHook as Hook

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Self, TypeAlias, Iterator

  Hooks: TypeAlias = tuple[Hook, ...]
  HookList: TypeAlias = list[Hook]


class CompoundHooks(AbstractObject):
  """
  CompoundHooks provides an array of 'AbstractDescriptorHook' objects owned
  by 'AbstractDescriptor' objects.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Fallback Variables

  #  Private Variables
  __accessor_hooks__ = None
  __iter_contents__ = None

  #  Public Variables

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _getAccessorHooks(self) -> Hooks:
    """Get the accessor hooks."""
    return maybe(self.__accessor_hooks__, ())

  def _getOrderedHooks(self, ) -> HookList:
    """
    Get the ordered hooks.

    This method returns the hooks sorted by priority in descending order.
    """
    hooks = self._getAccessorHooks()
    return [*sorted(hooks, key=lambda h: h.priority, ), ]

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _addAccessorHook(self, hook: Hook) -> Self:
    """Add an accessor hook."""
    existing = self.__accessor_hooks__
    self.__accessor_hooks__ = (*existing, hook)
    return self

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __iter__(self) -> Self:
    """
    Yields hooks in order of priority with hooks of same priority randomly
    chosen.
    """
    hooks = self._getAccessorHooks()
    priorityMap = dict()
    for hook in hooks:
      existing = priorityMap.get(hook.priority, [])
      existing.append(hook)
      priorityMap[hook.priority] = existing
    self.__iter_contents__ = []
    priorities = sorted(priorityMap.keys(), reverse=True)
    for p in priorities:
      self.__iter_contents__.extend(priorityMap[p])
    return self

  def __next__(self, ) -> Hook:
    """
    Returns the next hook in the iteration. If there are no more hooks,
    raises StopIteration.
    """
    if self.__iter_contents__:
      return self.__iter_contents__.pop(0)
    self.__iter_contents__ = None
    raise StopIteration

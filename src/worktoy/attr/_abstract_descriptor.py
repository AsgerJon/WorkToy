"""
AbstractDescriptor provides the base class for descriptors in the
'worktoy.attr' module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from random import shuffle

from ..parse import maybe
from ..static import AbstractObject
from ..waitaminute import MissingVariable

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Self, TypeAlias, Any
  from .accessor_hooks import AbstractDescriptorHook as Hook

  Hooks: TypeAlias = dict[str, Hook]
  HookList: TypeAlias = list[Hook]


class AbstractDescriptor(AbstractObject):
  """
  'AbstractDescriptor' inherits descriptor protocol implementation from
  'AbstractObject' and enhances it with a hook system surrounding each
  accessor method. These hooks are class specific and thus set with
  classmethod 'addAccessorHook'. The intended use is for hook classes to
  register themselves during '__set_name__'.

  The control flow dispatches hooks in order determined by their priority
  attribute from low to high. Tie-breakers are intentionally given fuzzy
  ordering to avoid undefined deterministic behaviour concealing errors.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Fallback Variables

  #  Private Variables
  __accessor_hooks__ = None

  #  Public Variables

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def _getAccessorHooks(cls) -> Hooks:
    """Get the accessor hooks."""
    return maybe(cls.__accessor_hooks__, dict())

  @classmethod
  def getOrderedHooks(cls, ) -> HookList:
    """
    Returns the hooks in order of descending priority. Hooks with the same
    priority are returned in random order (via shuffle). Lower numeric
    priority values are considered more urgent.
    """
    accessorHooks = cls._getAccessorHooks()
    priorityMap = dict()
    priorities = [h.priority for n, h in accessorHooks.items()]
    priorities = sorted(list(set(priorities)), reverse=True)
    out = []
    for name, hook in accessorHooks.items():
      if hook.priority not in priorityMap:
        priorityMap[hook.priority] = [hook, ]
        continue
      priorityMap[hook.priority].append(hook)
    for p, hooks in priorityMap.items():
      shuffle(hooks)
      out.extend(hooks)
    return out

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def registerAccessorHook(cls, name: str, hook: Hook) -> Self:
    """
    Adds the given hook at the given name. This is meant to be invoked by
    '__set_name__' on the hook class.
    """
    hooks = cls._getAccessorHooks()
    if name in hooks:
      raise NotImplementedError('Duplicate hook names lmao')
    hooks[name] = hook
    cls.__accessor_hooks__ = hooks
    return cls

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __get__(self, instance: Any, owner: Any, **kwargs) -> Any:
    """
    Reimplementation preserving the 'updateContext' call and return of
    'self' when accessed on class (instance is None). Invokes hooks
    before and after '__instance_get__' method.
    """
    self.updateContext(instance, owner, **kwargs)
    if instance is None:
      return self
    hooks = self.getOrderedHooks()
    #  Pre hooks
    preValue = None
    for hook in hooks:
      val = hook.__pre_get__()
      if val is not None:
        if preValue is None:
          preValue = val
          continue
        raise NotImplementedError('TODO: Multiple pre-get values')
    #  Collect value from pre hooks or from instance
    if preValue is None:
      value = self.__instance_get__(**kwargs)
    else:
      value = preValue
    #  Post hooks
    for hook in hooks:
      postValue = hook.__post_get__(value)
      if postValue is not None:
        return postValue
    return value

  def __set__(self, instance: Any, value: Any, **kwargs) -> None:
    """
    Reimplementation preserving the 'updateContext' call and invoking
    hooks before and after '__instance_set__' method.
    """
    self.updateContext(instance, **kwargs)
    hooks = self.getOrderedHooks()
    #  Pre hooks
    preValue = None
    for hook in hooks:
      val = hook.__pre_set__(value, )
      if val is not None:
        if preValue is None:
          preValue = val
          continue
        raise NotImplementedError('TODO: Multiple pre-set values')
    if preValue is not None:
      return self.__instance_set__(preValue, **kwargs)
    #  Collect old value or MissingValue exception
    try:
      oldVal = self.__instance_get__()
    except AttributeError as missingValue:
      oldVal = missingValue
    #  Return 'None' if value is identical to old value
    if value is oldVal:
      return
    #  Post hooks
    postValue = None
    for hook in hooks:
      val = hook.__post_set__(value, oldVal)
      if val is not None:
        if postValue is not None:
          raise NotImplementedError('TODO: Multiple post-set values')
        postValue = val
    if postValue is None:
      return self.__instance_set__(value, **kwargs)
    return self.__instance_set__(postValue, **kwargs)

  def __delete__(self, instance: Any, **kwargs) -> None:
    """
    Reimplementation preserving the 'updateContext' call and invoking
    hooks before '__instance_delete__' method.
    """
    self.updateContext(instance, **kwargs)
    hooks = self.getOrderedHooks()
    for hook in hooks:
      hook.__pre_delete__()
    try:
      oldValue = self.__instance_get__(**kwargs)
    except MissingVariable as missingVariable:
      raise AttributeError from missingVariable
    for hook in hooks:
      hook.__post_delete__(oldValue)
    return self.__instance_delete__(**kwargs)

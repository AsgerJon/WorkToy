"""
AbstractDescriptorHook defines the hooks surrounding the accessor
functions in the 'worktoy.attr.AbstractDescriptor' class.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from warnings import warn

from ...static import AbstractObject
from ...text import stringList
from ...waitaminute import SubclassException

from .. import AbstractDescriptor

from . import _Priority

#  Below provides compatibility back to Python 3.7
try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, Optional, TypeAlias, Union


class AbstractDescriptorHook(AbstractObject):
  """
  AbstractDescriptorHook defines the hooks surrounding the accessor
  functions in the 'worktoy.attr.AbstractDescriptor' class.

  Note the 'None-means-no-change' convention: if a hook returns a value
  other than 'None', it replaces the value being handled by the accessor.
  Returning 'None' leaves the value unchanged. AbstractDescriptor explicitly
  disallows 'None' as a valid value, except for the above.

  The AbstractDescriptor class wraps three core accessor methods meant to
  be reimplemented by subclasses:

    Getter:  __instance_get__(self) -> Any
    Setter:  __instance_set__(self, value: Any) -> None
    Deleter: __instance_delete__(self) -> None

  Because hooks have access to the descriptor object, and the descriptor
  tracks both instance and owner, hook methods do not receive these as
  explicit arguments.

  Accessor control flows are defined as follows:

  Getter Flow:
    preValue = None
    for hook in hooks:
      result = __pre_get__(hook)
      if result is not None:
        if preValue is not None:
          raise HookConflict("Multiple pre-get overrides")
        preValue = result

    if preValue is None:
      value = __instance_get__(desc)
    else:
      value = preValue

    postValue = None
    for hook in hooks:
      result = __post_get__(hook, value)
      if result is not None:
        if postValue is not None:
          raise HookConflict("Multiple post-get overrides")
        postValue = result

    return postValue if postValue is not None else value

  Setter Flow:
    preValue = None
    for hook in hooks:
      result = __pre_set__(hook, value)
      if result is not None:
        if preValue is not None:
          raise HookConflict("Multiple pre-set overrides")
        preValue = result

    if preValue is not None:
      __instance_set__(desc, preValue)
      return

    try:
      oldVal = __instance_get__(desc)
    except MissingValue as missingValue:
      oldVal = missingValue

    postValue = None
    for hook in hooks:
      result = __post_set__(hook, value, oldVal)
      if result is not None:
        if postValue is not None:
          raise HookConflict("Multiple post-set overrides")
        postValue = result

    if postValue is not None:
      __instance_set__(desc, postValue)
    else:
      __instance_set__(desc, value)

  Deleter Flow:
    for hook in hooks:
      __pre_delete__(hook)

    try:
      oldVal = __instance_get__(desc)
    except MissingValue as missingValue:
      # Deletion of a missing value is forbidden; escalates to AttributeError
      raise AttributeError from missingValue  # Actual implementation may
      vary

    for hook in hooks:
      __post_delete__(hook, oldVal)

    __instance_delete__(desc)

  Where hooks may override values in the control flow at most one hook may
  provide a replacement value at each stage of the control flow. Multiple
  hooks providing replacement values will raise a HookConflict.

  Hooks apply according to their priority. The lower this priority value,
  the earlier the hook is applied in the control flow. The tie-breaker is
  deliberately random to avoid applying undefined deterministic order.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Fallback Variables

  #  Private Variables
  __priority_value__ = None

  #  Public Variables
  priority = _Priority()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, *args, **kwargs) -> None:
    keys = stringList("""priority, tier, rank""")
    kwargPriority, kwargs = self.parseKwargs(int, *keys, **kwargs)
    if kwargPriority is None:
      for arg in args:
        if isinstance(arg, int):
          kwargPriority = arg
          break
    else:
      self.priority = kwargPriority

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __pre_get__(self, ) -> Any:
    """
    Pre-get hook. Override this method to implement pre-get behavior.
    """

  def __post_get__(self, value: Any) -> Any:
    """
    Post-get hook. Override this method to implement post-get behavior.
    """

  def __pre_set__(self, value: Any, ) -> Any:
    """
    Pre-set hook. Override this method to implement pre-set behavior.
    """

  def __post_set__(self, value: Any, oldValue: Any) -> Any:
    """
    Post-set hook. Override this method to implement post-set behavior.
    """

  def __pre_delete__(self, ) -> None:
    """
    Pre-delete hook. Override this method to implement pre-delete behavior.
    """

  def __post_delete__(self, oldValue: Any) -> None:
    """
    Post-delete hook. Override this method to implement post-delete behavior.
    """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __set_name__(self, owner: type, name: str, **kwargs) -> None:
    """
    Sets the name of the hook in the owner class.
    """
    AbstractObject.__set_name__(self, owner, name, **kwargs)
    if issubclass(owner, AbstractDescriptor):
      owner.registerAccessorHook(name, self)
    else:
      raise SubclassException(owner, AbstractDescriptor, )

  def __int__(self, ) -> int:
    """
    Returns the priority value of the hook.
    """
    return self.priority.value

  def __str__(self) -> str:
    """
    Returns the string representation of the hook, which is its priority
    value.
    """
    warn('TODO: Implement __str__ for AbstractDescriptorHook', )
    return AbstractObject.__str__(self)

  def __repr__(self) -> str:
    """
    Returns the string representation of the hook, which is its priority
    value.
    """
    warn('TODO: Implement __repr__ for AbstractDescriptorHook', )
    return AbstractObject.__repr__(self)

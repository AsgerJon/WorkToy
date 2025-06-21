"""
AbstractDescriptorHook defines the hooks surrounding the accessor
functions in the 'worktoy.attr.AbstractDescriptor' class.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from types import FunctionType as Func

from random import random as r

from . import HookPhase
from ...parse import maybe
from ...static import AbstractObject, Alias
from ...waitaminute import SubclassException, DuplicateHookError

#  Below provides compatibility back to Python 3.7
try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, Callable, Iterator, TypeAlias, Type
  from .. import AbstractDescriptor

  ADesc: TypeAlias = Type[AbstractDescriptor]
  PhaseMap: TypeAlias = dict[HookPhase, Func]


class _ActiveInstance:
  """
  This private descriptor reflects the current instance of the descriptor
  owning the hook that owns this descriptor.
  """

  def __get__(self, desc: Any, owner: type) -> Any:
    """
    Returns the current instance of the descriptor owning the hook.
    """
    if desc is None:
      return self
    return desc.instance


class _ActiveOwner:
  """
  This private descriptor reflects the current owner of the descriptor
  owning the hook that owns this descriptor.
  """

  def __get__(self, desc: Any, owner: type) -> Any:
    """
    Returns the current owner of the descriptor owning the hook.
    """
    if desc is None:
      return self
    return desc.owner


class _DescName:
  """
  This private descriptor reflects the private name on the hook that owns
  this descriptor.
  """

  def __get__(self, desc: Any, owner: type) -> Any:
    """
    Returns the private name of the descriptor owning the hook.
    """
    if desc is None:
      return self
    if TYPE_CHECKING:
      assert isinstance(desc, AbstractObject)
    return desc.getPrivateName()


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

  Accessor control flows are defined below. Please note the use of the
  'worktoy.parse.maybe' function which returns the first value other than
  None encountered.

  Getter Flow:
    #  Pre-get Flow
    out = None  # Starting value
    for hook in hooks:
      out = maybe(hook.__pre_get__(out), out)
      #  'out' updates only when hook returns a value other than None
    #  If 'out' is still 'None', the '__instance_get__' method is
    called.

    if out is None:
      out = __instance_get__(...)

    #  Post-get Flow
    for hook in hooks:
      out = maybe(hook.__post_get__(out), out)

    #  If 'out' is still 'None' after post-get, the flow raises an
    'AttributeError'. Subclasses should change this behaviour by adding
    a hook either pre or post rather than reimplementing the flow.

    if out is None:
      raise AttributeError
    return out

  Setter Flow:
    #  Pre-set Flow
    #  Please note that 'pre' here means before the existing value,
    #  if any, is determined. This allows hooks in situations where the
    #  '__instance_get__' method might not be desirable to invoke.
    __set__(desc, instance, newValue: Any) -> None:
      ...
    hooks = desc.getAccessorHooks()
    for hook in hooks:
      newValue = maybe(hook.__pre_set__(newValue), newValue)
      #  'newValue' updates only when hook returns a value other than None

    #  Post-set Flow

    #  If no hook provides a post-set implementation, the flow invokes
    __instance_set__ immediately and stops.

    for hook in hooks:
      if hook.hasPost:
        break
    else:
      return __instance_set__(desc, newValue)  # prevented by any 'break'

    #  Having found at least one post-set hook, the flow now collects the
    old value, if any, invokes the post-set hooks and finally sets the new
    value:

    try:
      oldValue = __instance_get__(desc)
    except MissingValue as missingValue:
      oldValue = missingValue

    #  Normally, an exception raised by '__instance_get__' would
    #  propagate, but descriptors may raise 'MissingValue' to indicate that
    #  an expected value is not yet ready, but that nothing is wrong. For
    #  example, if the descriptor is waiting for the first 'set' call. All
    #  other exceptions raised by '__instance_get__' will propagate as
    #  normal.

    for hook in hooks:
      newValue = maybe(hook.__post_set__(newValue, oldValue), newValue)
      #  'newValue' updates only when hook returns a value other than None

    #  After post set hooks have been invoked, '__instance_set__' sets the
    #  new value

    return __instance_set__(desc, newValue)

  Deleter Flow:
    The deleter flow is identical to the setter flow except concluding
    with '__instance_delete__' instead of '__instance_set__'. Pre delete
    hooks are invoked before the old value is collected, allowing them to
    raise exceptions before an expensive call to __instance_get__ is made.

    If no such exception is raised, the old value, if any, is collected,
    but unlike the setter flow, any exception, even a 'MissingValue',
    will propagate as normal. Post delete hooks are invoked only where the
    old value is available. They are not able to stop the deletion,
    so where appropriate, they should either raise an exception or restore
    the deleted value.

  - HOOK PRIORITY -
  All hook objects have a 'priority' attribute assigned to each of their
  hook methods. The hooks are invoked beginning from the lowest priority
  value at the particular hook method being invoked. Hook objects not
  implementing a particular hook method has a negative priority (-1)
  indicating that they should be skipped entirely. Where multiple hooks
  share value, they are invoked in random order. This random order resets
  on every call.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __phase_map__ = None
  __pre_get__ = None
  __post_get__ = None
  __pre_set__ = None
  __post_set__ = None
  __pre_delete__ = None
  __post_delete__ = None

  #  Public Variables
  desc = Alias('instance')
  descClass = Alias('owner')
  activeInstance = _ActiveInstance()
  activeOwner = _ActiveOwner()
  privateName = _DescName()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def _getPhaseMap(cls, **kwargs) -> PhaseMap:
    """
    Returns mapping from HookPhase to the corresponding adder method. This
    method is bound to the class.
    """
    if cls.__phase_map__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      cls.__phase_map__ = {
          HookPhase.PRE_GET    : cls.addPreGet,
          HookPhase.POST_GET   : cls.addPostGet,
          HookPhase.PRE_SET    : cls.addPreSet,
          HookPhase.POST_SET   : cls.addPostSet,
          HookPhase.PRE_DELETE : cls.addPreDelete,
          HookPhase.POST_DELETE: cls.addPostDelete,
      }
      return cls._getPhaseMap(_recursion=True, )
    return cls.__phase_map__

  #  Hook Iterators
  @classmethod
  def getPreGets(cls, ) -> Iterator[Callable]:  # NOQA
    yield from sorted(maybe(cls.__pre_get__, ()), key=lambda h: h.p)

  @classmethod
  def getPostGets(cls, ) -> Iterator[Callable]:  # NOQA
    yield from sorted(maybe(cls.__pre_get__, ()), key=lambda h: h.p)

  @classmethod
  def getPreSets(cls, ) -> Iterator[Callable]:  # NOQA
    yield from sorted(maybe(cls.__pre_get__, ()), key=lambda h: h.p)

  @classmethod
  def getPostSets(cls, ) -> Iterator[Callable]:  # NOQA
    yield from sorted(maybe(cls.__pre_get__, ()), key=lambda h: h.p)

  @classmethod
  def getPreDeletes(cls, ) -> Iterator[Callable]:  # NOQA
    yield from sorted(maybe(cls.__pre_get__, ()), key=lambda h: h.p)

  @classmethod
  def getPostDeletes(cls, ) -> Iterator[Callable]:  # NOQA
    yield from sorted(maybe(cls.__pre_get__, ()), key=lambda h: h.p)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def addPreGet(cls, preGet: Callable) -> None:
    """
    Adds a pre-get hook to the descriptor.
    """
    preGetName = getattr(preGet, '__name__', None)
    existing = maybe(cls.__pre_get__, [])
    for hook in existing:
      hookName = getattr(hook, '__name__', )
      if hookName == preGetName:
        raise DuplicateHookError(cls, hookName, hook, preGet)
    cls.__pre_get__ = [*existing, preGet, ]

  @classmethod
  def addPostGet(cls, postGet: Callable) -> None:
    """
    Adds a post-get hook to the descriptor.
    """
    postGetName = getattr(postGet, '__name__', None)
    existing = maybe(cls.__post_get__, [])
    for hook in existing:
      hookName = getattr(hook, '__name__', )
      if hookName == postGetName:
        raise DuplicateHookError(cls, hookName, hook, postGet)
    cls.__post_get__ = [*existing, postGet, ]

  @classmethod
  def addPreSet(cls, preSet: Callable) -> None:
    """
    Adds a pre-set hook to the descriptor.
    """
    preSetName = getattr(preSet, '__name__', None)
    existing = maybe(cls.__pre_set__, [])
    for hook in existing:
      hookName = getattr(hook, '__name__', )
      if hookName == preSetName:
        raise DuplicateHookError(cls, hookName, hook, preSet)
    cls.__pre_set__ = [*existing, preSet, ]

  @classmethod
  def addPostSet(cls, postSet: Callable) -> None:
    """
    Adds a post-set hook to the descriptor.
    """
    postSetName = getattr(postSet, '__name__', None)
    existing = maybe(cls.__post_set__, [])
    for hook in existing:
      hookName = getattr(hook, '__name__', )
      if hookName == postSetName:
        raise DuplicateHookError(cls, hookName, hook, postSet)
    cls.__post_set__ = [*existing, postSet, ]

  @classmethod
  def addPreDelete(cls, preDelete: Callable) -> None:
    """
    Adds a pre-delete hook to the descriptor.
    """
    preDeleteName = getattr(preDelete, '__name__', None)
    existing = maybe(cls.__pre_delete__, [])
    for hook in existing:
      hookName = getattr(hook, '__name__', )
      if hookName == preDeleteName:
        raise DuplicateHookError(cls, hookName, hook, preDelete)
    cls.__pre_delete__ = [*existing, preDelete, ]

  @classmethod
  def addPostDelete(cls, postDelete: Callable) -> None:
    """
    Adds a post-delete hook to the descriptor.
    """
    postDeleteName = getattr(postDelete, '__name__', None)
    existing = maybe(cls.__post_delete__, [])
    for hook in existing:
      hookName = getattr(hook, '__name__', )
      if hookName == postDeleteName:
        raise DuplicateHookError(cls, hookName, hook, postDelete)
    cls.__post_delete__ = [*existing, postDelete, ]

  @classmethod
  def addPhase(cls, phase: HookPhase, hook: Callable) -> None:
    """
    Adds a hook to the descriptor for the given phase.
    """
    cls._getPhaseMap()[phase](hook)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __set_name__(self, owner: ADesc, name: str, **kwargs) -> None:
    """
    Sets the name of the hook in the owner class.
    """
    AbstractObject.__set_name__(self, owner, name, **kwargs)
    owner.registerAccessorHook(self)

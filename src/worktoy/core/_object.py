"""
Object provides the most basic object used by the 'worktoy' library. It
stands in for the 'object' type by adding functionality that must be
shared by every object in the library.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

import re
from typing import TYPE_CHECKING

from ..utilities import Directory, maybe
from ..waitaminute import TypeException, MissingVariable
from ..waitaminute.desc import WithoutException, ReadOnlyError
from ..waitaminute.desc import ProtectedError
from ..waitaminute.control_flow import SkipSet
from .sentinels import THIS, DESC, OWNER, DELETED, Sentinel
from . import ContextInstance, MetaType, ContextOwner

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Self, Optional, Type, TypeAlias
  from types import TracebackType

  ExcType: TypeAlias = Optional[Type[Exception]]
  ExcVal: TypeAlias = Optional[Exception]
  Trace: TypeAlias = Optional[TracebackType]

#  Compiled once at import. 'getPrivateName' sits on the hot path of
#  every descriptor access, so the pattern must not be rebuilt per call.
_PRIVATE_KEY_PATTERN = re.compile(r'(?<!^)(?=[A-Z])')


class Object(metaclass=MetaType):
  """The fundamental base class for objects in the 'worktoy' library.

  'Object' provides a contextually aware descriptor protocol so that
  subclasses can implement descriptor behavior in three small hooks
  ('__instance_get__', '__instance_set__', '__instance_delete__')
  without having to thread the '(instance, owner)' pair through every
  call. Inside those hooks the active instance is available as
  'self.instance' and the owning class as 'self.owner'.

  Subclassing contract
  --------------------
  Override one or more of:

  - '__instance_get__(self, instance, owner, **kw)': define how
    the descriptor reads. Defaults to returning 'self'.
  - '__instance_set__(self, instance, value, **kw)': define how
    the descriptor writes. Defaults to raising 'ReadOnlyError'.
  - '__instance_delete__(self, instance, old, **kw)': define how
    the descriptor deletes. Defaults to raising 'ProtectedError'.

  Do not override '__get__', '__set__', or '__delete__'. Those are
  the context-managing entry points and are expected to stay as
  implemented here. They push a new '(instance, owner)' frame onto
  the descriptor's context stack, dispatch to the corresponding
  '__instance_*' hook, and pop the frame on the way out.

  Context machinery
  -----------------
  Each descriptor object holds a per-descriptor stack of
  '(instance, owner)' pairs in '__call_chain__'. The stack is grown
  by 'createContext(instance, owner)' and shrunk by 'exitContext()'.
  'self.instance' and 'self.owner' read the top of that stack via
  the 'ContextInstance' and 'ContextOwner' descriptors. The
  'with self.createContext(...) as context:' idiom inside '__get__'
  / '__set__' / '__delete__' guarantees the pop happens even if the
  hook raises.

  Re-entrant access to the same descriptor object is safe: an inner
  call pushes a new frame, 'self.instance' inside that frame sees
  the new instance, and when the inner call returns and pops, the
  outer frame's instance is restored.

  Reading 'self.instance' or 'self.owner' outside any active
  context raises 'WithoutException'. Calling 'exitContext' on an
  empty stack raises 'WithoutException' as well, since that
  indicates an unpaired 'createContext' / 'exitContext' call.

  Public context API: 'createContext', 'exitContext', 'hasContext',
  'getContextInstance', 'getContextOwner'.

  Limitations
  -----------
  The context stack lives on the descriptor object, which is shared
  across every owning instance of the class. Concurrent access is
  therefore not safe:

  - Multiple threads accessing the same field on different instances
    will race on the stack.
  - An 'await' inside a descriptor hook lets another coroutine
    clobber the stack the same way.

  'worktoy' descriptors are intended for single-threaded synchronous
  code. If you need thread- or task-local safety, layer it on top.

  Deletion semantics
  ------------------
  '__instance_delete__' signals deletion by assigning the 'DELETED'
  sentinel to the storage that '__instance_get__' would read. The
  next call to '__instance_get__' returns 'DELETED', which the
  '__get__' wrapper translates into 'MissingVariable'. This avoids
  threading a 'was-deleted' flag through every accessor.

  Examples
  --------
  >>> class Counted(Object):
  ...   def __instance_get__(self, instance: Any, owner: type, **kw) -> Any:
  ...     return getattr(instance, '_count', 0)
  ...   def __instance_set__(self, instance: Any, value: Any, **kw) -> None:
  ...     instance._count = value
  ...   def __instance_delete__(self, instance: Any, **kw) -> None:
  ...     instance._count = DELETED
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables

  #  Private Variables
  __field_owner__ = None
  __field_name__ = None
  __private_name__ = None  # cached result of 'getPrivateName'
  __pos_args__ = None
  __key_args__ = None
  __call_chain__ = None

  #  Public Variables
  directory = Directory()
  instance = ContextInstance()
  owner = ContextOwner()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def getFieldOwner(self) -> type:
    return self.__field_owner__

  def getFieldName(self) -> Optional[str]:
    return self.__field_name__

  def getContextualSentinels(self, ) -> dict[Type[Sentinel], Any]:
    """
    Returns a dictionary mapping the sentinels 'THIS', 'OWNER', and 'DESC'
    to their corresponding contextual values. Where contextual values are
    not available, the sentinel is returned.
    """
    if self.__call_chain__:
      instance, owner = self.__call_chain__[-1]
    else:
      instance, owner = None, None
    return {
      THIS : maybe(instance, THIS),
      OWNER: maybe(owner, OWNER),
      DESC : self,
    }

  def filterSentinels(self, arg: Any) -> Any:
    """
    If 'arg' is one of the sentinels 'THIS', 'OWNER', or 'DESC',
    it is replaced by the corresponding contextual value.
    """
    try:
      out = self.getContextualSentinels().get(arg, arg)
    except TypeError:
      return arg
    else:
      return out

  def getPosArgs(self, ) -> tuple[Any, ...]:
    out = []
    for arg in maybe(self.__pos_args__, ()):
      out.append(self.filterSentinels(arg))
    return (*out,)

  def getKeyArgs(self, ) -> dict[str, Any]:
    out = dict()
    for key, value in maybe(self.__key_args__, dict()).items():
      out[key] = self.filterSentinels(value)
    return out

  def getContextInstance(self) -> Any:
    """Returns the contextual instance or raises 'WithoutException'"""
    if self.hasContext():
      return self.__call_chain__[-1][0]
    raise WithoutException(self)

  def getContextOwner(self) -> type:
    """Returns the contextual owner or raises 'WithoutException'"""
    if self.hasContext():
      return self.__call_chain__[-1][1]
    raise WithoutException(self)

  def hasContext(self) -> bool:
    """
    Returns True if the descriptor has at least one active context,
    i.e. 'createContext' has been called more times than 'exitContext'.
    """
    return bool(self.__call_chain__)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, *args, **kwargs) -> None:
    object.__init__(self)
    self.__pos_args__ = args
    self.__key_args__ = kwargs
    self.__call_chain__ = []

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __set_name__(self, owner: type, name: str, **kwargs) -> None:
    """Records the owning class and attribute name, then invokes
    'hookSetName' so subclasses can react without overriding this
    method."""
    self.__field_owner__ = owner
    self.__field_name__ = name
    self.hookSetName(owner, name, **kwargs)

  def __get__(self, instance: Any, owner: type, ) -> Any:
    """When accessed through the class, returns this descriptor.
    When accessed through an instance, pushes a context frame,
    invokes 'hookPreGet' and '__instance_get__', translates a
    'DELETED' result into 'MissingVariable', and finally invokes
    'hookOnGet'. The context frame is popped on the way out
    regardless of whether the hooks raise."""
    if instance is None:
      return self
    self.createContext(instance, owner)
    try:
      self.hookPreGet(instance, )
      value = self.__instance_get__(instance, owner)
      value = self._deletedGuard(instance, value)
      self.hookOnGet(instance, value, )
    finally:
      self.exitContext()
    return value

  def __set__(self, instance: Any, newValue: Any, **kwargs) -> None:
    """Pushes a context frame, invokes 'hookPreSet', and (unless the
    hook raises 'SkipSet' to abort) calls '__instance_set__' followed
    by 'hookOnSet'. The context frame is popped on the way out
    regardless of whether the hooks raise."""
    self.createContext(instance, type(instance))
    try:
      try:
        self.hookPreSet(instance, newValue, **kwargs)
      except SkipSet:
        pass
      else:
        self.__instance_set__(instance, newValue, **kwargs)
        self.hookOnSet(instance, newValue, **kwargs)
    finally:
      self.exitContext()

  def __delete__(self, instance: Any, **kwargs) -> None:
    """Pushes a context frame, reads the prior value (or 'None' if
    the attribute already raised), invokes 'hookPreDelete', calls
    '__instance_delete__' with the old value, and finally invokes
    'hookOnDelete'. Subclasses signal deletion by storing the
    'DELETED' sentinel in their backing storage; see 'Object'."""
    owner = type(instance)
    self.createContext(instance, owner)
    try:
      try:
        oldVal = self.__instance_get__(instance, owner, **kwargs)
      except AttributeError:
        oldVal = None
      else:
        oldVal = self._deletedGuard(instance, oldVal)
      self.hookPreDelete(instance, **kwargs)
      self.__instance_delete__(instance, oldVal, **kwargs)
      self.hookOnDelete(instance, **kwargs)
    finally:
      self.exitContext()

  def __init_subclass__(cls, **kwargs) -> None:
    """Accept arbitrary class kw so worktoy metaclass machinery
    can forward them to space hooks without 'object.__init_subclass__'
    rejecting them."""
    super().__init_subclass__()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __instance_get__(self, instance: Any, owner: type, **kwargs) -> Any:
    """Instance-specific getter for this descriptor.

    Inside this method, 'self.instance' resolves to the currently
    active instance and 'self.owner' to the owning class. Subclasses
    should override to define attribute retrieval logic. Return the
    'DELETED' sentinel to signal that the attribute has been deleted;
    the surrounding '__get__' wrapper will translate that into
    'MissingVariable'. See 'Object' for a full example.
    """
    return self

  def __instance_set__(self, instance: Any, value: Any, **kwargs) -> None:
    """Instance-specific setter for this descriptor.

    Inside this method, 'self.instance' resolves to the currently
    active instance. Subclasses should override to define attribute
    assignment logic. The default raises 'ReadOnlyError'. See
    'Object' for a full example.
    """
    raise ReadOnlyError(instance, self, value)

  def __instance_delete__(
      self,
      instance: Any,
      old: Any = None,
      **kwargs,
  ) -> None:
    """Instance-specific deleter for this descriptor.

    To signal deletion, assign the 'DELETED' sentinel to your storage
    so the next '__instance_get__' returns 'DELETED'; the wrapper
    will raise 'MissingVariable' on subsequent access. The default
    raises 'ProtectedError'. See 'Object' for a full example.
    """
    raise ProtectedError(instance, self, old)

  def createContext(self, instance: Any, owner: type, ) -> Self:
    """
    Pushes a new '(instance, owner)' pair onto the descriptor's
    context stack and returns 'self' so the descriptor can be used as
    a context manager. The stack makes the protocol safe under
    re-entrant access to the same descriptor.
    """
    if self.__call_chain__ is None:
      self.__call_chain__ = []
    self.__call_chain__.append((instance, owner))
    return self

  def exitContext(self) -> Self:
    """
    Pops the most recent '(instance, owner)' pair off the
    descriptor's context stack, restoring the prior context (if any).
    Raises 'WithoutException' if the stack is empty, since that
    indicates an unpaired 'createContext' / 'exitContext' call.
    """
    if not self.__call_chain__:
      raise WithoutException(self)
    self.__call_chain__.pop()
    return self

  def _deletedGuard(self, instance: Any, value: Any, ) -> Any:
    """If 'value' is the 'DELETED' sentinel, raise 'MissingVariable'
    so callers see the attribute as absent. Otherwise return 'value'
    unchanged."""
    if value is DELETED:
      raise MissingVariable(instance, self.__field_name__)
    return value

  def getPrivateName(self, ) -> str:
    """Returns the dunder-style private name corresponding to this
    descriptor's field name. 'camelCase' is converted to
    'snake_case' and wrapped in double underscores. For example, a
    descriptor named 'fooBar' returns '__foo_bar__'. The result is
    cached on first use: the field name is fixed once '__set_name__'
    has run, and this sits on the hot path of every access."""
    if self.__private_name__ is None:
      snake = _PRIVATE_KEY_PATTERN.sub('_', self.__field_name__).lower()
      self.__private_name__ = '__%s__' % snake
    return self.__private_name__

  def hookPreGet(self, instance, **kwargs) -> None:
    """
    A hook called at the beginning of a get operation, but before running
    the '__instance_get__'
    """

  def hookOnGet(self, instance: Any, value: Any, **kwargs, ) -> None:
    """
    A hook that is called after the value is retrieved from the instance.
    The given value is the value about to be returned by '__get__'. This
    method *cannot* replace this value. If mutable, the value may be
    modified in place. This hook is *not* notified, if instance is 'None'.

    Parameters
    ----------
    instance: The instance the descriptor is bound to.
    value: The value about to be returned by '__get__'.

    Returns
    -------
    None
    """

  def hookPreSet(self, instance: Any, value: Any, **kwargs, ) -> None:
    """
    A hook that is called *before* the value is set on the instance. The
    given value is the value just set by '__set__'.

    Parameters
    ----------
    instance: The instance the descriptor is bound to.
    value: The value just set by '__set__'.

    Returns
    -------
    None
    """

  def hookOnSet(self, instance: Any, value: Any, **kwargs, ) -> None:
    """
    A hook that is called *after* the value is set on the instance. The
    given value is the value just set by '__set__'.

    Parameters
    ----------
    instance: The instance the descriptor is bound to.
    value: The value just set by '__set__'.

    Returns
    -------
    None
    """

  def hookPreDelete(self, instance: Any, **kwargs, ) -> None:
    """
    A hook that is called *before* the value is deleted from the
    instance, prior to '__instance_delete__'.

    Parameters
    ----------
    instance: The instance the descriptor is bound to.
    """

  def hookOnDelete(self, instance: Any, **kwargs, ) -> None:
    """
    A hook that is called *after* the value is deleted from the
    instance, once '__instance_delete__' has returned.

    Parameters
    ----------
    instance: The instance the descriptor is bound to.
    """

  def hookSetName(self, owner: type, name: str, **kwargs) -> None:
    """
    A hook that is called when the descriptor is assigned to a class. The
    given 'owner' is the class the descriptor is assigned to, and 'name'
    is the name of the attribute the descriptor is assigned to.

    Parameters
    ----------

    owner: type
      The class the descriptor is assigned to.

    name: str
      The name of the attribute the descriptor is assigned to.
    """

  @classmethod
  def parseKwargs(cls, *args, **kwargs) -> tuple[Any, dict]:
    """
    Parses the keyword arguments for value matching keys and types given
    in positional arguments. The return value is a tuple of the value
    found and the remaining keyword arguments. If no value is found,
    the returned tuple will be 'None' and all the keyword arguments
    received. If no types are given, the type of the value is ignored.
    """
    typeArgs, keys = [], []
    for arg in args:
      if isinstance(arg, type):
        typeArgs.append(arg)
        continue
      if isinstance(arg, str):
        keys.append(arg)
        continue
    if not keys:
      return None, {**kwargs, }
    typeArgs = typeArgs or [object, ]
    if complex in typeArgs:
      if float not in typeArgs:
        typeArgs.append(float)
      if int not in typeArgs:
        typeArgs.append(int)
    elif float in typeArgs:
      if int not in typeArgs:
        typeArgs.append(int)
    for key in keys:
      if key in kwargs:
        value = kwargs[key]
        for type_ in typeArgs:
          if isinstance(value, type_):
            del kwargs[key]
            return value, {**kwargs, }
        else:
          raise TypeException(key, value, *typeArgs, )
    else:
      return None, {**kwargs, }

"""
Object is the most primitive base class in the 'worktoy' library.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

import re
from typing import TYPE_CHECKING

from ..utilities import Directory, maybe
from ..waitaminute import TypeException, MissingVariable
from ..waitaminute.desc import WithoutException, ReadOnlyError
from ..waitaminute.desc import ProtectedError, RecursiveRead
from .control_flow import SkipSet
from .sentinels import THIS, DESC, OWNER, DELETED, Sentinel
from . import ContextInstance, MetaType, ContextOwner

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any, Callable, Self, Optional, Type

  from ..desc import AttriBox

#  Compiled once at import rather than rebuilt on every 'getPrivateName'
#  call.
_PRIVATE_KEY_PATTERN = re.compile(r'(?<!^)(?=[A-Z])')


class Object(metaclass=MetaType):
  """
  A descriptor in plain Python receives the instance and the owner as
  arguments of '__get__', '__set__' and '__delete__', and every helper it
  calls must be handed them again. worktoy needs descriptors whose code
  can ask for the instance and owner of the access in progress instead,
  even when the same descriptor is reached again from inside one of its
  own hooks. A descriptor class should define reading, writing and
  deleting in one method each, while the bookkeeping and the notification
  hooks around them stay out of its way. A value a descriptor builds
  lazily, such as the default of a box, needs the arguments the
  descriptor was created with, with placeholders for the instance, the
  owner and the descriptor filled in at the time of the access.

  The same base serves the ordinary objects of worktoy, 'BaseObject'
  among them. Such an object placed in a class body is a class variable
  shared by every instance, and no instance may replace or remove it.

  Implementation
  --------------

  Each 'Object' keeps a stack of '(instance, owner)' frames in
  '__call_chain__'. '__get__', '__set__' and '__delete__' push a frame,
  call 'hookPreGet', 'hookOnGet', 'hookPreSet', 'hookOnSet',
  'hookPreDelete' or 'hookOnDelete' around '__instance_get__',
  '__instance_set__' or '__instance_delete__', and pop the frame in a
  'finally' block. 'self.instance' and 'self.owner' read the top frame.
  The constructor keeps its arguments, which 'getPosArgs' and
  'getKeyArgs' return with 'THIS', 'OWNER' and 'DESC' replaced. The
  defaults of the three '__instance_*__' methods return the descriptor,
  refuse writes with 'ReadOnlyError' and refuse deletions with
  'ProtectedError', which makes every 'Object' in a class body read-only
  through instances; a write or deletion through the class itself is
  left to the metaclass, as for 'type'. A deletion stores 'DELETED',
  which a read turns into 'MissingVariable'. A read made while a read
  hook of the same descriptor runs for the same instance is refused with
  'RecursiveRead', since it would run that hook again. The frames live on
  the descriptor and are shared by every instance of the owning class, so
  the protocol is meant for single-threaded, synchronous code.

  Attributes
  ----------

  instance : Any
    The instance of the access in progress; see 'ContextInstance'.

  owner : type
    The owner of the access in progress; see 'ContextOwner'.

  directory : str
    The directory of the file defining the class of the instance.

  __field_owner__ : type or None
    The class the descriptor is placed in, from '__set_name__'.

  __field_name__ : str or None
    The name the descriptor is placed at, from '__set_name__'.

  __pos_args__ : tuple or None
    The positional arguments of the constructor.

  __key_args__ : dict or None
    The keyword arguments of the constructor.

  __call_chain__ : list or None
    The stack of '(instance, owner)' frames.

  __get_lock__ : list or None
    The instances whose read hooks are running, each with the name of
    the hook, 'preGet' or 'onGet'.

  Examples
  --------

  A descriptor counting on its instances, with deletion:

  >>> class Counted(Object):
  ...   def __instance_get__(self, instance: Any, owner: type, **kw) -> Any:
  ...     return getattr(instance, '_count', 0)
  ...   def __instance_set__(self, instance: Any, value: Any, **kw) -> None:
  ...     instance._count = value
  ...   def __instance_delete__(self, instance: Any, old: Any = None,
  ...                           **kw) -> None:
  ...     instance._count = DELETED
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables

  #  Private Variables
  __field_owner__: Optional[type] = None
  __field_name__: Optional[str] = None
  __private_name__: Optional[str] = None  # cached result of 'getPrivateName'
  __pos_args__: Optional[tuple[Any, ...]] = None
  __key_args__: Optional[dict[str, Any]] = None
  __call_chain__: Optional[list[tuple[Any, type]]] = None
  __get_lock__: Optional[list[tuple[Any, str]]] = None

  #  Public Variables
  directory = Directory()
  instance = ContextInstance()
  owner = ContextOwner()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def getFieldOwner(self) -> Optional[type]:
    return self.__field_owner__

  def getFieldName(self) -> str:
    return maybe(self.__field_name__, '<%s>' % type(self).__name__)

  def getContextualSentinels(self, ) -> dict[Type[Sentinel], Any]:
    """
    The placeholders 'THIS', 'OWNER' and 'DESC' among the constructor
    arguments must become the instance, the owner and the descriptor of the
    access in progress.

    Implementation
    --------------

    The top frame gives the instance and owner; without a frame, 'THIS'
    and 'OWNER' stand for themselves.

    Returns
    -------

    dict[type[Sentinel], Any]
      The mapping from each placeholder to its value.
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
    A single constructor argument that is a placeholder must be replaced by
    what it stands for, and any other argument passed on as it is.

    Implementation
    --------------

    The argument is looked up in 'getContextualSentinels'. Only the
    argument itself is compared, so a placeholder inside a container stays
    a placeholder, and an unhashable argument is returned unchanged.

    Parameters
    ----------

    arg : Any
      A constructor argument.

    Returns
    -------

    Any
      The value the placeholder stands for, or 'arg' itself.
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

  def hasSentinelArgs(self) -> bool:
    """
    A box given a single argument of its field type copies it rather than
    calling the constructor. When that argument only became an instance of
    the field type because a placeholder was replaced, as 'THIS' replaced
    by an instance of the field type, the constructor must be called all
    the same.

    Implementation
    --------------

    Every positional and keyword argument is compared by identity with
    'THIS', 'OWNER' and 'DESC'.

    Returns
    -------

    bool
      Whether any constructor argument is a placeholder.
    """
    posArgs = maybe(self.__pos_args__, ())
    keyArgs = maybe(self.__key_args__, dict())
    sentinels = (THIS, OWNER, DESC)
    for arg in (*posArgs, *keyArgs.values()):
      if any(arg is sentinel for sentinel in sentinels):
        return True
    return False

  def getContextInstance(self) -> Any:
    """
    The code of a descriptor must be able to ask for the instance of the
    access in progress. Outside an access the question has no answer, and
    the failure must say why: a descriptor placed in a class was used
    outside its protocol, which is a mistake worth an error of its own,
    while a value no class holds simply has no such attribute, and must let
    'hasattr' answer 'False'. A value built by an 'AttriBox' belongs to the
    instance it was built for, and must be able to learn that instance
    while its box is reading.

    Implementation
    --------------

    With a frame, the instance of the top frame is returned. Without one,
    an object with no '__field_name__' raises a plain 'AttributeError'; an
    object carrying the box tag '__field_box__' answers through that box,
    or raises a plain 'AttributeError' when the box has no frame; any other
    object, a placed descriptor, raises 'WithoutException'. A box tags an
    'Object' it builds only after its constructor returns, so the
    constructor of a box-built value cannot ask; it receives the instance
    through 'THIS' among the arguments of the box instead.

    Returns
    -------

    Any
      The instance of the access in progress.

    Raises
    ------

    WithoutException
      A placed descriptor is asked outside an access.

    AttributeError
      A value no class holds is asked, or a box-built value outside a read
      of its box.
    """
    if self.hasContext():
      if self.__call_chain__ is None:
        raise MissingVariable(self, '__call_chain__', list)
      return self.__call_chain__[-1][0]
    if self.__field_name__ is None:
      infoSpec: str = """'%s' object has no attribute 'instance'"""
      info: str = infoSpec % type(self).__name__
      raise AttributeError(info)
    try:
      box: AttriBox = object.__getattribute__(self, '__field_box__')
    except AttributeError:
      raise WithoutException(self)
    else:
      try:
        boxInstance: Any = box.getContextInstance()
      except WithoutException:
        infoSpec: str = """'%s' object has no attribute 'instance'"""
        clsName: str = type(self).__name__
        info = infoSpec % clsName
        raise AttributeError(info)
      else:
        return boxInstance

  def getContextOwner(self) -> Optional[type]:
    """
    The code of a descriptor must be able to ask for the owner of the
    access in progress, under the same conditions as for the instance; see
    'getContextInstance'.

    Implementation
    --------------

    As 'getContextInstance', with the owner of the frame.

    Returns
    -------

    type
      The owner of the access in progress.

    Raises
    ------

    WithoutException
      A placed descriptor is asked outside an access.

    AttributeError
      A value no class holds is asked, or a box-built value outside a read
      of its box.
    """
    if self.hasContext():
      if self.__call_chain__ is None:
        raise MissingVariable(self, '__call_chain__', list)
      return self.__call_chain__[-1][1]
    if self.__field_name__ is None:
      infoSpec: str = """'%s' object has no attribute 'owner'"""
      info: str = infoSpec % type(self).__name__
      raise AttributeError(info)
    try:
      box: AttriBox = object.__getattribute__(self, '__field_box__')
    except AttributeError:
      raise WithoutException(self)
    else:
      try:
        boxOwner: Optional[type] = box.getContextOwner()
      except WithoutException:
        infoSpec: str = """'%s' object has no attribute 'owner'"""
        clsName: str = type(self).__name__
        info = infoSpec % clsName
        raise AttributeError(info)
      else:
        return boxOwner

  def hasContext(self) -> bool:
    """
    A subclass may need to change what counts as an access in progress,
    without making 'getContextInstance' and 'getContextOwner' read a stack
    that is not there.

    Implementation
    --------------

    The stack is non-empty. Both getters check the stack again after
    asking, which guards against a reimplementation answering 'True'
    wrongly.

    Returns
    -------

    bool
      Whether a frame is on the stack.
    """
    return bool(self.__call_chain__)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, *args, **kwargs) -> None:
    """
    The arguments given to an 'Object' must be kept for later, when a box
    builds its value from them, even when a subclass guards its attributes
    with a '__setattr__' of its own. A base listed after 'Object', such as
    'threading.Thread', must still be initialized as in a plain class.

    Implementation
    --------------

    The arguments and an empty stack are written with
    'object.__setattr__', and the next '__init__' along the resolution
    order is called without arguments. A subclass taking arguments of its
    own passes on to this method the ones meant for 'getPosArgs' and
    'getKeyArgs'.
    """
    #  The bookkeeping bypasses any '__setattr__' of a subclass.
    object.__setattr__(self, '__pos_args__', args)
    object.__setattr__(self, '__key_args__', kwargs)
    object.__setattr__(self, '__call_chain__', [])
    #  The arguments belong to this class, which recorded them above. A
    #  base after it in the resolution order, such as 'threading.Thread',
    #  is initialized without them, as in a plain class.
    super().__init__()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __set_name__(self, owner: type, name: str, **kwargs) -> None:
    """
    A descriptor must learn the class and name it is placed at, and a
    subclass must be able to react to the placement without taking over
    this method.

    Implementation
    --------------

    The owner and name are recorded, then 'hookSetName' is called. On
    Python 3.7 to 3.11, an exception raised here reaches the class
    statement wrapped in a 'RuntimeError'.

    Parameters
    ----------

    owner : type
      The class the descriptor is placed in.

    name : str
      The name it is placed at.
    """
    object.__setattr__(self, '__field_owner__', owner)
    object.__setattr__(self, '__field_name__', name)
    self.hookSetName(owner, name, **kwargs)

  def __get__(self, instance: Any, owner: type, ) -> Any:
    """
    A read through an instance must run with its frame in place and the
    read hooks around it, and a deleted value must read as absent. A read
    through the class gives the descriptor itself, so it can be inspected
    or have callbacks registered on it.

    Implementation
    --------------

    Through an instance: push the frame, 'hookPreGet', '__instance_get__',
    'DELETED' turned into 'MissingVariable', 'hookOnGet', and pop the frame
    even when something raises. Each hook runs through '_runReadHook',
    which refuses a read reaching the hooks while a hook of this read
    still runs for the same instance.

    Parameters
    ----------

    instance : Any
      The instance read through, or 'None'.

    owner : type
      The class read through.

    Returns
    -------

    Any
      The descriptor through the class, else what '__instance_get__'
      returned.

    Raises
    ------

    MissingVariable
      The attribute was deleted.

    RecursiveRead
      The read was made while a read hook of this descriptor ran for the
      same instance.
    """
    if instance is None:
      return self
    self.createContext(instance, owner)
    try:
      self._runReadHook('preGet', self.hookPreGet, instance)
      value = self.__instance_get__(instance, owner)
      value = self._deletedGuard(instance, value)
      self._runReadHook('onGet', self.hookOnGet, instance, value)
    finally:
      self.exitContext()
    return value

  def _runReadHook(
      self,
      phase: str,
      hook: Callable,
      instance: Any,
      *args,
  ) -> None:
    """
    A read hook reading its own field, as an 'onGet' comparing the field
    with the value it was handed, would run itself again, and so would the
    hooks of two instances reading each other's field, until Python gave
    up with a bare 'RecursionError' a thousand frames later. Such a read
    must fail at the line making it, while a read of another instance, or
    one made by the getter outside the hooks, must not.

    Implementation
    --------------

    The instances whose read hooks are running are kept in '__get_lock__',
    each with the name of its hook. An instance found there is refused
    with 'RecursiveRead', naming the hook that runs. Otherwise the instance
    is added, the hook called, and the instance removed in a 'finally'
    block, so a hook raising leaves later reads as they were. The record
    is written with 'object.__setattr__', past any '__setattr__' of a
    subclass.

    Parameters
    ----------

    phase : str
      The name of the hook, 'preGet' or 'onGet'.

    hook : Callable
      The hook, 'hookPreGet' or 'hookOnGet'.

    instance : Any
      The instance read through.

    *args
      The further arguments of the hook: the value, for 'hookOnGet'.

    Raises
    ------

    RecursiveRead
      A read hook of this descriptor runs for the instance already.
    """
    locked = maybe(self.__get_lock__, [])
    for held, runningPhase in locked:
      if held is instance:
        raise RecursiveRead(self, instance, runningPhase)
    object.__setattr__(self, '__get_lock__', [*locked, (instance, phase)])
    try:
      hook(instance, *args)
    finally:
      locked = maybe(self.__get_lock__, [])
      remaining = [pair for pair in locked if pair[0] is not instance]
      object.__setattr__(self, '__get_lock__', remaining)

  def __set__(self, instance: Any, newValue: Any, **kwargs) -> None:
    """
    A write must run with its frame in place and the write hooks around
    it. The hook before the write sees the value as assigned, and may end
    the write silently with 'SkipSet'; the hook after it sees the value as
    stored, which may be a cast of the value assigned.

    Implementation
    --------------

    Push '(instance, type(instance))', call 'hookPreSet'; unless it raised
    'SkipSet', call '__instance_set__' and then 'hookOnSet' with what it
    returned, or with the value as assigned when it returned 'None'; pop
    the frame even when something raises.

    Parameters
    ----------

    instance : Any
      The instance written through.

    newValue : Any
      The value assigned.
    """
    self.createContext(instance, type(instance))
    try:
      try:
        self.hookPreSet(instance, newValue, **kwargs)
      except SkipSet:
        pass
      else:
        storedValue = self.__instance_set__(instance, newValue, **kwargs)
        self.hookOnSet(instance, maybe(storedValue, newValue), **kwargs)
    finally:
      self.exitContext()

  def __delete__(self, instance: Any, **kwargs) -> None:
    """
    A deletion must run with its frame in place and the delete hooks
    around it, and must hand the value being deleted to
    '__instance_delete__'. Reading that value must not build a default as
    a side effect, and a second deletion must fail as it does for a plain
    attribute.

    Implementation
    --------------

    Push the frame and read the value with '__instance_get__', passing
    '_deleting=True'; an 'AttributeError' from the read gives 'None', and
    'DELETED' raises 'MissingVariable'. Then 'hookPreDelete',
    '__instance_delete__' with the old value and 'hookOnDelete', and pop
    the frame even when something raises.

    Parameters
    ----------

    instance : Any
      The instance deleted through.

    Raises
    ------

    MissingVariable
      The attribute was already deleted.
    """
    owner = type(instance)
    self.createContext(instance, owner)
    try:
      try:
        oldVal = self.__instance_get__(
            instance, owner, _deleting=True, **kwargs
        )
      except AttributeError:
        oldVal = None
      else:
        oldVal = self._deletedGuard(instance, oldVal)
      self.hookPreDelete(instance, **kwargs)
      self.__instance_delete__(instance, oldVal, **kwargs)
      self.hookOnDelete(instance, **kwargs)
    finally:
      self.exitContext()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __instance_get__(self, instance: Any, owner: type, **kwargs) -> Any:
    """
    A descriptor based on 'Object' needs one place that defines what a
    read of the attribute through an instance gives. A subclass must be
    able to define that place without dealing with the rest of the read:
    keeping track of the instance and owner the read is for, so that
    'self.instance' and 'self.owner' answer during it, calling the
    notification hooks around it, and turning a deleted value into an
    error. A read through the class itself is not its concern. A deletion
    must also be able to learn the current value from the same place,
    without a default being built or stored as a side effect.

    Implementation
    --------------

    '__get__' calls this method when the instance is not 'None', after
    pushing the frame '(instance, owner)' and calling 'hookPreGet', and
    calls 'hookOnGet' afterwards. A result of 'DELETED' becomes
    'MissingVariable'. '__delete__' calls it with '_deleting=True' to
    report the old value. The default returns the descriptor itself.

    Parameters
    ----------

    instance : Any
      The instance the attribute is being read from.

    owner : type
      The class the attribute is being read from. Generally, the
      'instance' above is an instance of 'owner'.

    **kwargs
      '_deleting=True' when '__delete__' asks for the current value.

    Returns
    -------

    Any
      The value to be returned by the read. Subclasses are free to return
      any value, create a value, cause side effects or return the
      descriptor itself.

    Raises
    ------

    Exception
      Subclasses may raise any exception as appropriate.
    """
    return self

  def __instance_set__(self, instance: Any, value: Any, **kwargs) -> Any:
    """
    A descriptor based on 'Object' needs one place that defines what a
    write through an instance does, free of the frame and the hooks, and
    able to report the value it actually stored when that differs from the
    value assigned, as after a cast, so the hook after the write sees the
    truth.

    Implementation
    --------------

    '__set__' calls this method after 'hookPreSet' and hands what it
    returns to 'hookOnSet'. The default refuses, which is what keeps a
    worktoy value in a class body from being replaced through an instance.

    Parameters
    ----------

    instance : Any
      The instance written through.

    value : Any
      The value assigned.

    Returns
    -------

    Any
      The value as stored, or 'None' to report the value as assigned.

    Raises
    ------

    ReadOnlyError
      Always, in the default.
    """
    raise ReadOnlyError(instance, self, value)

  def __instance_delete__(
      self,
      instance: Any,
      old: Any = None,
      **kwargs,
  ) -> None:
    """
    A descriptor based on 'Object' needs one place that defines what a
    deletion through an instance does. The deletion must be visible to the
    next read, which must fail, even for a descriptor that builds a default
    into empty storage.

    Implementation
    --------------

    '__delete__' calls this method with the old value, between
    'hookPreDelete' and 'hookOnDelete'. A reimplementation stores
    'DELETED' where '__instance_get__' reads, and makes it return that
    value. The default refuses.

    Parameters
    ----------

    instance : Any
      The instance deleted through.

    old : Any
      The value held before, or 'None' when it could not be read.

    Raises
    ------

    ProtectedError
      Always, in the default.
    """
    raise ProtectedError(instance, self, old)

  def createContext(self, instance: Any, owner: type, ) -> Self:
    """
    Code driving the protocol by hand, outside '__get__', '__set__' and
    '__delete__', needs to give the descriptor a frame for the instance and
    owner it works with.

    Implementation
    --------------

    The frame is appended to a new copy of the stack. Every call is paired
    with one call of 'exitContext', in a 'finally' block.

    Parameters
    ----------

    instance : Any
      The instance of the frame.

    owner : type
      The owner of the frame.

    Returns
    -------

    Object
      The descriptor itself.
    """
    existing: list[tuple[Any, type]] = maybe(self.__call_chain__, [])
    updated: list[tuple[Any, type]] = [*existing, (instance, owner), ]
    object.__setattr__(self, '__call_chain__', updated)
    return self

  def exitContext(self) -> Self:
    """
    A frame pushed with 'createContext' must be removed when the work is
    done, bringing back the frame below it. A removal without a matching
    push means the protocol was driven wrongly, and must not pass quietly.

    Implementation
    --------------

    The stack is replaced by a copy without its top frame.

    Returns
    -------

    Object
      The descriptor itself.

    Raises
    ------

    WithoutException
      The stack is empty.
    """
    if not self.__call_chain__:
      raise WithoutException(self)
    updated: list[tuple[Any, type]] = self.__call_chain__[:-1]
    object.__setattr__(self, '__call_chain__', updated)
    return self

  def _deletedGuard(self, instance: Any, value: Any, ) -> Any:
    if value is DELETED:
      if self.__field_name__ is None:
        raise MissingVariable(instance, '__field_name__', str)
      raise MissingVariable(instance, self.__field_name__, object)
    return value

  def getPrivateName(self, ) -> str:
    """
    A descriptor written by a project may want a private attribute on each
    instance, named after its field, without choosing the name by hand.

    Implementation
    --------------

    A camelCase field name becomes snake case between double underscores,
    'fooBar' giving '__foo_bar__', and the result is cached. The worktoy
    boxes do not use it. The mapping is not one to one, 'fooBar' and
    'foo_bar' giving the same name, and a short field name can give a name
    Python uses itself, as 'dict' gives '__dict__'. The cache is not
    refreshed if the descriptor is placed again at another name.

    Returns
    -------

    str
      The private name.

    Raises
    ------

    MissingVariable
      The descriptor has not been placed in a class.
    """
    if self.__private_name__ is None:
      if self.__field_name__ is None:
        raise MissingVariable(self, '__field_name__', str)
      spec = _PRIVATE_KEY_PATTERN.sub('_', self.__field_name__).lower()
      snake = '__%s__' % spec
      object.__setattr__(self, '__private_name__', snake)
    if isinstance(self.__private_name__, str):
      return self.__private_name__
    raise TypeException('__private_name__', self.__private_name__, str)

  def hookPreGet(self, instance, **kwargs) -> None:
    """
    A subclass may need to act before every read through an instance, with
    the frame of the read already in place.

    Implementation
    --------------

    The default does nothing.

    Parameters
    ----------

    instance : Any
      The instance read through.
    """

  def hookOnGet(self, instance: Any, value: Any, **kwargs, ) -> None:
    """
    A subclass may need to see the value every read through an instance is
    about to return. It may change a mutable value in place, but cannot
    replace it.

    Implementation
    --------------

    The default does nothing. It is not called for a read through the
    class, nor for the read a deletion makes.

    Parameters
    ----------

    instance : Any
      The instance read through.

    value : Any
      The value about to be returned.
    """

  def hookPreSet(self, instance: Any, value: Any, **kwargs, ) -> None:
    """
    A subclass may need to act before every write through an instance,
    with the value as assigned: to refuse it by raising, or to end a
    redundant write silently with 'SkipSet'.

    Implementation
    --------------

    The default does nothing.

    Parameters
    ----------

    instance : Any
      The instance written through.

    value : Any
      The value as assigned.
    """

  def hookOnSet(self, instance: Any, value: Any, **kwargs, ) -> None:
    """
    A subclass may need to react to every completed write through an
    instance, with the value actually stored.

    Implementation
    --------------

    The default does nothing. It is not called when 'hookPreSet' raised
    'SkipSet'.

    Parameters
    ----------

    instance : Any
      The instance written through.

    value : Any
      The value as stored.
    """

  def hookPreDelete(self, instance: Any, **kwargs, ) -> None:
    """
    A subclass may need to act before every deletion through an instance.

    Implementation
    --------------

    The default does nothing. The old value has been read already.

    Parameters
    ----------

    instance : Any
      The instance deleted through.
    """

  def hookOnDelete(self, instance: Any, **kwargs, ) -> None:
    """
    A subclass may need to react to every completed deletion through an
    instance.

    Implementation
    --------------

    The default does nothing.

    Parameters
    ----------

    instance : Any
      The instance deleted through.
    """

  def hookSetName(self, owner: type, name: str, **kwargs) -> None:
    """
    A subclass may need to react when the descriptor is placed in a class,
    without taking over '__set_name__'.

    Implementation
    --------------

    The default does nothing. The owner and name are recorded before it
    is called.

    Parameters
    ----------

    owner : type
      The class the descriptor is placed in.

    name : str
      The name it is placed at.
    """

  @classmethod
  def parseKwargs(cls, *args, **kwargs) -> tuple[Any, dict]:
    """
    An option given by keyword may go by several names, as 'frozen' or
    'readOnly', and must still be read once, checked for its type, and
    removed from the keywords passed on.

    Implementation
    --------------

    The positional arguments are the accepted names, as strings, and the
    accepted types, as classes. The first name present is taken and
    removed from a copy of the keywords; a second synonym given as well
    stays. A number type admits the narrower number types, 'float' an
    'int' and 'complex' both, and a 'bool' passes as an 'int'. The value is
    returned as given, not cast.

    Parameters
    ----------

    *args
      The accepted names and types, in any order.

    **kwargs
      The keywords to search.

    Returns
    -------

    tuple[Any, dict]
      The value found and the remaining keywords, or 'None' and a copy of
      the keywords when no name is present.

    Raises
    ------

    TypeException
      A name is present with a value of none of the accepted types.
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

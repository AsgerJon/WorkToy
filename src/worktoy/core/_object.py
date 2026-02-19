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

from ..utilities import Directory, maybe, textFmt
from ..waitaminute import TypeException, attributeErrorFactory
from ..waitaminute.desc import AccessError
from .sentinels import THIS, DESC, OWNER, DELETED, Sentinel
from . import ContextInstance, MetaType, ContextOwner

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Self, Optional, Type, TypeAlias
  from types import TracebackType

  ExcType: TypeAlias = Optional[Type[Exception]]
  ExcVal: TypeAlias = Optional[Exception]
  Trace: TypeAlias = Optional[TracebackType]


class Object(metaclass=MetaType):
  """
  Fundamental base class for all objects in the 'worktoy' library.

  This class provides full-featured descriptor context management. When
  subclassing, you need only implement `__instance_get__`,
  `__instance_set__`, and `__instance_delete__`. The owning instance
  is always made available as `self.instance` within these methods.

  Deletion is handled by assigning the `DELETED` sentinel to the relevant
  attribute or storage, so that a future call to `__instance_get__` will
  return `DELETED`. The core machinery ensures this triggers an
  AttributeError on access.

  Example implementation:
    .. code-block:: python

    def __instance_get__(self) -> Any:
      return self.instance._value

    def __instance_set__(self, value: Any) -> None:
      self.instance._value = value

    def __instance_delete__(self, oldVal: Any) -> None:
      self.instance._value = DELETED  # Ensures next get raises
      AttributeError

  Do not override `__get__`, `__set__`, or `__delete__` unless you are
  extending or altering the core behavior. Context, error handling, and
  attribute protection are managed by Object and its metaclass.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables

  #  Private Variables
  __field_owner__ = None
  __field_name__ = None
  __pos_args__ = None
  __key_args__ = None
  __context_instance__ = None
  __context_owner__ = None
  __call_chain__ = []

  #  Public Variables
  directory = Directory()
  instance = ContextInstance()
  owner = ContextOwner()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def getFieldOwner(self) -> type:
    """Getter for the field owner of the descriptor object"""
    return self.__field_owner__

  def getFieldName(self) -> Optional[str]:
    """Getter for the field name of the descriptor object"""
    return self.__field_name__

  def getContextualSentinels(self, ) -> dict[Type[Sentinel], Any]:
    """
    Returns a dictionary mapping the sentinels 'THIS', 'OWNER', and 'DESC'
    to their corresponding contextual values. Where contextual values are
    not available, the sentinel is returned.
    """
    return {
      THIS: maybe(self.__context_instance__, THIS),
      OWNER: maybe(self.__context_owner__, OWNER),
      DESC: self,
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
    """Getter for the positional arguments of the object."""
    out = []
    for arg in maybe(self.__pos_args__, ()):
      out.append(self.filterSentinels(arg))
    return (*out,)

  def getKeyArgs(self, ) -> dict[str, Any]:
    """Getter for the keyword arguments of the object."""
    out = dict()
    for key, value in self.__key_args__.items():
      out[key] = self.filterSentinels(value)
    return out

  def getContextInstance(self) -> Any:
    """Returns the contextual instance or raises 'WithoutException'"""
    if self.hasContext():
      return self.__context_instance__
    from ..waitaminute.desc import WithoutException
    raise WithoutException(self)

  def getContextOwner(self) -> type:
    """Returns the contextual owner or raises 'WithoutException'"""
    if self.hasContext():
      return self.__context_owner__
    from ..waitaminute.desc import WithoutException
    raise WithoutException(self)

  def hasContext(self) -> bool:
    """
    Returns True if the descriptor has a context, i.e. if it has been
    created with 'createContext' and not exited with 'exitContext'.
    """
    own = self.__context_owner__
    ins = self.__context_instance__
    if (ins is None) ^ (own is None):
      infoSpec = """Encountered inconsistent context state! The context 
      owner and instance must both be 'None' or neither be 'None', 
      but received instance: '%s' and owner: '%s'."""
      info = infoSpec % (str(ins), str(own))
      raise RuntimeError(textFmt(info, ))
    if own is None:
      return False
    return True

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, *args: Any, **kwargs: Any) -> None:
    object.__init__(self)
    self.__pos_args__ = args
    self.__key_args__ = kwargs

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __set_name__(self, owner: type, name: str) -> None:
    self.__field_owner__ = owner
    self.__field_name__ = name

  def __get__(self, instance: Any, owner: type, **kwargs) -> Any:
    """
    Returns the root of the descriptor owning the hook.
    """
    if instance is None:
      return self
    with self.createContext(instance, owner) as context:
      value = context.__instance_get__(instance, owner, **kwargs)
    return self._deletedGuard(instance, value)

  def __set__(self, instance: Any, newValue: Any, **kwargs) -> None:
    """
    Sets the value of the descriptor in the instance. If accessing an
    attribute would raise an exception, it should not prevent setting a
    value on that attribute. Since the 'setter' control flow
    """
    with self.createContext(instance, type(instance)) as context:
      context.__instance_set__(instance, newValue, **kwargs)

  def __delete__(self, instance: Any, **kwargs) -> None:
    """
    Deletes the value of the descriptor in the instance.
    """
    owner = type(instance)
    with self.createContext(instance, type(instance)) as context:
      try:
        oldVal = context.__instance_get__(instance, owner, **kwargs)
      except AttributeError:
        oldVal = None
      else:
        oldVal = self._deletedGuard(instance, oldVal)
      context.__instance_delete__(instance, oldVal, **kwargs)

  def __enter__(self, ) -> Self:
    """
    Must be used with along with 'enterContext(instance, owner)'.
    """
    if self.hasContext():
      return self
    from ..waitaminute.desc import WithoutException
    raise WithoutException(self)

  def __exit__(self, _, exception: BaseException, __) -> None:
    """
    Must be used with along with 'exitContext'.
    """
    try:
      if exception is not None:
        raise exception
    finally:
      self.exitContext()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __instance_get__(self, instance: Any, owner: type, **kwargs) -> Any:
    """
    Instance-specific getter for this descriptor.

    When called, `self.instance` is the object this descriptor is bound to.
    Subclasses should override this to define attribute retrieval logic.

    Returns:
      Any: The attribute value, or the DELETED sentinel if deleted.

    Example:
      .. code-block:: python
      return self.instance._value
    """
    return self

  def __instance_set__(self, instance: Any, value: Any, **kwargs) -> None:
    """
    Instance-specific setter for this descriptor.

    When called, `self.instance` is the object this descriptor is bound to.
    Subclasses should override to define attribute assignment logic.

    Example:
      .. code-block:: python
      self.instance._value = value
    """
    from ..waitaminute.desc import ReadOnlyError
    raise ReadOnlyError(instance, self, value)

  def __instance_delete__(
      self,
      instance: Any,
      old: Any = None,
      **kwargs,
      ) -> None:
    """
    Instance-specific deleter for this descriptor.

    To signal deletion, assign the `DELETED` sentinel to your storage,
    so that the next `__instance_get__` returns `DELETED`. This ensures
    the core will raise AttributeError on further access.

    Example:
      .. code-block:: python
      self.instance._value = DELETED
    """
    from ..waitaminute.desc import ProtectedError
    raise ProtectedError(instance, self, old)

  def createContext(self, instance: Any, owner: type, ) -> Self:
    """
    Creates a context for the descriptor. The context is used to
    store the instance and owner of the descriptor.
    """
    self.__context_instance__ = instance
    self.__context_owner__ = owner
    return self

  def exitContext(self) -> Self:
    """
    Exits the context of the descriptor. The method restores the
    descriptor to its previous state.
    """
    self.__context_instance__ = None
    self.__context_owner__ = None
    return self

  def _deletedGuard(self, instance: Any, value: Any, ) -> Any:
    """
    A guard that raises an exception if the value is 'DELETED'. This is
    used to prevent accessing deleted attributes.
    """
    if value is DELETED:
      attributeError = attributeErrorFactory(instance, self.__field_name__)
      raise AttributeError(attributeError)
    return value

  def getPrivateName(self, ) -> str:
    """
    Returns the name chain of the descriptor. This is used to access
    the name of the descriptor in the context of the instance.
    """
    fieldName = self.__field_name__
    pattern = re.compile(r'(?<!^)(?=[A-Z])')
    return '__%s__' % pattern.sub('_', fieldName).lower()

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

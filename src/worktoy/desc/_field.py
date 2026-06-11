"""
Field is a property-like descriptor whose accessors are methods decorated
in the class body.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from . import BaseDescriptor
from ..utilities import maybe
from ..waitaminute import TypeException
from ..waitaminute.desc import ProtectedError, ReadOnlyError, AccessError

T = TypeVar('T')

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Any, Callable, Optional
  from typing import Self

  MaybeStr: TypeAlias = Optional[str]

  StrTuple: TypeAlias = tuple[str, ...]
  MaybeStrTuple: TypeAlias = Optional[StrTuple]

  CallMeMaybe: TypeAlias = Callable[..., Any]
  MaybeBool: TypeAlias = Optional[bool]


class Field(BaseDescriptor[T]):
  """
  Flexible descriptor requiring accessor methods to be decorated. Please
  note that the instance of 'Field' can decorate only methods appearing
  below it in the class body.

  @GET - Marks the getter, called as 'method(self)'. Only one getter is
  kept: a second '@GET' silently replaces the first. Reading a 'Field'
  with no getter raises 'AccessError'.

  @SET - Decorate any number of methods as setters. Every such method runs
  in response to __set__

  @DELETE - Decorate any number of methods as deleters. Optionally, implement
  by setting the value to the 'DELETED' sentinel object.

  Notes
  -----
  The accessors are stored by name, not as captured function objects. A
  decorator such as 'GET' records 'callMeMaybe.__name__', and at access
  time '__instance_get__' looks that name up with 'getattr(owner, key)',
  where 'owner' is the type of the instance being accessed rather than
  the class in which the 'Field' was declared. Setters and deleters
  resolve the same way.

  The consequence is that a subclass overrides any decorated accessor
  just by redefining a method of the same name, with no need to decorate
  it again: the name lookup finds the override. A subclass that redefines
  an inherited '_getValue' as a plain method changes what the inherited
  'Field' returns, because the parent never captured the decorated method,
  only its name. The sampler hierarchy in 'worktoy.work_test' relies on
  exactly this, where 'FloatSampler' replaces the 'int' accessors it
  inherits from 'IntSampler' with floating-point versions.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __prototype_object__: Optional[Self] = None

  # -- Accessor Keys
  __get_key__ = None
  __set_keys__ = None
  __delete_keys__ = None

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _getGetterKey(self) -> str:
    if self.__get_key__ is None:
      raise AccessError(self)
    if isinstance(self.__get_key__, str):
      return self.__get_key__
    raise TypeException('__get_key__', self.__get_key__, str)

  def _getSetterKeys(self, ) -> tuple[str, ...]:
    return (*[k for k in maybe(self.__set_keys__, ()) if k],)

  def _getDeleterKeys(self) -> tuple[str, ...]:
    return (*[k for k in maybe(self.__delete_keys__, ()) if k],)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def GET(self, callMeMaybe: Callable) -> Callable:
    """
    The 'GET' decorator marks the getter, called as 'method(self)'.
    Only one getter is kept: a second '@GET' silently replaces the
    first. Reading a 'Field' with no getter raises 'AccessError'.

    Parameters
    ----------
    callMeMaybe : Callable
        The method to register as the getter.

    Returns
    -------
    Callable
        The same method, unchanged, so the name stays bound in the
        class body.
    """
    self.__get_key__ = callMeMaybe.__name__
    return callMeMaybe

  def SET(self, callMeMaybe: Callable) -> Callable:
    """
    The 'SET' decorator marks a setter. Any number may be registered;
    each is called as 'method(self, value)' in registration order on
    every assignment, where 'value' is the incoming value. If no setter
    is registered, assignment raises 'ReadOnlyError'.

    Parameters
    ----------
    callMeMaybe : Callable
        The method to register as a setter.

    Returns
    -------
    Callable
        The same method, unchanged, so the name stays bound in the
        class body.
    """
    existing = maybe(self.__set_keys__, ())
    self.__set_keys__ = (*existing, callMeMaybe.__name__,)
    return callMeMaybe

  def DELETE(self, callMeMaybe: Callable) -> Callable:
    """
    The 'DELETE' decorator marks a deleter. Any number may be
    registered; each is called as 'method(self)' in registration order
    on 'del'. If no deleter is registered, 'del' raises
    'ProtectedError'.

    Parameters
    ----------
    callMeMaybe : Callable
        The method to register as a deleter.

    Returns
    -------
    Callable
        The same method, unchanged, so the name stays bound in the
        class body.
    """
    existing = maybe(self.__delete_keys__, ())
    self.__delete_keys__ = (*existing, callMeMaybe.__name__,)
    return callMeMaybe

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PARENT METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __instance_get__(self, instance: Any, owner: type, **kwargs) -> Any:
    """
    The '__instance_get__' method retrieves the getter by its
    registered name from the owner of the instance and calls it. While
    the instance received is certain to satisfy
    'isinstance(instance, self.getFieldOwner())', the field owner is the
    class where the descriptor was instantiated. For this reason the
    decorated method is retrieved by name from the owner of the instance
    received, so a subclass override is honoured.
    """
    getterKey = self._getGetterKey()
    getterFunc = getattr(owner, getterKey)
    return getterFunc(instance, **kwargs)

  def __instance_set__(self, instance: Any, value: Any, **kwargs) -> None:
    """
    The '__instance_set__' method retrieves every decorated setter by
    name in the same fashion as the getter and calls each in
    registration order. With no setter registered, assignment raises
    'ReadOnlyError'.
    """
    setterKeys = self._getSetterKeys()
    owner = type(instance)
    if not setterKeys:
      raise ReadOnlyError(instance, self, value, )
    for key in setterKeys:
      setterFunc = getattr(owner, key, )
      setterFunc(instance, value, )

  def __instance_delete__(self, instance: Any, *_, **kwargs) -> None:
    """
    The '__instance_delete__' method retrieves every decorated deleter
    by name in the same fashion as the getter and calls each in
    registration order. With no deleter registered, deletion raises
    'ProtectedError'.
    """
    deleterKeys = self._getDeleterKeys()
    owner = type(instance)
    if not deleterKeys:
      try:
        oldVal = self.__instance_get__(instance, owner, **kwargs)
      except AttributeError:
        oldVal = None
      raise ProtectedError(instance, self, oldVal)
    for key in deleterKeys:
      deleterFunc = getattr(owner, key, )
      deleterFunc(instance, **kwargs)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, other: Self = None) -> None:
    BaseDescriptor.__init__(self, other)
    if isinstance(other, Field):
      self.__prototype_object__ = other
      self.__get_key__ = other.__get_key__
      keyGroups = (
        '__pre_get_keys__',
        '__on_get_keys__',
        '__pre_set_keys__',
        '__on_set_keys__',
        '__pre_delete_keys__',
        '__on_delete_keys__',
        '__set_keys__',
        '__delete_keys__',
      )
      for keyGroup in keyGroups:
        otherValue = getattr(other, keyGroup)
        if otherValue is not None:
          setattr(self, keyGroup, (*otherValue,))
    elif other is not None:
      raise TypeException('other', other, type(self))

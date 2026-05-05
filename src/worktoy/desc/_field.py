"""
Field provides a property-like descriptor implementation allowing
descriptor owners to decorate methods to designate them as accessors.
Since these are identified by name, the function object are entirely
unaffected by the decoration and subclasses can override any decorated
method and the descriptor uses the overridden method instead.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from . import BaseDescriptor
from ..utilities import maybe
from ..waitaminute import TypeException
from ..waitaminute.desc import ProtectedError, ReadOnlyError, AccessError

T = TypeVar('T')

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Any, Callable, TypeAlias, Optional
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

  @GET - Decorate one method designating it as the 'getter'. It should be
  a normal instance method that can be run without any other arguments.

  @SET - Decorate any number of methods as setters. Every such method runs
  in response to __set__

  @DELETE - Decorate any number of methods as deleters. Optionally, implement
  by setting the value to the 'DELETED' sentinel object.
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
    if not isinstance(self.__get_key__, str):
      raise AccessError(self)
    return self.__get_key__

  def _getSetterKeys(self, ) -> tuple[str, ...]:
    return (*[k for k in maybe(self.__set_keys__, ()) if k],)

  def _getDeleterKeys(self) -> tuple[str, ...]:
    return (*[k for k in maybe(self.__delete_keys__, ()) if k],)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def GET(self, callMeMaybe: Callable) -> Callable:
    """
    Decorator for the getter method. The method should be a normal instance
    method that can be run without any other arguments.
    """
    self.__get_key__ = callMeMaybe.__name__
    return callMeMaybe

  def SET(self, callMeMaybe: Callable) -> Callable:
    """
    Decorator for the setter method. The method should be a normal instance
    method that can be run without any other arguments.
    """
    existing = maybe(self.__set_keys__, ())
    self.__set_keys__ = (*existing, callMeMaybe.__name__,)
    return callMeMaybe

  def DELETE(self, callMeMaybe: Callable) -> Callable:
    """
    Decorator for the deleter method. The method should be a normal instance
    method that can be run without any other arguments.
    """
    existing = maybe(self.__delete_keys__, ())
    self.__delete_keys__ = (*existing, callMeMaybe.__name__,)
    return callMeMaybe

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PARENT METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __instance_get__(self, instance: Any, owner: type, **kwargs) -> Any:
    """
    Retrieves the getter from the owner of instance and the registered
    name of getter function. Please note that while the instance received
    is certain to satisfy: isinstance(instance, self.getFieldOwner()),
    the field owner is the class where the descriptor was instantiated.
    For this reason, the decorated method is retrieved by name from the
    owner of the instance received.
    """
    getterKey = self._getGetterKey()
    getterFunc = getattr(owner, getterKey)
    return getterFunc(instance, **kwargs)

  def __instance_set__(self, instance: Any, value: Any, **kwargs) -> None:
    """
    All decorated setters are retrieved in the same fashion as the getter.
    """
    setterKeys = self._getSetterKeys()
    owner = type(instance)
    if not setterKeys:
      raise ReadOnlyError(self.instance, self, value, )
    for key in setterKeys:
      setterFunc = getattr(owner, key, )
      setterFunc(instance, value, )

  def __instance_delete__(
      self,
      instance: Any,
      old: Any = None,
      **kwargs,
  ) -> None:
    """
    All decorated deleters are retrieved in the same fashion as the getter.
    """
    deleterKeys = self._getDeleterKeys()
    owner = type(instance)
    if not deleterKeys:
      try:
        oldVal = self.__instance_get__(instance, owner, **kwargs)
      except AttributeError:
        oldVal = None
      raise ProtectedError(self.instance, self, oldVal)
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

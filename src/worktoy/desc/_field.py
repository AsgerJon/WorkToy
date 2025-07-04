"""
Field provides a property-like descriptor implementation allowing
descriptor owners to decorate methods to designate them as accessors.
Since these are identified by name, the function object are entirely
unaffected by the decoration and subclasses can override any decorated
method and the descriptor uses the overridden method instead.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from types import FunctionType as Func

from ..core import Object
from ..utilities import maybe
from ..waitaminute import MissingVariable, TypeException
from ..waitaminute import attributeErrorFactory
from ..waitaminute.desc import ProtectedError, ReadOnlyError, AccessError

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Callable, Iterator


class Field(Object):
  """
  Flexible descriptor requiring accessor methods to be decorated. Please
  note that the instance of 'Field' can decorate only methods appearing
  below it in the class body.

  @GET - Decorate one method designating it as the 'getter'. It should be
  a normal instance method that can be run without any other arguments.

  @SET - Decorate any number of methods as setters. Every such method runs
  in response to __set__

  @DEL - Decorate any number of methods as deleters. Optionally, implement
  by setting the value to the 'DELETED' sentinel object.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __get_key__ = None
  __set_keys__ = None
  __delete_keys__ = None

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _getGetterKey(self) -> str:
    if isinstance(self.__get_key__, str):
      return self.__get_key__
    if self.__get_key__ is None:
      raise AccessError(self)
    raise TypeException('__get_key__', self.__get_key__, str)

  def _getSetterKeys(self, newValue: Any = None) -> Iterator[str]:
    """Iterates over setter keys. The 'newValue' is used only to compose
    error message. """
    if isinstance(self.__set_keys__, (tuple, list)):
      key = None
      for key in self.__set_keys__:
        if not isinstance(key, str):
          raise TypeException('key', key, str)
        yield key
      else:
        if key is None:  # Happens only with empty key list
          raise ReadOnlyError(self, newValue)
        return
    elif self.__set_keys__ is None:
      return
    else:
      raise TypeException('__set_keys__', self.__set_keys__, tuple, list)

  def _getDeleterKeys(self) -> Iterator[str]:
    if isinstance(self.__delete_keys__, (tuple, list)):
      key = None
      for key in maybe(self.__delete_keys__, ()):
        if not isinstance(key, str):
          raise TypeException('key', key, str)
        yield key
      else:
        if key is None:
          return
    elif self.__delete_keys__ is None:
      instance = self.getContextInstance()
      owner = self.getContextOwner()
      ownerName = owner.__name__
      getterKey = self._getGetterKey()
      try:
        oldVal = getattr(instance, getterKey, )
      except AttributeError as attributeError0:
        attributeError = attributeErrorFactory(ownerName, getterKey)
        raise attributeError from attributeError0
      else:
        raise ProtectedError(instance, self, oldVal)
    else:
      raise TypeException('__del_keys__', self.__delete_keys__, tuple, list)

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
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __instance_get__(self, *args, **kwargs) -> Any:
    """
    Retrieves the getter from the owner of instance and the registered
    name of getter function. Please note that while the instance received
    is certain to satisfy: isinstance(instance, self.getFieldOwner()),
    the field owner is the class where the descriptor was instantiated.
    For this reason, the decorated method is retrieved by name from the
    owner of the instance received.
    """
    getterKey = self._getGetterKey()
    getterFunc = getattr(self.getContextInstance(), getterKey, )
    if getterFunc is None:
      raise MissingVariable(getterKey, Func, )
    if not callable(getterFunc):
      raise TypeException('getterFunc', getterFunc, Func, )
    return getterFunc(*args, **kwargs)

  def __instance_set__(self, val: Any, *args, **kwargs) -> None:
    """
    All decorated setters are retrieved in the same fashion as the getter.
    """
    instance = self.getContextInstance()
    for key in self._getSetterKeys(val):
      setterFunc = getattr(instance, key, )
      if setterFunc is None:
        owner = self.getContextOwner()
        ownerName = owner.__name__
        raise MissingVariable(key, Func, )
      if not callable(setterFunc):
        raise TypeException('setterFunc', setterFunc, Func, )
      setterFunc(val, *args, **kwargs)

  def __instance_delete__(self, *args, **kwargs) -> None:
    """
    All decorated deleters are retrieved in the same fashion as the getter.
    """
    instance = self.getContextInstance()
    for key in self._getDeleterKeys():
      getattr(instance, key, )(**kwargs)

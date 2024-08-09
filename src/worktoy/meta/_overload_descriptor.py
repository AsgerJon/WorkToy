"""Overload provides a class for overloading methods in a class."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from random import randint

from worktoy.parse import maybe
from worktoy.text import monoSpace
from worktoy.meta import Dispatcher, TypeSig

try:
  from typing import Any, Callable, TYPE_CHECKING
except ImportError:
  Any = object
  Callable = object
  TYPE_CHECKING = False

if TYPE_CHECKING:
  FuncList = list[tuple[TypeSig, Callable]]
else:
  FuncList = object


class Overload:
  """Overload provides a class for overloading methods in a class."""

  __function_name__ = None
  __function_owner__ = None
  __func_list__ = None
  __dispatcher_instance__ = None
  __class_method__ = None
  __static_method__ = None
  __instance_id__ = None

  def __init__(self, functionType: type = None) -> None:
    self.__instance_id__ = randint(0, 255)
    self.__static_method__ = False
    self.__class_method__ = False
    self.__func_list__ = []
    if functionType is not None:
      if functionType is staticmethod:
        self.__static_method__ = True
        self.__class_method__ = False
      elif functionType is classmethod:
        self.__static_method__ = False
        self.__class_method__ = True
      else:
        e = """Received invalid function type: '%s'! Only 'staticmethod'
        and 'classmethod' are allowed!"""
        raise TypeError(monoSpace(e % functionType))

  def __set_name__(self, owner: type, name: str) -> None:
    """Set the name of the field and the owner of the field. When this
    method is called the owner is created, so it is safe for the overload
    instance to create the Dispatcher instance. """
    self.__function_owner__ = owner
    clsName = '%sOverload' % name
    setattr(owner, clsName, self)
    self.__function_name__ = name
    self.__dispatcher_instance__ = Dispatcher(self, self.getFuncList(), )

  def __get__(self, instance: object, owner: type) -> Any:
    """Getter-function"""
    if instance is None:
      return self._classGetter(owner)
    return self._instanceGetter(instance)

  def _classGetter(self, owner: type) -> Any:
    """Getter-function for the class."""
    if self.__class_method__:
      self.__dispatcher_instance__.setBound(owner)
      return self.__dispatcher_instance__
    return self

  def _instanceGetter(self, instance: object) -> Any:
    """Getter-function for the instance. This returns the dispatcher. """
    self.__dispatcher_instance__.setBound(instance)
    return self.__dispatcher_instance__

  def getFuncList(self) -> FuncList:
    """Getter-function for the function dictionary."""
    return maybe(self.__func_list__, [])

  def overload(self, *types) -> Callable:
    """The overload function returns a callable that decorates a function
    with
    the signature. """
    key = TypeSig(*types)

    def decorator(callMeMaybe: Callable) -> Callable:
      """The decorator function that adds the function to the function
      dictionary."""
      if isinstance(callMeMaybe, staticmethod):
        if not self.__static_method__:
          e = """The 'Overload' instance is not a static method!"""
          raise TypeError(e)
      if isinstance(callMeMaybe, classmethod):
        if not self.__class_method__:
          e = """The 'Overload' instance is not a class method!"""
          raise TypeError(e)
      self.__func_list__.append((key, callMeMaybe))
      return callMeMaybe

    return decorator

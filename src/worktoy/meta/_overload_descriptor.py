"""Overload provides a class for overloading methods in a class."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from random import randint

from worktoy.parse import maybe
from worktoy.text import monoSpace, typeMsg
from worktoy.meta import Dispatcher, TypeSig, OverloadException

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
  __deferred_funcs__ = None
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
    clsName = '%sOverload' % name
    setattr(owner, clsName, self)
    self._setFunctionOwner(owner)
    self._setFunctionName(name)
    self.__dispatcher_instance__ = Dispatcher(self, self.getFuncList(), )

  def _setFunctionOwner(self, owner: type) -> None:
    """Setter-function for the function owner."""
    if self.__function_owner__ is not None:
      oldName = self.__function_owner__.__name__
      newName = owner.__name__
      print("""Owner changed from '%s' to '%s'!""" % (oldName, newName))
      # e = """The function owner of the '%s' instance is already set!"""
      # raise OverloadException(monoSpace(e % self.__class__.__name__))
    if not isinstance(owner, type):
      e = typeMsg('owner', owner, type)
      raise TypeError(e)
    self.__function_owner__ = owner
    self._compileFuncList()

  def _getFunctionOwner(self) -> type:
    """Getter-function for the function owner."""
    if self.__function_owner__ is None:
      e = """The function owner of the '%s' instance is accessed before 
      '__set_name__' has been called!"""
      raise OverloadException(monoSpace(e % self.__class__.__name__))
    if isinstance(self.__function_owner__, type):
      return self.__function_owner__
    e = typeMsg('self.__function_owner__', self.__function_owner__, type)
    raise TypeError(e)

  def _setFunctionName(self, name: str, ) -> None:
    """Setter-function for the function name"""
    if self.__function_name__ is not None:
      print("""Renamed from '%s' to '%s'""" % (self.__function_name__, name))
      # e = """The function name of the '%s' instance is already set!"""
      # raise OverloadException(monoSpace(e % self.__class__.__name__))
    if not isinstance(name, str):
      e = typeMsg('name', name, str)
      raise TypeError(e)
    self.__function_name__ = name

  def _getFunctionName(self, ) -> str:
    """Getter-function for the function name"""
    if self.__function_name__ is None:
      e = """The function name of the '%s' instance is accessed before 
      '__set_name__' has been called!"""
      raise OverloadException(monoSpace(e % self.__class__.__name__))
    if isinstance(self.__function_name__, str):
      return self.__function_name__
    e = typeMsg('self.__function_name__', self.__function_name__, str)
    raise TypeError

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

  def overload(self, *types) -> Callable:
    """The overload function returns a callable that decorates a function
    with the signature. """

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
      existing = maybe(self.__deferred_funcs__, [])
      self.__deferred_funcs__ = [*existing, ((*types,), callMeMaybe)]
      return callMeMaybe

    return decorator

  def _compileFuncList(self, ) -> None:
    """Creates TypeSig instances for the function list. Please note that
    this method is meant to be invoked only after the owning class has
    been created. This permits the use of 'THIS' in overloaded functions.
    This allows overloading functions to instances of the same class."""
    for (types, callMeMaybe) in self.getDeferredFuncs():
      finalTypes = []
      for type_ in types:
        if getattr(type_, '__THIS_ZEROTON__', None) is None:
          finalTypes.append(type_)
          continue
        finalTypes.append(self._getFunctionOwner())
      self.setFunc(TypeSig(*finalTypes, ), callMeMaybe)

  def getFuncList(self) -> FuncList:
    """Getter-function for the function list."""
    return maybe(self.__func_list__, [])

  def getDeferredFuncs(self) -> FuncList:
    """Getter-function for the deferred functions."""
    return maybe(self.__deferred_funcs__, [])

  def setFunc(self, key: TypeSig, func: Callable) -> None:
    """Set the function for the given type signature."""
    existing = self.getFuncList()
    self.__func_list__ = [*existing, (key, func)]

  def getFunc(self, key: TypeSig) -> Callable:
    """Get the function for the given type signature."""
    for (sig, func) in self.getFuncList():
      if sig == key:
        return func
    e = """No function found for the type signature: '%s'!"""
    raise KeyError(monoSpace(e % key))

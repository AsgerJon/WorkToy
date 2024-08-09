"""OverloadDispatcher class for dispatching overloaded functions."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.meta import DispatchException, TypeSig
from worktoy.text import monoSpace

try:
  from typing import Any, Callable, TYPE_CHECKING
except ImportError:
  Any = object
  Callable = object
  TYPE_CHECKING = False

if TYPE_CHECKING:
  from worktoy.meta import Overload

if TYPE_CHECKING:
  FuncList = list[tuple[TypeSig, Callable]]
else:
  FuncList = object


class Dispatcher:
  """Dispatcher is the class responsible for calling the correct overloaded
  function based on received arguments. """
  __static_method__ = None
  __class_method__ = None
  __func_dict__ = None
  __overload_function__ = None
  __bound_arg__ = None

  def __init__(self, func: Overload, funcList: FuncList) -> None:
    """Initialize the Dispatcher with the function dictionary and the
    function
    type."""
    self.__overload_function__ = func
    self.__func_dict__ = funcList
    self.__static_method__ = func.__static_method__
    self.__class_method__ = func.__class_method__

  def getFuncList(self) -> FuncList:
    """Return the function dictionary."""
    return self.__func_dict__

  def setBound(self, arg: object) -> None:
    """Set the bound argument."""
    self.__bound_arg__ = arg

  def getBound(self, ) -> object:
    """Return the bound argument."""
    return self.__bound_arg__

  def getOverload(self) -> Overload:
    """Return the Overload instance."""
    return self.__overload_function__

  def __call__(self, *args, **kwargs) -> Any:
    """Calling the dispatcher handles the dispatching of the correct
    function"""
    bound = self.getBound()
    argTypes = [type(arg).__name__ for arg in args]
    typeSig, callMeMaybe = None, None
    for (typeSig, callMeMaybe) in self.getFuncList():
      if len(typeSig) != len(args):
        continue
      arg = typeSig.cast(*args)
      if arg is None:
        continue
      break
    else:
      raise DispatchException(self.getOverload(), *args)
    if not callable(callMeMaybe):
      raise DispatchException(self.getOverload(), *args)
    if bound is None:
      return callMeMaybe(*arg, **kwargs)
    return callMeMaybe(bound, *arg, **kwargs)

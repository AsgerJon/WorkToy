"""Dispatcher is the class responsible for calling the correct overloaded
function based on received arguments. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Callable, Any

Overloaded = dict[tuple[type, ...], Callable]


class Dispatcher:
  """Dispatcher is the class responsible for calling the correct overloaded
  function based on received arguments. """

  __overloaded_functions__ = None

  def __init__(self, overloadedFunctions: Overloaded) -> None:
    self.__overloaded_functions__ = overloadedFunctions

  def functionFactory(self, ) -> Callable:
    """Return a function that calls the dispatcher."""

    f = self.__overloaded_functions__

    def callMeMaybe(this: Any, *args) -> Any:
      """Call the dispatcher."""
      typeSig = (*[type(arg) for arg in args],)
      func = self.__overloaded_functions__.get(typeSig, None)
      if func is None:
        args = [float(arg) if isinstance(arg, int) else arg for arg in args]
        typeSig = (*[type(arg) for arg in args],)
        func = self.__overloaded_functions__.get(typeSig, None)
      if callable(func):
        return self.__overloaded_functions__.get(typeSig, None)(this, *args)
      print(typeSig)
      return NotImplemented

    return callMeMaybe

  def staticFactory(self, ) -> Callable:
    """Return a static method that calls the dispatcher."""

    def callMeMaybe(*args) -> Any:
      """Call the dispatcher."""
      typeSig = tuple([type(arg) for arg in args])
      return self.__overloaded_functions__.get(typeSig, None)(*args)

    return callMeMaybe

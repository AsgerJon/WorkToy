"""Dispatcher is the class responsible for calling the correct overloaded
function based on received arguments. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Callable, Any, Optional

Overloaded = dict[tuple[type, ...], Callable]


class Dispatcher:
  """Dispatcher is the class responsible for calling the correct overloaded
  function based on received arguments. """

  __overloaded_functions__ = None
  __bound_arg__ = None
  __static_method__ = None
  __class_method__ = None

  def __init__(self,
               overloadedFunctions: Overloaded,
               functionType: type) -> None:
    self.__overloaded_functions__ = overloadedFunctions
    if functionType is staticmethod:
      self.__static_method__ = True
      self.__class_method__ = False
    elif functionType is classmethod:
      self.__static_method__ = False
      self.__class_method__ = True
    else:
      self.__static_method__ = False
      self.__class_method__ = False

  def __call__(self, *args, **kwargs) -> Any:
    """The '__bound_arg__' provides the object to which this is bounded.
    If it covers a static method, no object is ever bounded, if a class
    method, the owner is bounded, and if an instance method, the instance is
    bounded. """
    if self.__bound_arg__ is None:  # Unbounded
      this = args[0]
      args = args[1:]
    else:  # bounded
      this = self.__bound_arg__
    typeSig = tuple(type(arg) for arg in args)
    func = self.__overloaded_functions__.get(typeSig, None)
    if func is None:
      floatSig = (*[float if arg is int else arg for arg in typeSig],)
      func = self.__overloaded_functions__.get(floatSig, None)
    if func is None:
      intArgs, intSig = [], []
      for arg in args:
        if isinstance(arg, float):
          if float.is_integer(arg):
            intArgs.append(arg)
            intSig.append(int)
          else:
            intArgs.append(arg)
            intSig.append(float)
        else:
          intArgs.append(arg)
          intSig.append(type(arg))
      intSig, intArgs = (*intSig,), (*intArgs,)
      func = self.__overloaded_functions__.get(intSig, None)
      if func is not None:
        return func(this, *intArgs, **kwargs)
    if func is None:
      for keyTypes, callMeMaybe in self.__overloaded_functions__.items():
        if len(keyTypes) == len(args):
          for keyType, arg in zip(keyTypes, args):
            if not isinstance(arg, keyType):
              break
          else:
            func = callMeMaybe
            break
      else:
        e = """Unable to match arguments to any overloaded function!"""
        raise ValueError(e)
    return func(this, *args, **kwargs)

  def __get__(self, instance: object, owner: type) -> Optional[Callable]:
    """Getter-function for descriptor protocol"""
    if self.__class_method__:
      self.__bound_arg__ = owner
    elif self.__static_method__:
      self.__bound_arg__ = None
    else:
      self.__bound_arg__ = instance
    return self

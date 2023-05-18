"""This abstract metaclass registers any callable object as an instance."""
#  MIT License
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any, NoReturn, Callable, Never
from warnings import warn

from worktoy import AnywayUWantIt, searchKeys, maybeType, maybe, monoSpace


class CallMeMaybe(metaclass=AnywayUWantIt):
  """This abstract metaclass registers any callable object as an instance."""

  _explicits = []
  _callables = []
  _unCallables = []
  _unCallableFunctions = []

  @staticmethod
  def recognizeInstance(instance: Any = None) -> bool:
    """Recognizing anything callable as an instance"""
    for callableType in CallMeMaybe._callables:
      if isinstance(instance, callableType):
        return True
    for unCallableType in CallMeMaybe._unCallables:
      if isinstance(instance, unCallableType):
        return False
    if instance in CallMeMaybe._unCallableFunctions:
      return False
    # if isinstance(instance, Callable)
    if isinstance(instance, Callable):
      return True
    callableFlag = getattr(instance, '__isCallable__', None)
    if callableFlag is not None:
      if not callableFlag:
        return False
      return True
    if isinstance(instance, (int, float, str, complex)):
      return False
    if isinstance(instance, (tuple, dict, list, set)):
      return False
    if instance is None:
      return False
    classId = getattr(instance, '__class__', None)
    instanceName = getattr(instance, '__name__', None)
    if instanceName is None:
      return True
    if classId is None:
      e = """Unable to recognize class of instance"""
      raise ValueError(e)
    className = getattr(classId, '__name__', None)
    if className is None:
      e = """Unable to recognize name of instance class"""
      raise ValueError(e)
    if className == 'builtin_function_or_method':
      return True
    if className == 'function':
      return True
    callFunc = getattr(instance, '__call__', None)
    if callFunc is None:
      return False
    if callFunc is not None:
      return True

  @classmethod
  def registerUnCallable(cls, other: type) -> NoReturn:
    """Registers other type as being explicitly not callable"""
    cls._unCallables.append(other)

  @classmethod
  def registerCallable(cls, other: type) -> NoReturn:
    """Registers other type as being explicitly callable"""
    cls._callables.append(other)

  @classmethod
  def registerUnCallableFunction(cls, other: Callable) -> NoReturn:
    """Registers other function as unCallable"""
    cls._unCallableFunctions.append(other)

  @classmethod
  def registerCallableFunction(cls, *_) -> Never:
    """LOL"""
    msg = """Do not use this method 'registerCallableFunction' as any 
    function this method would accept is already callable. In a future 
    update this will raise an error."""
    warn(PendingDeprecationWarning(warn(msg)))

  def __init__(self, *args, **kwargs) -> None:
    callableKwarg = searchKeys('callable', 'callMeMaybe') @ bool >> kwargs
    callableArg = maybeType(str, *args)
    if callableArg is not None:
      if callableArg == 'callable':
        callableArg = True
      elif callableArg in ['Not-callable', 'not callable']:
        callableArg = False
    callableDefault = True
    self._callableFlag = maybe(callableKwarg, callableArg, callableDefault)

  def __call__(self, other: Callable | type) -> Any:
    """Use as a function decorator. By default, the decorated function are
    regarded as callable. Change this by setting keyword argument
    'callable' to False so that a decorated function will not be regarded
    as a callable. """
    isCallable = isinstance(other, Callable)
    isType = isinstance(other, type)
    if isType:
      return maybe(self._handleType(other), other)
    if isCallable:
      return maybe(self._handleCallable(other), other)
    msg = """CallMeMaybe should decorate classes or functions, not %s"""
    raise TypeError(monoSpace(msg % type(other)))

  def _handleCallable(self, func: Callable) -> NoReturn:
    """Handles the callables."""
    if self._callableFlag is not None:
      if self._callableFlag:
        return self.registerCallableFunction(func)
      return self.registerUnCallableFunction(func)
    return self.registerUnCallableFunction(func)

  def _handleType(self, type_: type) -> NoReturn:
    """Handles types"""
    if self._callableFlag is not None:
      if self._callableFlag:
        return self.registerCallable(type_)
      return self.registerUnCallable(type_)
    return self.registerUnCallable(type_)

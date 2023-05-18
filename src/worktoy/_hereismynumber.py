"""Documentation: HereIsMyNumber
A decorator class for wrapping a callable object.

  Args:
    callMeMaybe: The callable object to be wrapped.

  Attributes:
    _callMeMaybe: The wrapped callable object.
    _callableKeys: List of keys representing members of the callable object.
    _callableData: Dictionary of members of the callable object.
    _decoratorKeys: List of keys representing data in the decorator.
    _decoratorData: Dictionary of data in the decorator."""
#  MIT License
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import inspect
from typing import Any

from worktoy import searchKeys, maybeType, maybe


class HereIsMyNumber:
  """A decorator class for wrapping a callable object.

  Args:
    callMeMaybe: The callable object to be wrapped.

  Attributes:
    _callMeMaybe: The wrapped callable object.
    #  MIT License
    #  Copyright (c) 2023 Asger Jon Vistisen"""

  _AllCallers = []

  def __new__(cls, *args, **kwargs) -> HereIsMyNumber:
    """Adds instance to _AllCallers"""
    out = super().__new__(cls)
    HereIsMyNumber._AllCallers.append(out)
    return out

  def __init__(self, *args, **kwargs) -> None:
    callMeKeys = ['callable', 'callMeMaybe']
    doNotCallKeys = ['noCall', 'secret']
    callableFlagKwarg = searchKeys(*callMeKeys) @ bool >> kwargs
    callableFlagKwargInv = searchKeys(*doNotCallKeys) @ bool >> kwargs
    if callableFlagKwargInv is not None:
      callableFlagKwargInv = False if callableFlagKwargInv else True
    callableFlagArg = maybeType(bool, *args)
    callableFlagDefault = True
    self.__isCallable__ = maybe(callableFlagKwarg, callableFlagKwargInv,
                                callableFlagArg, callableFlagDefault)
    self._callMeMaybe = None

  def __call__(self, *args, **kwargs) -> Any:
    """If callable is None, set argument equal to callable. Else, invoke
    callable on given arguments"""
    if self._callMeMaybe is None:
      self._callMeMaybe = args[0]
      for (key, val) in inspect.getmembers_static(self._callMeMaybe):
        try:
          setattr(self, key, val)
        except TypeError:
          pass
      self.__annotations__ = self._callMeMaybe.__annotations__
      return self
    return self._callMeMaybe(*args, **kwargs)

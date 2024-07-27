"""BaseNamespace provides the namespace object class for the
BaseMetaclass."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Callable

from worktoy.meta import AbstractNamespace, Dispatcher
from worktoy.parse import maybe
from worktoy.text import typeMsg, monoSpace

Overloaded = dict[tuple[type, ...], Callable]


class BaseNamespace(AbstractNamespace):
  """BaseNamespace provides the namespace object class for the
  BaseMetaclass."""

  __overloaded_functions__ = None

  def _getOverloadedFunctions(self) -> dict[str, Overloaded]:
    """Get the overloaded functions."""
    return maybe(self.__overloaded_functions__, {})

  def _setOverloadedFunctions(self, data: dict[str, Overloaded]) -> None:
    """Set the overloaded functions."""
    self.__overloaded_functions__ = data

  def _appendOverload(self, *args) -> None:
    """Append an overloaded function."""
    key, callMeMaybe, typeSig = [*args, None, None, None][:3]
    if key is None:
      e = """Unable to recognize key, function or type signature!"""
      raise ValueError(e)
    if not isinstance(key, str):
      e = typeMsg('key', key, str)
      raise TypeError(e)
    if callMeMaybe is None:
      e = """Unable to recognize function or type signature!"""
      raise ValueError(e)
    if not callable(callMeMaybe):
      e = typeMsg('callMeMaybe', callMeMaybe, Callable)
      raise TypeError(e)
    if typeSig is None:
      e = """Unable to recognize type signature!"""
      raise ValueError(e)
    self._validateTypeSignature(typeSig)
    allOverloads = self._getOverloadedFunctions()
    existing = allOverloads.get(key, {})
    if typeSig in existing:
      e = """Received duplicate signature '%s' for overloaded function!"""
      raise KeyError(monoSpace(e % typeSig))
    existing[typeSig] = callMeMaybe
    allOverloads[key] = existing
    self._setOverloadedFunctions(allOverloads)

  @classmethod
  def _validateTypeSignature(cls, *args) -> None:
    """This method validates the type signature. This method raises a type
    error if the type signature received fails to validate."""
    if len(args) == 1:
      if isinstance(args[0], (list, tuple)):
        return cls._validateTypeSignature(*args[0])
    for arg in args:
      if not isinstance(arg, type):
        e = typeMsg('arg', arg, type)
        raise TypeError(e)

  def __setitem__(self, key: str, value: object) -> None:
    """Set an item in the namespace."""
    if getattr(value, '__overloaded_signature__', None) is not None:
      typeSig = getattr(value, '__overloaded_signature__', )
      return self._appendOverload(key, value, typeSig)
    return AbstractNamespace.__setitem__(self, key, value)

  @staticmethod
  def _validateOverload(overloaded: Overloaded, key: str) -> type:
    """Validate the overloaded functions."""
    functionType = None
    for (typeSig, callMeMaybe) in overloaded.items():
      if functionType is None:
        functionType = type(callMeMaybe)
        continue
      if type(callMeMaybe) is not functionType:
        e = """Found overloaded functions at name: '%s' belonging to 
        different function types! All functions overloaded to the same 
        name must be of the same function type, either 'staticmethod', 
        'classmethod' or 'function'!"""
        raise TypeError(monoSpace(e % key))
    return functionType

  def compile(self) -> dict[str, object]:
    """Compile the namespace into a dictionary."""
    out = AbstractNamespace.compile(self, )
    for (key, overloaded) in self._getOverloadedFunctions().items():
      functionType = self._validateOverload(overloaded, key)
      dispatcher = Dispatcher(overloaded)
      if functionType is staticmethod:
        out[key] = dispatcher.staticFactory()
      else:
        out[key] = dispatcher.functionFactory()
    return out

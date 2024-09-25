"""BaseNamespace provides the namespace object class for the
BaseMetaclass."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.meta import Overload

try:
  from typing import Callable, Any
except ImportError:
  Callable = object
  Any = object

from worktoy.meta import AbstractNamespace
from worktoy.parse import maybe
from worktoy.text import typeMsg, monoSpace

try:
  Overloaded = dict[tuple[type, ...], Callable]
except TypeError:
  Overloaded = dict


class OverloadEntry:
  """Instances of this class are used to store the overloads in the
  BaseNamespace."""

  __func_name__ = None
  __call_me_maybe__ = None
  __raw_types__ = None
  __assigned_key__ = None
  __nested_instances__ = None

  def __init__(self, *types) -> None:
    self.__raw_types__ = (*types,)

  def getNested(self) -> Any:
    """Getter-function for nested instances."""
    return maybe(self.__nested_instances__, [])

  def __call__(self, callMeMaybe: Any) -> Callable:
    existing = getattr(callMeMaybe, '__type_signatures__', [])
    self.__call_me_maybe__ = callMeMaybe
    self.__func_name__ = callMeMaybe.__name__
    setattr(callMeMaybe, '__type_signatures__', [*existing, self])
    return callMeMaybe

  def __str__(self, ) -> str:
    """String representation"""
    typeNames = [t.__name__ for t in self.__raw_types__]
    return """%s: %s""" % (self.__func_name__, typeNames)


def overload(*types) -> OverloadEntry:
  """Decorator function for overloading functions."""
  return OverloadEntry(*types)


class BaseNamespace(AbstractNamespace):
  """BaseNamespace provides the namespace object class for the
  BaseMetaclass."""

  __overload_dict__ = None

  def __init__(self, *args, **kwargs) -> None:
    """Initialize the BaseNamespace."""
    AbstractNamespace.__init__(self, *args, **kwargs)

  def __setitem__(self, key: str, value: object) -> None:
    """Set the item in the namespace."""
    overloadEntries = getattr(value, '__type_signatures__', None)
    if overloadEntries is None:
      return AbstractNamespace.__setitem__(self, key, value)
    existing = self.getOverloadList()
    for entry in overloadEntries:
      entry.__assigned_key__ = key
    self.__overload_dict__ = [*existing, *overloadEntries]

  def getOverloadList(self) -> list:
    """Getter-function for overloads"""
    return maybe(self.__overload_dict__, [])

  def compile(self) -> dict:
    """Compile the namespace into a dictionary."""
    out = {}
    for entry in self.getOverloadList():
      name = entry.__func_name__
      key = entry.__assigned_key__
      sig = entry.__raw_types__
      func = entry.__call_me_maybe__
      if name != key:
        e = """ERROR IN COMPILE!
        The function name '%s' does not match the assigned key 
        '%s'! END"""
        raise ValueError(monoSpace(e % (name, key)))
      overloadField = out.get(name, Overload())
      overloadField.overload(*sig)(func)

      out[name] = overloadField

    return {**AbstractNamespace.compile(self), **out}

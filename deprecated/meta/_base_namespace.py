"""BaseNamespace provides the namespace object class for the
BaseMetaclass."""
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

try:
  from typing import Callable, Any, TYPE_CHECKING
except ImportError:
  Callable = object
  Any = object
  TYPE_CHECKING = False

from depr.meta import AbstractNamespace
from worktoy.static import maybe
from worktoy.text import monoSpace, typeMsg

if TYPE_CHECKING:
  Overloaded = dict[tuple[type, ...], Callable]
  Types = tuple[type, ...]
else:
  Overloaded = object
  Types = object


class OverloadEntry:
  """Instances of this class are used to store the overloads in the
  BaseNamespace."""

  __func_name__ = None
  __call_me_maybe__ = None
  __raw_types__ = None
  __assigned_key__ = None
  __this_zeroton__ = None
  __type_zeroton__ = None

  def __init__(self, *types) -> None:
    self.__raw_types__ = (*types,)

  def getRawTypes(self) -> Types:
    """Getter-function for the raw types"""
    return self.__raw_types__

  def __call__(self, callMeMaybe: Any) -> Callable:
    self.__call_me_maybe__ = callMeMaybe
    self.__func_name__ = callMeMaybe.__name__
    existing = getattr(callMeMaybe, '__type_signatures__', [])
    updated = [*existing, self]
    setattr(callMeMaybe, '__type_signatures__', updated)
    return callMeMaybe

  def assignKey(self, key: str) -> None:
    """Assign the key to the entry."""
    self.__assigned_key__ = key

  def getKey(self, ) -> str:
    """Getter-function for the assigned key."""
    if self.__assigned_key__ is None:
      e = """The key for the overload entry is not assigned!"""
      raise ValueError(monoSpace(e))
    if isinstance(self.__assigned_key__, str):
      return self.__assigned_key__
    e = typeMsg('__assigned_key__', self.__assigned_key__, str, )
    raise TypeError(e)

  def __str__(self, ) -> str:
    """String representation"""
    typeNames = [t.__name__ for t in self.__raw_types__]
    return """%s: %s""" % (self.__func_name__, typeNames)


class BaseNamespace(AbstractNamespace):
  """BaseNamespace provides the namespace object class for the
  BaseMetaclass."""

  __overload_entries__ = None

  def getOverloadEntries(self) -> list[OverloadEntry]:
    """Getter-function for overload entries."""
    return maybe(self.__overload_entries__, [])

  def getOverloadKeys(self) -> list[str]:
    """Getter-function for overload keys."""
    out = []
    for entry in self.getOverloadEntries():
      key = entry.getKey()
      if key not in out:
        out.append(key)
    return out

  def addOverloadEntry(self, entry: OverloadEntry) -> None:
    """Add an overload entry to the namespace."""
    existing = self.getOverloadEntries()
    self.__overload_entries__ = [*existing, entry]

  def getOverload(self, key: str) -> list[OverloadEntry]:
    """Getter-function for an overload entry."""
    out = []
    for entry in self.getOverloadEntries():
      if entry.getKey() == key:
        out.append(entry)
    return out

  def __init__(self, *args, **kwargs) -> None:
    """Initialize the BaseNamespace."""
    AbstractNamespace.__init__(self, *args, **kwargs)

  def __setitem__(self, key: str, value: object) -> None:
    """Set the item in the namespace."""
    if isinstance(value, OverloadEntry):
      value.assignKey(key)
      return self.addOverloadEntry(value)
    if key in self.getOverloadKeys():
      e = """The key '%s' is already assigned to an overload entry!"""
      raise ValueError(monoSpace(e % key))
    return AbstractNamespace.__setitem__(self, key, value)

  def compile(self) -> dict:
    """Compile the namespace into a dictionary."""
    out = {'__overload_entries__': self.getOverloadEntries()}
    return {**AbstractNamespace.compile(self), **out}

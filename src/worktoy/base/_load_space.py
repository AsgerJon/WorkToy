"""EZSpace provides the namespace object class for the EZData class."""
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.abstract import Abstract
from worktoy.static import maybe, OverloadEntry, Dispatch
from worktoy.mcls import AbstractNamespace
from worktoy.text import typeMsg

try:
  from typing import TYPE_CHECKING
except ImportError:
  TYPE_CHECKING = False

try:
  from typing import Callable
except ImportError:
  Callable = object

if TYPE_CHECKING:
  FuncDict = dict[str, Callable]
  Keys = list[str]
else:
  FuncDict = object
  Keys = object
  CallMeMaybe = object


class LoadSpace(AbstractNamespace):
  """EZSpace provides the namespace object class for the EZData class."""

  __overload_entries__ = None
  __field_attributes__ = None
  __abstract_methods__ = None

  def _getBaseAbstractMethods(self) -> FuncDict:
    """Getter-function for the abstract methods defined on the base
    classes. """
    out = {}
    bases = self.getBaseClasses()
    for base in bases:
      methods = getattr(base, '__abstract_methods__', None)
      if methods is None:
        continue
      out = {**out, **methods}
    return out

  def _getAbstractMethods(self) -> FuncDict:
    """Getter-function for the abstract methods."""
    baseAbstractMethods = self._getBaseAbstractMethods()
    out = {**self._getCurrentAbstractMethods(), }
    for (key, abstractMethod) in baseAbstractMethods.items():
      if key in self:
        continue
      out[key] = abstractMethod
    return out

  def _getCurrentAbstractMethods(self) -> FuncDict:
    """Getter-function for the abstract methods defined on the current
    class. """
    out = maybe(self.__abstract_methods__, {})
    if TYPE_CHECKING:
      assert isinstance(out, dict)
    if isinstance(out, dict):
      for (key, val) in out.items():
        if not isinstance(key, str):
          e = typeMsg('key', key, str)
          raise TypeError(e)
        if not callable(val):
          e = typeMsg('val', val, Callable)
          raise TypeError(e)
      return out

  def _addAbstractMethod(self, key: str, abstract: Abstract) -> None:
    """Adds an abstract method to those defined on the class. """
    existing = self._getCurrentAbstractMethods()
    if key in existing:
      e = """The abstract method '%s' is already defined!"""
      raise AttributeError(e % key)
    self.__abstract_methods__ = {**existing, key: abstract}

  def _getOverloadEntries(self) -> dict:
    """Getter-function for the overloaded entries."""
    out = {}
    bases = self.getBaseClasses()
    for base in [*bases, self]:
      entries = maybe(getattr(base, '__overload_entries__', None), {})
      for (key, val) in entries.items():
        existing = out.get(key, [])
        out[key] = [*existing, *val]
    return out

  def _appendOverloadEntry(self, key: str, entry: OverloadEntry) -> None:
    """Appends an overload entry to the namespace."""
    if entry:
      entries = self._getOverloadEntries()
      existing = entries.get(key, [])
      self.__overload_entries__ = {**entries, key: [*existing, entry]}
    else:
      e = """Received an empty overload entry!"""
      raise AttributeError(e)

  def __setitem__(self, key: str, value: object) -> None:
    """This method sets the key, value pair in the namespace."""
    if isinstance(value, Abstract):
      return self._addAbstractMethod(key, value)
    if isinstance(value, OverloadEntry):
      return self._appendOverloadEntry(key, value)
    return AbstractNamespace.__setitem__(self, key, value)

  def _buildDispatchers(self, ) -> dict:
    """Build the dispatchers for the overloaded functions."""
    overloadEntries = self._getOverloadEntries()
    dispatchers = {}
    for (name, entries) in overloadEntries.items():
      dispatchers[name] = Dispatch(*entries)
    return dispatchers

  def compile(self, ) -> dict:
    """Compile the namespace."""
    out = AbstractNamespace.compile(self)
    out['__overload_entries__'] = self._getOverloadEntries()
    abstractMethods = self._getAbstractMethods()
    out['__abstract_methods__'] = abstractMethods
    dispatchers = self._buildDispatchers()
    return {**out, **dispatchers}

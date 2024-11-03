"""OverloadSpace provides the namespace object used to create classes that
support function overloading. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.meta import AbstractNamespace, Dispatcher, Overload
from worktoy.parse import maybe

try:
  from typing import TYPE_CHECKING
except ImportError:
  TYPE_CHECKING = False

if TYPE_CHECKING:
  DispatchDict = dict[str, Dispatcher]
else:
  DispatchDict = object


class OverloadSpace(AbstractNamespace):
  """OverloadSpace provides the namespace object used to create classes that
  support function overloading. """

  __overloaded_entries__ = None

  def _getOverloadEntries(self) -> dict:
    """Getter-function for the overloaded entries."""
    return maybe(self.__overloaded_entries__, {})

  def appendOverloadEntry(self, key: str, entry: Overload) -> None:
    """Appends an overload entry to the namespace."""
    entries = self._getOverloadEntries()
    existing = entries.get(key, [])
    self.__overloaded_entries__ = {**entries, key: [*existing, entry]}

  def _dispatchFactory(self, ) -> DispatchDict:
    """Build the dispatchers for the overloaded functions."""
    mcls = self.getMetaClass()
    entries = self._getOverloadEntries()
    dispatchers = {}
    bases = self.getBaseClasses()
    dispatcher = None
    for key, overloads in entries.items():
      #  Find dispatcher from base class or create new
      for base in bases:
        dispatcher = getattr(base, key, None)
        if not isinstance(dispatcher, Dispatcher):
          continue
        baseName = base.__name__
        print("""Reusing dispatcher from base class in %s!""" % baseName)
        break
      else:
        dispatcher = Dispatcher(mcls, key)
      #  Populate the dispatcher
      for entry in overloads:
        dispatcher.addOverload(entry)
      dispatchers[key] = dispatcher

    return dispatchers

  def compile(self, ) -> dict:
    """Compile the namespace into a dictionary."""
    base = AbstractNamespace.compile(self)
    dispatchers = self._dispatchFactory()
    return {**base, **dispatchers}

  def __setitem__(self, key: str, value: object) -> None:
    """Removes instances of OverloadEntry from the default namespace
    handling."""
    clsName = self.getClassName()
    if isinstance(value, Overload):
      return self.appendOverloadEntry(key, value)
    return AbstractNamespace.__setitem__(self, key, value)

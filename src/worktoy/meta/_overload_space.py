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
    return {**base, **dispatchers, '__class_body_lines__': self.getLines()}

  def __setitem__(self, key: str, value: object) -> None:
    """Removes instances of OverloadEntry from the default namespace
    handling."""
    if isinstance(value, Overload):
      return self.appendOverloadEntry(key, value)
    if isinstance(value, classmethod):
      e = """Present version does not support """
      return self.__setitem__(key, value.__func__)

    return AbstractNamespace.__setitem__(self, key, value)

  def __getitem__(self, key: str, ) -> object:
    """This reimplementation handles the item retrieval case of
    classmethod. """
    if key == 'classmethod':
      return AbstractNamespace.__getitem__(self, 'derp')
    return AbstractNamespace.__getitem__(self, key)

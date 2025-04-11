"""The Dispatcher class maps type signatures to callables. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.text import typeMsg, monoSpace
from worktoy.castOLD import TypeSig, OverloadEntry, maybe, THIS
from worktoy.waitaminute import DispatchException, CastMismatch

try:
  from typing import Any, Callable
except ImportError:
  Any = object
  Callable = object

try:
  from typing import TYPE_CHECKING
except ImportError:
  TYPE_CHECKING = False

if TYPE_CHECKING:
  TypeSigs = list[TypeSig]
  SigFuncMap = dict[TypeSig, Callable]
  DefEntries = list[OverloadEntry]
  Map = dict[TypeSig, Callable]
else:
  TypeSigs = object
  SigFuncMap = object
  DefEntries = object
  Map = object

if TYPE_CHECKING:
  from worktoy.mcls import CallMeMaybe


class Dispatch:
  """The Dispatcher class maps type signatures to callables. """

  __overload_map__ = None
  __fallback_func__ = None
  __deferred_entries__ = None
  __field_name__ = None
  __field_owner__ = None

  __is_finalized__ = None

  def __init__(self, *entries, ) -> None:
    for entry in entries:
      self._deferEntry(entry)

  def isFinalized(self, ) -> bool:
    """Return True if the dispatcher has been finalized. """
    return False if self.__is_finalized__ is None else True

  def finalize(self) -> None:
    """Finalize the dispatcher. """
    self.__is_finalized__ = True

  def _getDeferredEntries(self, ) -> DefEntries:
    """Get the deferred entries. """
    entries = maybe(self.__deferred_entries__, [])
    if isinstance(entries, list):
      for entry in entries:
        if not isinstance(entry, OverloadEntry):
          e = typeMsg('entry', entry, OverloadEntry)
          raise TypeError(monoSpace(e))
      return entries
    e = typeMsg('deferred_entries', entries, list)
    raise TypeError(monoSpace(e))

  def _deferEntry(self, entry: OverloadEntry) -> None:
    """Defer the given entry. """
    if not isinstance(entry, OverloadEntry):
      e = typeMsg('entry', entry, OverloadEntry)
      raise TypeError(e)
    entries = self._getDeferredEntries()
    self.__deferred_entries__ = [*entries, entry]

  def __set_name__(self, owner: type, name: str) -> None:
    """Set the name of the function. """
    print("""__set_name__(%s, %s)""" % (owner.__name__, name))
    self.__field_name__ = name
    self.__field_owner__ = owner
    print("""Starting _buildMap()""")
    try:
      self._buildMap()
    finally:
      print("""_buildMap() finished\n%s""" % ('-' * 80))

  def _getFieldName(self, ) -> str:
    """Getter-function for field name"""
    if self.__field_name__ is None:
      e = """The field name has not been set!"""
      raise AttributeError(monoSpace(e))
    if isinstance(self.__field_name__, str):
      return self.__field_name__
    e = typeMsg('field_name', self.__field_name__, str)
    raise TypeError(monoSpace(e))

  def _getFieldOwner(self, ) -> type:
    """Getter-function for field owner. """
    if self.__field_owner__ is None:
      e = """The field owner has not been set!"""
      raise AttributeError(monoSpace(e))
    if isinstance(self.__field_owner__, type):
      return self.__field_owner__
    e = typeMsg('field_owner', self.__field_owner__, type)
    raise TypeError(monoSpace(e))

  def _getMappings(self, ) -> Map:
    """Return the mappings. """
    mappings = maybe(self.__overload_map__, {})
    if isinstance(mappings, dict):
      for sig, call in mappings.items():
        if not isinstance(sig, TypeSig):
          e = typeMsg('sig', sig, TypeSig)
          raise TypeError(monoSpace(e))
        if not callable(call):
          from worktoy.mcls import CallMeMaybe
          e = typeMsg('call', call, CallMeMaybe)
          raise TypeError(monoSpace(e))
      return mappings
    e = typeMsg('overload_map', mappings, dict)
    raise TypeError(monoSpace(e))

  def _addMapping(self, sig: TypeSig, call: CallMeMaybe) -> None:
    """Add a mapping to the dispatcher. """
    if self.isFinalized():
      e = """The dispatcher has already been finalized!"""
      raise AttributeError(monoSpace(e))
    mappings = self._getMappings()
    self.__overload_map__ = dict()
    for key, val in mappings.items():
      if key == sig:
        e = """The signature '%s' is already in use!""" % sig
        raise AttributeError(monoSpace(e))
      self.__overload_map__[key] = val

  def _setFallback(self, callMeMaybe: CallMeMaybe) -> None:
    """Set the fallback function. """
    if self.__fallback_func__ is not None:
      e = """The fallback function has already been set!"""
      raise AttributeError(monoSpace(e))
    if not callable(callMeMaybe):
      from worktoy.mcls import CallMeMaybe
      e = typeMsg('fallback_func', callMeMaybe, CallMeMaybe)
      raise TypeError(monoSpace(e))
    self.__fallback_func__ = callMeMaybe

  def _getFallback(self, ) -> CallMeMaybe:
    """Getter-function for the fallback function. """
    if self.__fallback_func__ is None:
      e = """The fallback function has not been set!"""
      raise AttributeError(monoSpace(e))
    if callable(self.__fallback_func__):
      return self.__fallback_func__
    from worktoy.mcls import CallMeMaybe
    e = typeMsg('fallback_func', self.__fallback_func__, CallMeMaybe)
    raise TypeError(monoSpace(e))

  def _hasFallback(self, ) -> bool:
    """Return True if the fallback function has been set. """
    return False if self.__fallback_func__ is None else True

  def _buildMap(self, ) -> None:
    """This method is responsible for building the map from signatures to
    callables. It should be deferred until the owning class has been
    created and announced to the __set_name__ method. """
    ownerName = self._getFieldOwner().__name__
    fieldName = self._getFieldName()
    info = """%s.%s _buildMap()"""
    cls = self._getFieldOwner()
    entries = self._getDeferredEntries()
    print(info % (ownerName, fieldName))
    print("""Deferred entries: """)
    for entry in entries:
      print(entry)
      if not isinstance(entry, OverloadEntry):
        e = typeMsg('entry', entry, OverloadEntry)
        raise TypeError(monoSpace(e))
      if entry.isFallback():
        call = entry.getFunc()
        self._setFallback(call)
        continue
      rawTypes = []
      defTypes = entry.getDeferredTypes()
      if not isinstance(defTypes, list):
        e = typeMsg('deferred_types', defTypes, list)
        raise TypeError(monoSpace(e))
      for type_ in defTypes:
        if type_ is THIS:
          rawTypes.append(cls)
        elif isinstance(type_, type):
          rawTypes.append(type_)
        else:
          e = typeMsg('type', type_, type)
          raise TypeError(monoSpace(e))
      sig = TypeSig(*rawTypes)
      call = entry.getFunc()
      self._addMapping(sig, call)
    else:
      print("""NORMAL END""")
      return self.finalize()

  def hereIsMyNumber(self, instance: object) -> CallMeMaybe:
    """Return the dispatcher. """
    if not self.isFinalized():
      e = """The dispatcher has not been finalized!"""
      raise AttributeError(monoSpace(e))
    mappings = self._getMappings()
    info = """%s.%s hereIsMyNumber()"""
    ownerName = self._getFieldOwner().__name__
    fieldName = self._getFieldName()
    print(info % (ownerName, fieldName))
    for key, val in mappings.items():
      print(key, val)
    print("""END of hereIsMyNumber""")

    if instance is None:
      def callMeMaybe(this, *args, **kwargs) -> Any:
        castArg = ()
        """Call the dispatcher. """
        for (sig, call) in mappings.items():
          if not isinstance(sig, TypeSig):
            raise TypeError(typeMsg('sig', sig, TypeSig))
          try:
            castArg = sig.fastCast(*args)
          except CastMismatch:
            continue
          if isinstance(castArg, (tuple, list)):
            return call(this, *castArg, **kwargs)
          raise TypeError(typeMsg('castArg', castArg, tuple))

        for (sig, call) in mappings.items():
          try:
            castArg = sig.flexCast(*args)
          except CastMismatch:
            continue
          if isinstance(castArg, (tuple, list)):
            return call(this, *castArg, **kwargs)
          raise TypeError(typeMsg('castArg', castArg, tuple))
        if self._hasFallback():
          fallbackFunc = self._getFallback()
          if callable(fallbackFunc):
            return fallbackFunc(this, *args, **kwargs)
        raise DispatchException(self, *args)

      if TYPE_CHECKING:
        assert isinstance(callMeMaybe, Callable)
      return callMeMaybe

    thisIsCrazy = self.hereIsMyNumber(None)

    def callMeMaybe(*args, **kwargs) -> Any:
      """Call the dispatcher. """
      return thisIsCrazy(instance, *args, **kwargs)

    if TYPE_CHECKING:
      assert isinstance(callMeMaybe, Callable)
    return callMeMaybe

  def __get__(self, instance: object, owner: type) -> Any:
    """Return the dispatcher. """
    if instance is None:
      return self
    return self.hereIsMyNumber(instance)

  def __str__(self, ) -> str:
    """Return the dispatcher as a string. """
    info = """%s.%s overloaded function:"""
    owner = self._getFieldOwner()
    fieldName = self._getFieldName()
    if owner is None:
      return object.__str__(self)
    return info % (owner.__name__, fieldName)

  def __repr__(self, ) -> str:
    """Return the dispatcher as a string. """
    return self.__str__()

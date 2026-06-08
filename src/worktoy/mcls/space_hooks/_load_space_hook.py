"""
LoadSpaceHook assembles the overload 'Dispatcher' objects for a class.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...dispatch import overload, Dispatcher
from . import AbstractSpaceHook

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class LoadSpaceHook(AbstractSpaceHook):
  """
  LoadSpaceHook collects the 'overload' instances declared in the class
  body. During 'setItemPhase' it records each overload's signatures,
  variadics, fallback, and finalizer on the namespace; during
  'postCompilePhase' it assembles one 'Dispatcher' per overloaded name
  and writes it into the compiled namespace.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PARENT METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def setItemPhase(self, key: str, val: Any, old: Any = None, ) -> bool:
    if not isinstance(val, overload):
      return False
    if val.isFallback():
      self.space.addFallback(key, val.getFallback())
      return True
    if val.isFinalizer():
      self.space.addFinalizer(key, val.getFinalizer())
      return True
    for sig, func in val:
      self.space.addOverload(key, sig, func)
    for sig, func in val.getVariadics():
      self.space.addVariadic(key, sig, func)
    return True

  def postCompilePhase(self, compiledSpace) -> dict:
    """Assembles one 'Dispatcher' per overloaded name from the collected
    'overload' registrations (concrete signatures, variadics, fallback,
    and finalizer) and writes each into 'compiledSpace'.

    A name that the class body bound to a plain (non-'overload')
    definition is left untouched: that explicit definition overrides any
    overloads inherited from a base class. The inherited registrations
    for such a name are dropped, so neither this class nor a subclass
    rebuilds a 'Dispatcher' over the override. The signal is the
    namespace's own storage: '@overload' declarations are claimed by
    'setItemPhase' and never reach it, whereas a plain definition is
    stored there under its name.
    """
    overloadMap = self.space.getOverloads()
    variadicMap = self.space.getVariadics()
    fallbackMap = self.space.getFallbacks()
    finalizerMap = self.space.getFinalizers()
    names = set(overloadMap) | set(variadicMap)
    for name in names:
      if dict.__contains__(self.space, name):
        overloadMap.pop(name, None)
        variadicMap.pop(name, None)
        fallbackMap.pop(name, None)
        finalizerMap.pop(name, None)
        continue
      dispatcher = Dispatcher()
      sigFunc = overloadMap.get(name, {})
      for sig, func in sigFunc.items():
        dispatcher.addSigFunc(sig, func)
      for sig, func in variadicMap.get(name, []):
        dispatcher.addVariadicSigFunc(sig, func)
      fallback = fallbackMap.get(name, None)
      if fallback is not None:
        dispatcher.setFallbackFunction(fallback)
      finalizer = finalizerMap.get(name, None)
      if finalizer is not None:
        dispatcher.setFinalizerFunction(finalizer)
      compiledSpace[name] = dispatcher
    return compiledSpace

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
    and finalizer) and writes each into 'compiledSpace'."""
    variadicMap = self.space.getVariadics()
    names = set(self.space.getOverloads()) | set(variadicMap)
    for name in names:
      dispatcher = Dispatcher()
      sigFunc = self.space.getOverloads().get(name, {})
      for sig, func in sigFunc.items():
        dispatcher.addSigFunc(sig, func)
      for sig, func in variadicMap.get(name, []):
        dispatcher.addVariadicSigFunc(sig, func)
      fallback = self.space.getFallbacks().get(name, None)
      if fallback is not None:
        dispatcher.setFallbackFunction(fallback)
      finalizer = self.space.getFinalizers().get(name, None)
      if finalizer is not None:
        dispatcher.setFinalizerFunction(finalizer)
      compiledSpace[name] = dispatcher
    return compiledSpace

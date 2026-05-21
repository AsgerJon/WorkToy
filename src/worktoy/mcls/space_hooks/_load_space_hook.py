"""
LoadSpaceHook collects DescLoad instances encountered in the class body
and creates an entry in the namespace.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...dispatch import overload, Dispatcher
from . import AbstractSpaceHook, SpaceDesc

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Type, TypeAlias

  from .. import BaseSpace

  Meta: TypeAlias = Type[type]


class LoadSpaceHook(AbstractSpaceHook):
  """
  LoadSpaceHook collects DescLoad instances encountered in the class body
  and creates an entry in the namespace.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Public Variables
  space: SpaceDesc[BaseSpace] = SpaceDesc()

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
    """Populates the namespace with the collected DescLoad instances. """
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

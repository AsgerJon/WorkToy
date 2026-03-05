"""
LoadSpaceHook collects DescLoad instances encountered in the class body
and creates an entry in the namespace.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...dispatch import overload, Dispatcher
from . import AbstractSpaceHook
from ...utilities import textFmt

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Type, TypeAlias, Union

  from .. import BaseSpace as BSpace
  from . import SpaceDesc

  Meta: TypeAlias = Type[type]


class LoadSpaceHook(AbstractSpaceHook):
  """
  LoadSpaceHook collects DescLoad instances encountered in the class body
  and creates an entry in the namespace.
  """

  space: Union[BSpace, SpaceDesc]

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
    return True

  def postCompilePhase(self, compiledSpace) -> dict:
    """Populates the namespace with the collected DescLoad instances. """
    for name, sigFunc in self.space.getOverloads().items():
      dispatcher = Dispatcher()
      for sig, func in sigFunc.items():
        dispatcher.addSigFunc(sig, func)
      fallback = self.space.getFallbacks().get(name, None)
      if fallback is not None:
        dispatcher.setFallbackFunction(fallback)
      finalizer = self.space.getFinalizers().get(name, None)
      if finalizer is not None:
        dispatcher.setFinalizerFunction(finalizer)
      compiledSpace[name] = dispatcher
    return compiledSpace

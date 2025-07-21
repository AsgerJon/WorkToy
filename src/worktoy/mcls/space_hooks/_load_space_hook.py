"""
LoadSpaceHook collects DescLoad instances encountered in the class body
and creates an entry in the namespace.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.dispatch import Overload, Dispatcher
from worktoy.mcls.space_hooks import AbstractSpaceHook

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Type, TypeAlias

  Meta: TypeAlias = Type[type]


class LoadSpaceHook(AbstractSpaceHook):
  """
  LoadSpaceHook collects DescLoad instances encountered in the class body
  and creates an entry in the namespace.
  """

  def setItemPhase(self, key: str, val: Any, old: Any = None, ) -> bool:
    if not isinstance(val, Overload):
      return False
    sigs = [val.sig]
    while isinstance(val.func, Overload):
      val = val.func
      sigs.append(val.sig)
    for sig in sigs:
      self.space.addOverload(key, sig, val.func)
    return True

  def postCompilePhase(self, compiledSpace) -> dict:
    """Populates the namespace with the collected DescLoad instances. """
    for name, sigFunc in self.space.getOverloads().items():
      dispatcher = Dispatcher()
      for sig, func in sigFunc.items():
        dispatcher.addSigFunc(sig, func)
      compiledSpace[name] = dispatcher
    return compiledSpace

"""
LoadSpaceHook collects DescLoad instances encountered in the class body
and creates an entry in the namespace.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.dispatch import Dispatcher
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
    if not isinstance(val, Dispatcher):
      return False
    sig, func = None, None
    for sig, func in val.__sig_funcs__:
      self.space.addOverload(key, sig, func)
    return True

  def postCompilePhase(self, compiledSpace) -> dict:
    """Populates the namespace with the collected DescLoad instances. """
    for name, sigFunc in self.space.getOverloads().items():
      compiledSpace[name] = Dispatcher(sigFunc)
    return compiledSpace

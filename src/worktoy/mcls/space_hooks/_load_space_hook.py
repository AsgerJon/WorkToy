"""
LoadSpaceHook collects DescLoad instances encountered in the class body
and creates an entry in the namespace.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.mcls.space_hooks import AbstractSpaceHook
from worktoy.static import DescLoad, Dispatch

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Type, TypeAlias

  Meta: TypeAlias = Type[type]


class LoadSpaceHook(AbstractSpaceHook):
  """
  LoadSpaceHook collects DescLoad instances encountered in the class body
  and creates an entry in the namespace.
  """

  def setItemPhase(self, key: str, val: Any, old: Any = None, ) -> bool:
    """
    If key contains reference the class under construction by containing
    'THIS', replace with 'PreClass' object providing the hash and name of
    the future class.
    """
    if not isinstance(val, DescLoad):
      return False
    func = val.func
    name = func.__name__
    for sig in val.sigs:
      self.space.addOverload(name, sig, func)
    return True

  def postCompilePhase(self, compiledSpace) -> dict:
    """Populates the namespace with the collected DescLoad instances. """
    for name, sigFunc in self.space.getOverloads().items():
      compiledSpace[name] = Dispatch(sigFunc)
    return compiledSpace

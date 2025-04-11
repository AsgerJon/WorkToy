"""OverloadSpace provides the namespace class that implements overload
functionality. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.parse import maybe
from worktoy.text import typeMsg, monoSpace

from worktoy.mcls import AbstractNamespace
from worktoy.static import OverloadedFunction as OverFunc, Dispatch

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import TypeAlias, Callable

  Overloads: TypeAlias = dict[str, list[OverFunc]]
  Baseloads: TypeAlias = list[Overloads]


class OverloadSpace(AbstractNamespace):
  """OverloadSpace provides the namespace class that implements overload
  functionality. """

  __overloaded_functions__ = None

  def _getOverFuncs(self, **kwargs) -> Overloads:
    """Getter-function for the overloaded functions."""
    primeSpace = self.getPrimeSpace()
    if TYPE_CHECKING:
      assert isinstance(primeSpace, OverloadSpace)
    return maybe(primeSpace.__overloaded_functions__, {})

  def _addOverFunc(self, key: str, overFunc: OverFunc, *_) -> bool:
    """Add an overloaded function to the overload space."""
    if not isinstance(overFunc, OverFunc):
      return False
    overloads = self._getOverFuncs()
    existing = overloads.get(key, [])
    primeSpace = self.getPrimeSpace()
    if TYPE_CHECKING:
      assert isinstance(primeSpace, OverloadSpace)
    overloads[key] = [*existing, overFunc]
    setattr(primeSpace, '__overloaded_functions__', overloads)
    return True

  @classmethod
  def getSetItemHooks(cls, ) -> list[Callable]:
    """Get the set item hooks."""
    base = AbstractNamespace.getSetItemHooks()
    return [*base, cls._addOverFunc, ]

  def postCompile(self, namespace: dict) -> dict:
    """Post-compile the namespace."""
    for key, overFuncs in self._getOverFuncs().items():
      namespace[key] = Dispatch(*overFuncs)
    return namespace

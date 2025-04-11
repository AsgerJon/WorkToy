"""OverloadHook hooks into the namespace system and collects the overload
decorated methods replacing them with a dispatcher that calls the
correct method based on the arguments passed to it. It is used to
provide a simple way to overload methods in the namespace system."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False
from ...static import OverloadedFunction as OverFunc, Dispatch
from . import AbstractHook

if TYPE_CHECKING:
  from typing import Any, Callable, Self
  from .. import AbstractNamespace as ASpace


class OverloadHook(AbstractHook):
  """OverloadHook hooks into the namespace system and collects the overload
  decorated methods replacing them with a dispatcher that calls the
  correct method based on the arguments passed to it. It is used to
  provide a simple way to overload methods in the namespace system.
  """

  __overloads_name__ = '__overloaded_functions__'

  def _getPrivateName(self) -> str:
    """Get the name of the private attribute."""
    return self.__overloads_name__

  def _getOverFuncs(self) -> dict[str, list[OverFunc]]:
    """Get the overload functions."""
    pvtName = self._getPrivateName()
    instance = self.getOwningNamespace()
    space = instance.getPrimeSpace()
    return getattr(space, pvtName, {})

  def _setOverFuncs(self, overFuncs: dict[str, list[OverFunc]]) -> None:
    """Set the overload functions."""
    pvtName = self._getPrivateName()
    instance = self.getOwningNamespace()
    space = instance.getPrimeSpace()
    setattr(space, pvtName, overFuncs)

  def _addOverFunc(self, key: str, overFunc: OverFunc) -> None:
    """Add the given function to the list of overload functions."""
    overFuncs = self._getOverFuncs()
    existing = overFuncs.get(key, [])
    overFuncs[key] = [*existing, overFunc]
    self._setOverFuncs(overFuncs)

  def setItemHook(self, key: str, value: Any, *_) -> bool:
    """Set the item in the namespace and add it to the overload functions."""
    if not isinstance(value, OverFunc):
      return False
    self._addOverFunc(key, value)
    return True

  def postCompileHook(self, namespace: ASpace, space: dict) -> dict:
    """Post compile hook. This is called after the namespace has been
    compiled. It is used to replace the overload functions with a
    dispatcher that calls the correct function based on the arguments
    passed to it."""
    instance = namespace.getPrimeSpace()
    for (key, overFuncs) in self._getOverFuncs().items():
      space[key] = Dispatch(*overFuncs)
    return space

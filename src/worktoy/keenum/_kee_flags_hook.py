"""
KeeFlagsHook provides a namespace hook for the 'KeeFlagsSpace' class.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..mcls.space_hooks import AbstractSpaceHook
from . import KeeFlag

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any


class KeeFlagsHook(AbstractSpaceHook):
  """
  A flags class body binds its flags as ordinary names, 'READ =
  KeeFlag()', yet the class must hold members, not flags, at those
  names. The flags must therefore reach the namespace's record and
  never its dictionary.

  Implementation
  --------------

  'setItemPhase' hands every 'KeeFlag' to 'addKeeFlag' of the namespace
  and claims the binding; every other binding is left to the namespace.
  A body name colliding with a member name is refused as the class is
  created, since the combined names exist only then.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def setItemPhase(self, key: str, val: Any, old: Any = None, ) -> bool:
    if isinstance(val, KeeFlag):
      self.space.addKeeFlag(key, val)
      return True
    return False

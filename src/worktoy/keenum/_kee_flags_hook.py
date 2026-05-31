"""
KeeFlagsHook provides a namespace hook for the 'KeeFlagsSpace' class.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..mcls.space_hooks import AbstractSpaceHook
from . import KeeFlag

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class KeeFlagsHook(AbstractSpaceHook):
  """
  KeeFlagsHook provides a namespace hook for the 'KeeFlagsSpace' class.

  It intercepts key, KeeFlag pairs and redirects them to the 'addKeeFlag'
  method on the 'KeeFlagsSpace' instance.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def setItemPhase(self, key: str, val: Any, old: Any = None, ) -> bool:
    """
    The 'setItemPhase' method routes each 'KeeFlag' bound in the class
    body to the namespace's 'addKeeFlag', claiming it so the namespace
    does not store it as an ordinary attribute. Anything else is left
    untouched.
    """
    if isinstance(val, KeeFlag):
      self.space.addKeeFlag(key, val)
      return True
    return False

"""
ClaimingHook is a namespace hook that claims some bindings and some
deletions.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.mcls.space_hooks import AbstractSpaceHook

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any


class ClaimingHook(AbstractSpaceHook):
  """
  A hook may take a binding for itself, so the namespace never stores
  it, as 'LoadSpaceHook' takes every 'overload', and it may take a
  deletion the same way. 'ClaimingHook' claims every binding whose
  value is 'bytes', recording the name and value in 'taken', and every
  deletion of a name holding a 'bytearray', recording the name in
  'dropped'. Everything else passes.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  taken: list = []
  dropped: list = []

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PARENT METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def setItemPhase(self, key: str, val: Any, old: Any = None) -> bool:
    if isinstance(val, bytes):
      ClaimingHook.taken.append((key, val))
      return True
    return False

  def delItemPhase(self, key: str, val: Any = None) -> bool:
    if isinstance(val, bytearray):
      ClaimingHook.dropped.append(key)
      return True
    return False

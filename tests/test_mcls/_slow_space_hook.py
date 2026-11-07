"""
SlowSpaceHook is a namespace hook that yields to other threads inside a
phase and records whether its namespace is still the one it was given.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import time
from typing import TYPE_CHECKING

from worktoy.mcls.space_hooks import AbstractSpaceHook

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from worktoy.mcls import AbstractNamespace


class SlowSpaceHook(AbstractSpaceHook):
  """
  A hook bound to a namespace shared between threads shows its fault
  only when another thread binds the hook between the binding and the
  read of 'self.space'. 'preparePhase' is handed the namespace outright,
  so it can tell: it yields the processor, then records whether
  'self.space' is still that namespace. The records go to 'seen', one
  per class statement.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  seen: list = []

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PARENT METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def preparePhase(self, space: AbstractNamespace) -> None:
    time.sleep(0)
    SlowSpaceHook.seen.append(self.space is space)

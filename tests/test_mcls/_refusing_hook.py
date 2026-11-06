"""
RefusingHook is a namespace hook that refuses one class and one read.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.mcls.space_hooks import AbstractSpaceHook

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any

  from worktoy.mcls import AbstractNamespace


class RefusingHook(AbstractSpaceHook):
  """
  A hook may refuse a class before its body runs, and it may refuse a
  read in the body, which the namespace reports as a 'HookException'.
  'RefusingHook' raises 'ValueError' from 'preparePhase' for a class
  named 'Refused' and from 'getItemPhase' for a read of 'forbidden'.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PARENT METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def preparePhase(self, space: AbstractNamespace) -> None:
    if space.getClassName() == 'Refused':
      raise ValueError('refused before the body ran')

  def getItemPhase(self, key: str, value: Any) -> None:
    if key == 'forbidden':
      raise ValueError('forbidden read')

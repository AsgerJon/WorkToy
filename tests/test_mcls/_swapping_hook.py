"""
SwappingHook is a namespace hook that may hand the metaclass another
class than the one it built.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.mcls.space_hooks import AbstractSpaceHook

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any, Optional


class SwappingHook(AbstractSpaceHook):
  """
  The metaclass lets every hook replace the finished class through
  'newClassPhase', keeping the class when a hook returns nothing.
  'SwappingHook' returns 'replacement' for a class named 'Decoy', which
  is 'None' unless a test sets it, and every other class as it is.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  replacement: Optional[type] = None

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PARENT METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def newClassPhase(self, cls: type) -> Any:
    if cls.__name__ == 'Decoy':
      return SwappingHook.replacement
    return cls

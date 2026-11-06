"""
Liar is a descriptor whose 'hasContext' answers 'True' without a frame.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core import Object


class Liar(Object):
  """
  'getContextInstance' and 'getContextOwner' check the stack again after
  'hasContext' answered, so a reimplementation answering 'True' wrongly
  is caught with 'MissingVariable' rather than an 'IndexError' on an
  empty stack. 'Liar' is that reimplementation.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PARENT METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def hasContext(self) -> bool:
    return True

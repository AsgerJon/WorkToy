"""
Till is a worktoy class with one box and one method, for the warnings
to name.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox
from worktoy.mcls import BaseObject


class Till(BaseObject):
  """
  A warning is handed the thing it is about and names it as a user
  would write it. 'Till' is an everyday class to hand over: its 'cash'
  box is named after the class and the field, and its 'recount' method
  by its qualified name.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Public Variables
  cash = AttriBox[int](0)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def recount(self, ) -> int:
    """The 'recount' method gives the cash in the till."""
    return self.cash

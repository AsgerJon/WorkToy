"""
Boxed is a worktoy class holding an 'AttriBox', for the tests of 'THIS'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox
from worktoy.mcls import BaseObject


class Boxed(BaseObject):
  """
  A subclass built by a worktoy metaclass keeps the namespace of its body
  under '__namespace__', which is where 'THIS' looks for a declaration
  that would conflict with a clone. 'Boxed' is the holder for that route,
  a 'BaseObject' with the box 'x'.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Public Variables
  x = AttriBox[int](1)

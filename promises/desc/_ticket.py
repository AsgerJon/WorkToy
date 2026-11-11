"""
The private file '_ticket' holds 'Ticket', a class of boxes defined at
the top of a file, as pickling requires.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox
from worktoy.mcls import BaseObject


class Ticket(BaseObject):
  """
  'Ticket' is a seat at a show, its number and holder in boxes.
  """

  number = AttriBox[int](7)
  holder = AttriBox[str]('nobody')

"""
NarrowClause is a 'Clause' drawing its words from 'Narrow'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox
from worktoy.lorem_ipsum import Clause

from . import Narrow


class NarrowClause(Clause):
  """
  A project brings its own words to a clause by rebinding 'stochWord' to
  a box of its own 'StochasticWord' subclass. 'NarrowClause' takes its
  words from 'Narrow', so its texts hold words of five and six letters
  and some counts cannot be laid out at all.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Public Variables
  stochWord = AttriBox[Narrow]()

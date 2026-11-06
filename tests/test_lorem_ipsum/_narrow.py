"""
Narrow is a 'StochasticWord' with words of two lengths only.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.lorem_ipsum import StochasticWord


class Narrow(StochasticWord):
  """
  A project brings its own words by rebinding the category weights and
  nothing more, and the class statement computes the statistics of the
  new list. 'Narrow' holds words of five and six letters, so a count no
  run of them adds up to is easy to name.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __category_weights__ = (
    (('alpha', 'delta', 'gamma'), 1.0),
    (('zephyr', 'lambda'), 0.5),
  )

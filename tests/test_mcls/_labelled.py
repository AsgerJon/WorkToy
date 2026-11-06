"""
Labelled is a 'Figure' overloading 'scale' on a string as well.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.dispatch import overload

from . import Figure


class Labelled(Figure):
  """
  The overloading branch of the diamond: 'Labelled' adds a string
  signature and keeps the integer one of 'Figure' behind it.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(str)
  def scale(self, s: str) -> tuple:
    return 'labelled-str', s

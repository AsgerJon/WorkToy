"""
Fixed is a 'Figure' defining 'scale' plainly.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from . import Figure


class Fixed(Figure):
  """
  The plain branch of the diamond: 'Fixed' defines 'scale' as an
  ordinary method, which hides the overloads of 'Figure' on its own
  branch and takes no part in the dispatch of a class overloading the
  name.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def scale(self, *args) -> tuple:
    return 'fixed', args

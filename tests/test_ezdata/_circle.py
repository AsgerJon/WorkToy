"""
Circle is the frozen, keyword-only dataclass of the 'EZData' docstring.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.ezdata import EZData, EZField

from . import Point2D


class Circle(EZData, frozen=True, kwOnly=True):
  """
  A frozen class refuses assignment and deletion and hashes by its
  values; a keyword-only class refuses positional arguments and has an
  empty '__match_args__'. 'Circle' holds a 'Point2D' built from no
  arguments and a radius.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Fields
  center = EZField[Point2D]()
  radius = EZField[float](1.0)

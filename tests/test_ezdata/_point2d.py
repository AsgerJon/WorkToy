"""
Point2D is the dataclass of the 'EZData' docstring: two float fields.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.ezdata import EZData, EZField


class Point2D(EZData):
  """
  The plainest dataclass: two fields declared with 'EZField[T](value)',
  positional construction, generated equality, display and
  conversions, and nothing opted in.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Fields
  x = EZField[float](0.0)
  y = EZField[float](0.0)

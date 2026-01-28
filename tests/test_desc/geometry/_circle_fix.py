"""
CircleFix subclasses 'Circle' and replaces the 'AttriBox' descriptors
with 'FixBox' descriptors to create immutable circles.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.desc import FixBox
from . import Circle, Point2DFix

if TYPE_CHECKING:  # pragma: no cover
  pass


class CircleFix(Circle):
  """
  CircleFix subclasses 'Circle' and replaces the 'AttriBox' descriptors
  with 'FixBox' descriptors to create immutable circles.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Public Variables

  center = FixBox[Point2DFix]()
  radius = FixBox[float](1.0)

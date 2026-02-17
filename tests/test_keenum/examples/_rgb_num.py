"""
RGBNum provides a root KeeNum class enumerating colors in the RGB color
space as implemented by the RGB EZData class.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.keenum import KeeNum, Kee
from . import RGB

if TYPE_CHECKING:  # pragma: no cover
  pass


class RootRGB(KeeNum):
  """
  RootRGB provides a root KeeNum class enumerating colors in the RGB color
  space as implemented by the RGB EZData class.
  """

  RED = Kee[RGB](255, 0, 0)
  GREEN = Kee[RGB](0, 255, 0)
  BLUE = Kee[RGB](0, 0, 255)


class MoreRGB(RootRGB):
  """
  MoreRGB provides a KeeNum class enumerating more colors in the RGB color
  space as implemented by the RGB EZData class.
  """

  CYAN = Kee[RGB](0, 255, 255)
  MAGENTA = Kee[RGB](255, 0, 255)
  YELLOW = Kee[RGB](255, 255, 0)


class EvenMoreRGB(MoreRGB):
  """
  EvenMoreRGB provides a KeeNum class enumerating even more colors in the RGB
  color space as implemented by the RGB EZData class.
  """

  ORANGE = Kee[RGB](255, 165, 0)
  AQUA = Kee[RGB](0, 255, 165)
  PURPLE = Kee[RGB](165, 0, 255)
  LIME = Kee[RGB](165, 255, 0)
  AZURE = Kee[RGB](0, 165, 255)
  PINK = Kee[RGB](255, 0, 165)


class RGBNum(EvenMoreRGB):
  """
  RGBNum provides a KeeNum class enumerating colors in the RGB color space as
  implemented by the RGB EZData class.
  """

  WHITE = Kee[RGB](255, 255, 255)
  BLACK = Kee[RGB](0, 0, 0)
  GRAY = Kee[RGB](128, 128, 128)
  SILVER = Kee[RGB](192, 192, 192)

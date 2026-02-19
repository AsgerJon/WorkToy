"""
ColorNum enumerates colors with RGB values.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import RGB
from worktoy.keenum import KeeNum, Kee

if TYPE_CHECKING:  # pragma: no cover
  from typing import Self, Any


class ColorNum(KeeNum):
  """
  ColorNum enumerates colors with RGB values.
  """

  RED = Kee[RGB](255, 0, 0)
  GREEN = Kee[RGB](0, 255, 0)
  BLUE = Kee[RGB](0, 0, 255)

  YELLOW = Kee[RGB](255, 255, 0)
  CYAN = Kee[RGB](0, 255, 255)
  MAGENTA = Kee[RGB](255, 0, 255)

  BLACK = Kee[RGB](0, 0, 0)
  GRAY = Kee[RGB](128, 128, 128)
  WHITE = Kee[RGB](255, 255, 255)

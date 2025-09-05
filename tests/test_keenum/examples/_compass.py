"""
Compass enumerates the points on a compass rose.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.keenum import KeeNum, Kee

if TYPE_CHECKING:  # pragma: no cover
  pass


class Compass(KeeNum):
  """Compass enumeration."""
  NULL = Kee[complex](0 + 0j)  # Falsy because of name being 'NULL'
  ALSO_NULL = Kee[complex](0 + 0j)  # Falsy because of value
  EAST = Kee[complex](1 + 0j)
  NORTH = Kee[complex](0 + 1j)
  WEST = Kee[complex](-1 + 0j)
  SOUTH = Kee[complex](0 - 1j)
  NORTHEAST = Kee[complex](1 + 1j)
  NORTHWEST = Kee[complex](-1 + 1j)
  SOUTHEAST = Kee[complex](1 - 1j)
  SOUTHWEST = Kee[complex](-1 - 1j)

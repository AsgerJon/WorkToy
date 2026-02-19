"""RGB provides an EZData class representation of the RGB color space."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from icecream import ic

from worktoy.ezdata import EZData

if TYPE_CHECKING:  # pragma: no cover
  from typing import Self

ic.configureOutput(includeContext=True)


class RGB(EZData, frozen=True, order=True):
  """RGB provides an EZData class representation of the RGB color space."""

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  r = -1
  g = -1
  b = -1

  def __str__(self) -> str:
    """Returns the hex representation of the RGB color."""
    return f"#{self.r:02x}{self.g:02x}{self.b:02x}".upper()

  def __repr__(self) -> str:
    """Returns what would create this RGB color if passed to 'eval'. """
    infoSpec = """%s(%d, %d, %d)"""
    return infoSpec % (type(self).__name__, self.r, self.g, self.b)

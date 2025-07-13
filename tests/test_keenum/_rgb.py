"""RGB provides an EZData class representation of the RGB color space."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.ezdata import EZData

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Type, TypeAlias


class RGB(EZData, frozen=True, order=True):
  """RGB provides an EZData class representation of the RGB color space."""

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  r = 255
  g = 255
  b = 255

  def __str__(self) -> str:
    """Returns the hex representation of the RGB color."""
    return f"#{self.r:02x}{self.g:02x}{self.b:02x}".upper()

  def __repr__(self) -> str:
    """Returns what would create this RGB color if passed to 'eval'. """
    infoSpec = """%s(%d, %d, %d)"""
    return infoSpec % (type(self).__name__, self.r, self.g, self.b)

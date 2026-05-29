"""RGB provides an EZData class representation of the RGB color space."""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.desc import AttriBox

if TYPE_CHECKING:  # pragma: no cover
  from typing import Iterator, Self


class RGB:
  """RGB provides an EZData class representation of the RGB color space."""

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  r = AttriBox[int](0)
  g = AttriBox[int](0)
  b = AttriBox[int](0)

  def __str__(self) -> str:
    """Returns the hex representation of the RGB color."""
    return f"#{self.r:02x}{self.g:02x}{self.b:02x}".upper()

  def __repr__(self) -> str:
    """Returns what would create this RGB color if passed to 'eval'. """
    infoSpec = """%s(%d, %d, %d)"""
    return infoSpec % (type(self).__name__, self.r, self.g, self.b)

  def __init__(self, *args) -> None:
    keys = ('r', 'g', 'b')
    for key, value in zip(keys, args):
      setattr(self, key, int(value))

  def __eq__(self, other: Self) -> bool:
    """Returns 'True' if the RGB colors are the same."""
    if self.r != other.r:
      return False
    if self.g != other.g:
      return False
    if self.b != other.b:
      return False
    return True

  def __iter__(self, ) -> Iterator[int]:
    """Returns an iterator over the RGB color components."""
    yield self.r
    yield self.g
    yield self.b

  def __hash__(self, ) -> int:
    return hash((*self,))

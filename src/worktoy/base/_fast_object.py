"""FastObject requires all attributes to be instances of AttriBox. This
allows significant performance improvements."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.base import FastMeta


class FastObject(metaclass=FastMeta):
  """FastObject requires all attributes to be instances of AttriBox. This
  allows significant performance improvements."""

  def __init__(self, *args, **kwargs) -> None:
    """LMAO XD!"""

  def __init_subclass__(cls, *args, **kwargs) -> None:
    """LOL this is why we can't have nice things!"""

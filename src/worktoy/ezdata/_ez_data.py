"""FastObject requires all attributes to be instances of AttriBox. This
allows significant performance improvements."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.ezdata import EZMeta

try:
  from typing import TYPE_CHECKING
except ImportError:
  TYPE_CHECKING = False


class EZData(metaclass=EZMeta):
  """FastObject requires all attributes to be instances of AttriBox. This
  allows significant performance improvements."""

  def __init__(self, *args, **kwargs) -> None:
    """This method is overwritten by the namespace object returned by the
    metaclass __prepare__ method.
    $$IGNORE=TRUE$$
    The above line is read by the namespace object which tells it to ignore
    this method."""

  def __init_subclass__(cls, *args, **kwargs) -> None:
    """LOL this is why we can't have nice things!"""

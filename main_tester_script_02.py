"""BLABLA"""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.parse import maybe


class Float:
  """lmao"""

  __inner_value__ = None

  def __init__(self, value: float = None):
    self.__inner_value__ = maybe(value, 0)

  def __float__(self) -> float:
    return self.__inner_value__

"""
TrollSlice tests provides a class that does have an '__index__' attribute,
but not a callable.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from random import randint


class TrollSlice:
  __index__ = """Trolololo!"""
  __who_dat__ = None

  def __init__(self, ) -> None:
    self.__who_dat__ = randint(0, 2 ** 64 - 1)

"""The flexUnPack function allows flexible unpacking"""
#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence
from __future__ import annotations

from typing import Any


class FlexUnPack:
  """The flexUnPack function allows flexible unpacking
  :param *values: Any number of values
  res = FlexUnPack(1, 2, 3)
  a = res
  a
  >>> 1
  a, b = res
  a, b
  >>> 1, 2
  a, b, c = res
  a, b, c
  >>> 1, 2, 3
  #  Copyright (c) 2023 Asger Jon Vistisen
  #  MIT Licence"""

  def __init__(self, *values):
    self.values = values

  def __iter__(self):
    yield from self.values

  def __repr__(self):
    return str(self.values[0]) if len(self.values) == 1 else str(self.values)


class Extracted(FlexUnPack):
  """This subclass is augmented for use with the extractArg function."""

  def __init__(self,
               base: Any = None,
               args: tuple = None,
               kwargs: dict = None
               ) -> None:
    FlexUnPack.__init__(self, *[base, args, kwargs])


class UnParsed(FlexUnPack):
  """Peel of value one at a time."""

  def __init__(self, *args, ) -> None:
    FlexUnPack.__init__(self, *args)

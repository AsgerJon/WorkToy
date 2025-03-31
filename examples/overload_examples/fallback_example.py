"""The 'fallbackExample' function demonstrates how the overloading
protocol can be used to implement a fallback function that is called when
none of the other overloads match the type signature of the arguments
received. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.waitaminute import DispatchException

try:
  from typing import Never
except ImportError:
  try:
    from typing import NoReturn as Never
  except ImportError:
    from typing import Any as Never

from worktoy import EZData, overload
from depr.meta import FallBack, TypeSig


class PlanePoint(EZData):
  """Represents a point in the plane"""

  x = 0
  y = 0

  @overload(int, int)
  def __init__(self, x: int, y: int):
    self.x = x
    self.y = y

  @overload(int)
  def __init__(self, x: int):
    self.x = x
    self.y = 0

  @overload()
  def __init__(self):
    pass

  @overload(FallBack)
  def __init__(self, *args, **kwargs) -> Never:
    e = """Fallback overload function called! Received the following type 
    signature: %s"""
    typeSig = TypeSig(*[type(arg) for arg in args], )
    raise TypeError(e % str(typeSig))


def fallbackExample() -> None:
  """overloadExample demonstrates how to use the 'worktoy.overload'
  module."""
  nicePoint = PlanePoint(69, 420)
  try:
    susPoint = PlanePoint('sixty-nine', 'four-twenty')
  except DispatchException as dispatchException:
    print(dispatchException)

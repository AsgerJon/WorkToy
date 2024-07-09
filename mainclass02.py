"""LMAO"""
#  AGPL-3.0 license
#  Copyright (c) 2023-2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.desc import AttriBox, Instance, Owner
from worktoy.ezdata import EZData


class Volume:
  """LMAO"""

  __inner_value__ = None

  def __init__(self, point: Point2D) -> None:
    """LMAO"""
    if TYPE_CHECKING:
      assert isinstance(point.x, int)
      assert isinstance(point.y, int)
      assert isinstance(point.z, int)
    self.__inner_value__ = point.x ** 2 + point.y ** 2 + point.z ** 2

  def __str__(self) -> str:
    """LMAO"""
    return str(self.__inner_value__)


class Name:
  """LMAO"""

  __inner_value__ = None

  def __init__(self, cls: type) -> None:
    """LMAO"""
    self.__inner_value__ = cls.__name__

  def __str__(self) -> str:
    """LMAO"""
    return str(self.__inner_value__)


class Point2D(EZData):
  """Point is a test class!"""

  x = AttriBox[int](0)
  y = AttriBox[int](0)
  z = AttriBox[int](0)

  volume = AttriBox[Volume](Instance)
  name = AttriBox[Name](Owner)

  def __str__(self) -> str:
    """String representation"""
    if TYPE_CHECKING:
      assert isinstance(self.x, int)
      assert isinstance(self.y, int)
      assert isinstance(self.z, int)
    clsName = self.name
    x, y, z = self.x, self.y, self.z
    return """%s(%d, %d, %d) = %s""" % (clsName, x, y, z, str(self.volume))

  def __getitem__(self, item: object) -> None:
    """LMAO"""
    args, kwargs = (), {}
    if isinstance(item, tuple):
      if len(item) == 1:
        args = item
        kwargs = {}
      if len(item) > 1:
        if isinstance(item[-1], dict):
          if len(item) == 2:
            if isinstance(item[0], (tuple, list)):
              args = (*item[0],)
            else:
              args = item[0]
            kwargs = item[1]
          else:
            args = (*item[:-1],)
            kwargs = item[-1]
        else:
          args = item
          kwargs = {}
    print(args)
    print(kwargs)

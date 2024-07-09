"""YOLO"""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import EmptyField
from worktoy.keenum import KeeNum, auto


class Color(KeeNum):
  """Color enumeration supporting multiple representations"""

  r = EmptyField()
  g = EmptyField()
  b = EmptyField()
  HEX = EmptyField()

  @r.GET
  def _getR(self):
    return self.value[0]

  @g.GET
  def _getG(self):
    return self.value[1]

  @b.GET
  def _getB(self):
    return self.value[2]

  @HEX.GET
  def _getHEX(self):
    return f"#{self.value[0]:02X}{self.value[1]:02X}{self.value[2]:02X}"

  red = auto(255, 0, 0)
  green = auto(0, 255, 0)
  blue = auto(0, 0, 255)

  yellow = auto(255, 255, 0)
  cyan = auto(0, 255, 255)
  magenta = auto(255, 0, 255)

  orange = auto(255, 165, 0)
  purple = auto(128, 0, 128)
  pink = auto(255, 192, 203)

"""Main Tester Script"""
#  AGPL-3.0 license
#  Copyright (c) 2023-2024 Asger Jon Vistisen
from __future__ import annotations

import os
import sys

from main_tester_class01 import OwningClass, Circle
from worktoy.desc import Field
from worktoy.yolo import yolo, runTests


def tester00() -> int:
  """Hello World!"""
  stuff = ['hello world', os, sys, frozenset]
  for item in stuff:
    print(item)
  return 0


def tester01() -> int:
  """LMAO"""
  circle = Circle(69, 420, 4)
  print(circle)
  circle.radius = 1
  print(circle)
  circle.radius = -1
  return 0


if __name__ == '__main__':
  yolo(runTests, tester01)

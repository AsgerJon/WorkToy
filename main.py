"""Main Tester Script"""
#  AGPL-3.0 license
#  Copyright (c) 2023-2024 Asger Jon Vistisen
from __future__ import annotations

import os
import sys
import time

from icecream import ic

from main_tester_class02 import Test
from main_tester_class03 import Float, ComplexNumber2, ComplexNumber
from worktoy.yolo import yolo, runTests

ic.configureOutput(includeContext=True)


def tester00() -> int:
  """Hello World!"""
  stuff = ['hello world', os, sys, ]
  for item in stuff:
    ic(item)
  return 0


def tester01() -> int:
  """Hello World!"""
  z = ComplexNumber()  # realPart and imagPart not having setter applied
  z2 = ComplexNumber2(69., 420.)
  #  We expect the types of realPart and imagPart to be of Float:
  print(z.realPart.__class__)
  print(type(z.realPart))
  print(z2.realPart.__class__)
  print(type(z2.realPart))
  return 0


if __name__ == '__main__':
  yolo(tester01)

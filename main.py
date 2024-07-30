"""Main Tester Script"""
#  AGPL-3.0 license
#  Copyright (c) 2023-2024 Asger Jon Vistisen
from __future__ import annotations

import os
import sys

from icecream import ic

from main_tester_class03 import ComplexNumber2, ComplexNumber
from worktoy.desc import SCOPE, THIS
from worktoy.yolo import yolo

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
  print(z2.label)
  return 0


def tester02() -> int:
  """LMAO"""
  print(THIS)
  print(SCOPE)
  print(isinstance(THIS, SCOPE))
  return 0


if __name__ == '__main__':
  yolo(tester01)

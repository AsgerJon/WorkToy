"""Main Tester Script"""
#  AGPL-3.0 license
#  Copyright (c) 2023-2024 Asger Jon Vistisen
from __future__ import annotations

import os
import sys
import time

from icecream import ic

from main_tester_class02 import Test
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
  test = Test()
  print(test.lmao)


if __name__ == '__main__':
  yolo(runTests, tester01)

"""Main Tester Script"""
#  AGPL-3.0 license
#  Copyright (c) 2023-2024 Asger Jon Vistisen
from __future__ import annotations

import inspect
import os
import sys
import time
from typing import Never, Any

from icecream import ic

from main_tester_script_01 import SpacePoint
from worktoy.desc import AttriBox
from worktoy.yolo import yolo, runTests

ic.configureOutput(includeContext=True)


def tester00() -> int:
  """Hello World!"""
  stuff = ['hello world', os, sys, Never, Any, ]
  stuff = [*stuff, time, ]
  for item in stuff:
    ic(item)
  return 0


def tester01() -> int:
  """Stub lol"""
  print(inspect.getfile(AttriBox))
  return 0


def tester02() -> int:
  """Stub lol"""
  lmao = SpacePoint(69, 420, 1337)
  return 0


if __name__ == '__main__':
  yolo(runTests, tester02)

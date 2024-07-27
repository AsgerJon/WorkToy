"""Main Tester Script"""
#  AGPL-3.0 license
#  Copyright (c) 2023-2024 Asger Jon Vistisen
from __future__ import annotations

import os
import sys

from icecream import ic

from worktoy.yolo import yolo, runTests

ic.configureOutput(includeContext=True)


def tester00() -> int:
  """Hello World!"""
  stuff = ['hello world', os, sys, ]
  for item in stuff:
    ic(item)
  return 0


if __name__ == '__main__':
  yolo(runTests, tester00)

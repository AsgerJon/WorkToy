"""Main Tester Script"""
#  AGPL-3.0 license
#  Copyright (c) 2023-2024 Asger Jon Vistisen
from __future__ import annotations

import os
import sys

from _yolo import runTests, yolo
from main_tester_class02 import Trig
from main_tester_class03 import PlanePoint
from worktoy.text import wordWrap, typeMsg, joinWords


def tester00() -> int:
  """Hello World!"""
  stuff = ['hello world', os, sys, frozenset]
  for item in stuff:
    print(item)
  return 0


if __name__ == '__main__':
  yolo(runTests, tester00)

"""Main Tester Script"""
#  AGPL-3.0 license
#  Copyright (c) 2023-2024 Asger Jon Vistisen
from __future__ import annotations

import os
import sys
import time
from typing import Never, Any

from icecream import ic

from worktoy.math import jitSin, intGamma, jitCos, pi
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
  """Testing metaclass stuff"""
  print(type.__subclasses__)
  for item in type.__subclasses__(type):
    print(item)
  print(type.__mro__)
  lmao = type('lmao', (object,), {})
  print(lmao.__mro__)
  return 0


def tester02() -> int:
  """Reviving loremify"""

  def identity(x: float) -> float:
    return jitSin(x) ** 2 + jitCos(x) ** 2

  for i in range(1, 10):
    print('%02d: %04d' % (i, intGamma(i + 1)))

  print(0.42069, identity(0.42069))

  return 0


def tester03() -> int:
  """Have some pi lol"""
  print('pi:', pi)
  return 0


if __name__ == '__main__':
  yolo(tester03)

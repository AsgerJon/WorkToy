"""Main Tester Script"""
#  AGPL-3.0 license
#  Copyright (c) 2023-2024 Asger Jon Vistisen
from __future__ import annotations

import os
import sys
import time
from typing import Never, Any, Callable

from icecream import ic

from mainclass02 import Point2D
from mainclass03 import WeekDay
from mainclass04 import Color

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
  """Testing EZData class"""
  A = Point2D()
  B = Point2D(1, 2, 3)
  print(A, B)

  return 0


def tester03() -> int:
  """Testing EZData class"""
  C = Point2D(4, 5, 6)
  lol = dict(lmao=True)
  C[((1, 2, 3), lol)]
  return 0


def tester04() -> int:
  """Testing KeeNum class"""
  for day in WeekDay:
    print(day, int(day))

  print('WeekDay.MONDAY + 69: ',
        int(WeekDay.MONDAY + 69),
        WeekDay.MONDAY + 69)
  return 0


def int2hex(num: int) -> str:
  """Converts an integer to a hexadecimal string"""
  return ('%2s' % hex(num).split('x')[-1].upper()).replace(' ', '0')


def tester05() -> int:
  """Testing KeeNum class"""
  for color in Color:
    r = int2hex(color.r)
    g = int2hex(color.g)
    b = int2hex(color.b)
    print(color, '#%s%s%s' % (r, g, b))
  return 0


def main(*args: Callable) -> None:
  """Main Tester Script"""
  tic = time.perf_counter_ns()
  print('Running python script located at: \n%s' % sys.argv[0])
  print('Started at: %s' % time.ctime())
  print(77 * '-')
  retCode = 0
  for callMeMaybe in args:
    print('\nRunning: %s\n' % callMeMaybe.__name__)
    try:
      retCode = callMeMaybe()
    except BaseException as exception:
      print('Exception: %s' % exception)
      retCode = -1
  retCode = 0 if retCode is None else retCode
  print(77 * '-')
  print('Return Code: %s' % retCode)
  toc = time.perf_counter_ns() - tic
  if toc < 1000:
    print('Runtime: %d nanoseconds' % (int(toc),))
  elif toc < 1000000:
    print('Runtime: %d microseconds' % (int(toc * 1e-03),))
  elif toc < 1000000000:
    print('Runtime: %d milliseconds' % (int(toc * 1e-06),))


if __name__ == '__main__':
  main(tester05)

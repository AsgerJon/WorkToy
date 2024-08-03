"""Main Tester Script"""
#  AGPL-3.0 license
#  Copyright (c) 2023-2024 Asger Jon Vistisen
from __future__ import annotations

import os
import sys

from main_tester_class02 import Trig
from main_tester_class03 import PlanePoint
from worktoy.text import wordWrap, typeMsg, joinWords
from worktoy.yolo import yolo, runTests, LoremSegment, TermText, CodeSegment


def tester00() -> int:
  """Hello World!"""
  stuff = ['hello world', os, sys, frozenset]
  for item in stuff:
    print(item)
  return 0


def tester01() -> int:
  """LMAO"""


def tester02() -> int:
  """YOLO"""

  for i in range(17):
    t = 2 * 3.14159265358979323 * i / 16
    c, s = Trig.COS(t), Trig.SIN(t)
    msg = """%.3f | %.3f | %.3f | %.3f""" % (t, c, s, c ** 2 + s ** 2)
    print(msg)
    # print(i, Trig.factorial(i))
  return 0


def tester03() -> int:
  """LMAO"""

  P = PlanePoint(69, 420)
  print(P)
  P.x = 1337
  print(P)
  P.y = 80085  # Copilot suggested this for reals, lol
  print(P)


def tester04() -> int:
  """LMAO"""

  baseString = """This is a string that is too long to fit on one line. 
    It is so long that it must be split over multiple lines. This is 
    frustrating because it is difficult to manage long strings in Python. 
    This is a problem that is solved by the 'wordWrap' function."""
  wrapped = wordWrap(40, baseString)
  print(baseString.count('\n'))
  print(len(wrapped))
  print('\n'.join(wrapped))


def tester05() -> int:
  """LMAO"""

  susObject = 69 + 0j
  susName = 'susObject'
  expectedClass = float
  e = typeMsg(susName, susObject, expectedClass)
  print(e)


def tester06() -> int:
  """LMAO"""

  words = ['one', 'two', 'three', 'four', 'five']
  print(joinWords(*words))

  return 0


def tester07() -> int:
  """LMAO"""
  print(sys.version_info)
  return 0


def tester08() -> int:
  """LMAO"""
  text = TermText()
  loremSegment1 = LoremSegment()
  loremSegment2 = LoremSegment()
  codeSegment = CodeSegment()
  with open('main_tester_class03.py', 'r') as file:
    baseCode = file.readlines()
  for line in baseCode:
    codeSegment.addLine(line)
  loremSegment1.charLen = 200
  loremSegment2.charLen = 500
  text.addSegment(loremSegment1)
  text.addSegment(codeSegment)
  text.addSegment(loremSegment2)
  print(text)
  return 0


if __name__ == '__main__':
  yolo(runTests, tester08)

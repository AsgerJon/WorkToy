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
from worktoy.mineside import FromJava
from worktoy.stat import AbstractBaseDistribution, MomentField
from worktoy.threading import Sentinel
from worktoy.yolo import yolo

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


def tester04() -> int:
  """Testing runTests"""
  print(AbstractBaseDistribution)
  return 0


def tester05() -> int:
  """Testing MomentField"""
  print(MomentField)
  bla = dict(a=1, b=2)
  print(bla)
  print(dict(bla))
  print(bla == dict(bla))
  print(getattr(bla, 'a', 'unable to find a'))
  theseTypes = type('_', (), {'__annotations__': None})()
  setattr(theseTypes, 'urmom', 'fat')
  print(theseTypes)
  print(getattr(theseTypes, 'urmom', 'lmao fail'))
  return 0


def tester06() -> int:
  """Testing MomentField"""
  descLol = type('descLol', (), {'__get__': lambda *_: 'fuck you!'})
  LMAO = type('lmao', (), {'cunt': descLol()})
  lmao = LMAO()
  print(lmao.cunt)
  print(object.__getattribute__(lmao, 'cunt'))
  return 0


def tester07() -> int:
  """Testing the error message from object.__init__"""
  bla = object()
  try:
    object.__init__(bla, 69)
  except BaseException as baseException:
    print(type(baseException))

  try:
    class lmao(yolo=True):
      pass
  except BaseException as baseException:
    print(type(baseException))
    print(baseException)

  return 0


def tester08() -> int:
  """Testing error message from init subclass"""

  def lolPrint(data: bytes) -> None:
    """LMAO"""
    print(FromJava.unJava(data))

  listener = FromJava()
  print('before start')
  listener.start()
  print('after start')

  return 0


def tester09() -> int:
  """FUCK """
  for cunt in Sentinel:
    print(cunt, ' X ', cunt.name)
    ic(cunt == 'Sentinel.PASS')

  return 0


if __name__ == '__main__':
  yolo(tester08)

"""Main Tester Script"""
#  AGPL-3.0 license
#  Copyright (c) 2023-2024 Asger Jon Vistisen
from __future__ import annotations

import os
import sys

from numpy import zeros

from main_tester_class02 import TestClass
from main_tester_class03 import Test
from worktoy.desc import AttriBox
from worktoy.yolo import yolo, runTests


def tester00() -> int:
  """Hello World!"""
  stuff = ['hello world', os, sys, frozenset()]
  for item in stuff:
    print(item)
  return 0


def multiplication(a: int, b: int) -> int:
  """LOL"""
  return a * b


def division(**kwargs) -> float:
  """LMAO"""
  numerator = kwargs.get('numerator')
  denominator = kwargs.get('denominator')
  if numerator is None or denominator is None:
    e = """Unable to resolve required arguments!"""
    raise ValueError(e)
  if isinstance(numerator, int):
    numerator = float(numerator)
  if not isinstance(numerator, float):
    raise TypeError
  if isinstance(denominator, int):
    denominator = float(denominator)
  if not isinstance(denominator, float):
    raise TypeError
  if denominator:
    return numerator / denominator
  raise ZeroDivisionError


def tester01() -> int:
  """lmao"""
  a, b = 69, 420
  print("""multiplication(%d, %d) = %d""" % (a, b, multiplication(a, b)))
  c, d = multiplication(a, b), 420
  divTest = """division(numerator = %d, denominator = %d) = %d"""
  print(divTest % (c, d, division(numerator=c, denominator=d)))
  return 0


def tester02() -> int:
  """lmao"""
  print(multiplication(a=69, b=420))
  print(multiplication(b=420, a=69, ))
  print(multiplication(69, 420))
  return 0


def tester03() -> int:
  """lmao"""
  a = [1, 2]
  b = [3, 4]
  print(a)
  print(a.extend(b) or 'LMAO')
  print(a)


def tester04() -> int:
  """lmao"""

  A = {'a': 1, 'b': 2}
  B = {'c': 3, 'd': 4}
  #  Method 1
  AB = {**A, **B}  # AB is {'a': 1, 'b': 2, 'c': 3, 'd': 4}
  print(AB)
  #  Method 2
  AB = A | B
  print(AB)
  #  Method 3 updates A in place
  A |= B
  print(A)
  A = {'a': 1, 'b': 2}  # Resetting A
  #  Method 4 updates A in place
  A.update(B)
  print(A)
  return 0


def tester05() -> int:
  """LMAO"""
  fb = lambda n: ('' if n % 3 else 'Fizz') + ('' if n % 5 else 'Buzz') or n
  for i in range(69):
    print(fb(i))
  return 0


def tester06() -> int:
  """LMAO"""

  factorial = lambda n: factorial(n - 1) * n if n else 1
  recursiveSum = lambda F, n: F(n) + (recursiveSum(F, n - 1) if n else 0)
  taylorTerm = lambda x, t: (lambda n: t(n) * x ** n / factorial(n))
  expTerm = lambda n: 1
  sinTerm = lambda n: (-1 if ((n - 1) % 4) else 1) if n % 2 else 0
  cosTerm = lambda n: sinTerm(n + 1)
  sinhTerm = lambda n: 1 if n % 2 else 0
  coshTerm = lambda n: sinhTerm(n + 1)
  exp = lambda x, n: recursiveSum(taylorTerm(x, expTerm), n)
  sin = lambda x, n: recursiveSum(taylorTerm(x, sinTerm), n)
  cos = lambda x, n: recursiveSum(taylorTerm(x, cosTerm), n)
  sinh = lambda x, n: recursiveSum(taylorTerm(x, sinhTerm), n)
  cosh = lambda x, n: recursiveSum(taylorTerm(x, coshTerm), n)
  header = """| %s | %s | %s | %s |"""
  cols = [str.center(w, 5, ' ') for w in ['x', 'cos', 'sin', 'sqr']]
  line = '-' * len(cols)

  print(header % (*cols,))
  print(line)
  for i in range(16):
    try:
      X = i / 10
      Y = exp(X, 16)
      S = sin(X, 16)
      C = cos(X, 16)
      SH = sinh(X, 16)
      CH = cosh(X, 16)
      print("""| %.3f | %.3f | %.3f | %.3f |""" % (
          X, CH, SH, CH ** 2 - SH ** 2))
    except BaseException as exception:
      raise exception
  return 0


def tester07() -> int:
  """LMAO"""
  TestClass['fuck', 'you']
  return 0


def tester08() -> int:
  """YOLO"""
  print(Test)
  print(type(Test))
  return 0


def tester09() -> int:
  """FUCK"""

  print(dict(a=1, b=2) | dict(b=3))
  return 0


if __name__ == '__main__':
  yolo(runTests, tester08)

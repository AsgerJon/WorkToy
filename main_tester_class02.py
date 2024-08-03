"""Implementation of math functions using KeeNum"""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Callable, Any
from worktoy.keenum import KeeNum, auto


class Trig(KeeNum):
  """Enumeration of trigonometric functions."""

  @classmethod
  def factorial(cls, n: int) -> int:
    """This function returns the factorial of the argument."""
    if n:
      return n * cls.factorial(n - 1)
    return 1

  @classmethod
  def recursiveSum(cls, callMeMaybe: Callable, n: int) -> float:
    """This function returns the sum of the function F from 0 to n."""
    if n:
      return callMeMaybe(n) + cls.recursiveSum(callMeMaybe, n - 1)
    return callMeMaybe(n)

  @classmethod
  def taylorTerm(cls, x: float, callMeMaybe: Callable) -> Callable:
    """This function returns a function that calculates the nth term of a
    Taylor series expansion."""

    def polynomial(n: int) -> float:
      return callMeMaybe(n) * x ** n / cls.factorial(n)

    return polynomial

  @auto
  def SIN(self, x: float) -> float:
    """This method returns the sine of the argument."""
    term = lambda n: [0, 1, 0, -1][n % 4]
    return self.recursiveSum(self.taylorTerm(x, term), 17)

  @auto
  def COS(self, x: float) -> float:
    """This method returns the cosine of the argument."""
    term = lambda n: [1, 0, -1, 0][n % 4]
    return self.recursiveSum(self.taylorTerm(x, term), 17)

  @auto
  def SINH(self, x: float) -> float:
    """This method returns the hyperbolic sine of the argument."""
    term = lambda n: n % 2
    return self.recursiveSum(self.taylorTerm(x, term), 16)

  @auto
  def COSH(self, x: float) -> float:
    """This method returns the hyperbolic cosine of the argument."""
    term = lambda n: (n + 1) % 2
    return self.recursiveSum(self.taylorTerm(x, term), 16)

  def __call__(self, *args, **kwargs) -> Any:
    """Calls are passed on to the public value"""
    return self.value(self, *args, **kwargs)

"""
MathFunc encapsulates mathematical functions that map from R to R.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.core import Object

if TYPE_CHECKING:  # pragma: no cover
  from typing import Callable, Union, Self


class MathFunc(Object):
  """MathFunc encapsulates mathematical functions that map from R to R."""

  __anon_func__ = None
  __inf_mal__ = 1e-12

  def __init__(self, real2real: Callable[[float], float]) -> None:
    """
    Initialize the MathFunc with a real to real function.

    :param real2real: A callable that takes a float and returns a float.
    """
    self.__anon_func__ = real2real

  def __call__(self, x: float) -> float:
    return self.__anon_func__(x)

  def derivative(self, ) -> Self:
    """
    Compute the derivative of the function at a given point x.

    :param x: The point at which to compute the derivative.
    :return: The derivative of the function at x.
    """

    def d(x: float) -> float:
      f = self.__anon_func__
      _d = self.__inf_mal__
      return (f(x + _d) - f(x - _d)) / (2 * _d)

    cls = type(self)
    return cls(d)

  def antiDerivative(self, ) -> Self:
    """
    Compute the anti-derivative of the function.

    :return: A new MathFunc representing the anti-derivative.
    """

    def antiD(x: float, C: float = None) -> float:
      f = self.__anon_func__
      _d = self.__inf_mal__
      if C is None:
        C = 0.0
      x0 = 0
      step = (x - x0) / 100
      return C + sum(f(x0 + i * step) * step for i in range(100))

    cls = type(self)
    return cls(antiD)

  def inverse(self, ) -> Union[Self, None]:
    """
    Compute the inverse of the function if it is invertible.

    :return: A new MathFunc representing the inverse function or None if
    not invertible.
    """

    def inv(y: float) -> float:
      f = self.__anon_func__
      loss = type(self)(lambda x: abs(f(x) - y))
      dLoss = loss.derivative()
      x0 = 0.0
      step = 0.01
      for _ in range(1000):
        x1 = x0 - loss(x0) / dLoss(x0)
        if abs(x1 - x0) < 1e-6:
          return x1
        x0 = x1
      raise ValueError("Inverse not found within tolerance.")

    cls = type(self)
    return cls(inv)

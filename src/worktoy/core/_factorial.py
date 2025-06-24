"""
The 'factorial' function calculates the factorial of a given number.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations


def factorial(n: int) -> int:
  """
  Calculate the factorial of a given number.

  Args:
      n (int): The number to calculate the factorial of.

  Returns:
      int: The factorial of the number.
  """
  if n < 0:
    raise ValueError("Factorial is not defined for negative numbers.")
  out = 1
  for i in range(2, n + 1):
    out *= i
  return out

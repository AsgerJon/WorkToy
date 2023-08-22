"""WorkToy - Numeric Attribute
This class implements attributes representing numerical values.
"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
import string

from worktoy import ImmutableAttribute


class NumAttribute(ImmutableAttribute):
  """WorkToy - Numeric Attribute
  This class implements attributes representing numerical values. """

  @staticmethod
  def _sign(value: str) -> int:
    """Attempts to find the sign of the number"""
    out = 1
    for char in value:
      if char in string.digits:
        return out
      if char == '-' and out == 1:
        out = -1
      elif char == '-' and out == -1:
        return 1
    return out

  @staticmethod
  def _log10(value: str) -> int:
    """Attempts to find a single period or comma to assumed to represent
    the number comma."""
    for limiter in '., ':
      test = value.split(limiter)
      if test == 1:
        return len(value.split('.')[-1])
    return 0

  @staticmethod
  def string2Int(value: str) -> int:
    """Attempts to convert the string to an int"""
    sign = NumAttribute._sign(value)
    base = ''.join([
      string.ascii_uppercase,
      string.ascii_lowercase,
      string.punctuation,
      string.whitespace,
    ])
    for char in base:
      value = value.replace(char, '')
    digs = []
    for char in value:
      for i in range(10):
        if char == '%d' % i:
          digs.append(i)
    digs.reverse()
    out = 0
    for (i, dig) in enumerate(digs):
      out += (dig * 10 ** i)
    return out * sign

  @staticmethod
  def string2Float(value: str) -> float:
    """Attempts to convert the string to a float"""
    log10 = NumAttribute._log10(value)
    digs = NumAttribute.string2Int(value)
    return digs / (10 ** log10)

  def __init__(self, *args, **kwargs) -> None:
    ImmutableAttribute.__init__(self, *args, **kwargs)

  @abstractmethod
  def _typeCheck(self, value: object) -> bool:
    """Passed on from AbstractAttribute"""

  @abstractmethod
  def _typeGuard(self, value: object) -> object:
    """Passed on from AbstractAttribute"""

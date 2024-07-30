"""LMAO"""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from worktoy.desc import AttriBox
from worktoy.parse import maybe


class Float:
  """For the sake of the example, this class is used instead of float"""

  __fallback_value__ = 0.0
  __inner_value__ = None

  def __init__(self, *args) -> None:
    for arg in args:
      if isinstance(arg, int):
        self.__inner_value__ = float(arg)
        break
      if isinstance(arg, float):
        self.__inner_value__ = arg
        break
    else:
      self.__inner_value__ = self.__fallback_value__

  def __getattr__(self, key: str) -> Any:
    """Tries to use the attribute from the inner value"""
    try:
      return getattr(self.__inner_value__, key)
    except AttributeError:
      return object.__getattribute__(self, key)

  def __float__(self) -> float:
    """Returns the inner value"""
    return self.__inner_value__


class ComplexNumber:
  """Complex number representation"""

  __fallback_value__ = 0j
  realPart = AttriBox[Float](69.)
  imagPart = AttriBox[Float](420.)

  def __str__(self) -> str:
    """String representation"""
    a, b = float(self.realPart), float(self.imagPart)
    return """%.3f + %.3f I""" % (a, b)


class ComplexNumber2:
  """Complex number representation"""

  __fallback_value__ = 0j
  realPart = AttriBox[Float](69.)
  imagPart = AttriBox[Float](420.)
  label = AttriBox[str]('lmao')

  def __str__(self) -> str:
    """String representation"""
    a, b = float(self.realPart), float(self.imagPart)
    return """%.3f + %.3f I""" % (a, b)

  def __init__(self, *args) -> None:
    a, b = None, None
    for arg in args:
      if isinstance(arg, (int, float)):
        if a is None:
          a = float(arg)
        elif b is None:
          b = float(arg)
          break
      elif isinstance(arg, complex):
        a, b = arg.real, arg.imag
        break
    else:
      a = maybe(a, 0.0)
      b = maybe(b, 0.0)
    self.realPart = Float(a)
    self.imagPart = Float(b)
    self.label = 'fuck you!'

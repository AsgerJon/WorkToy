"""TestWaitForIt tests the WaitForIt class."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

import os
from math import atan2
from unittest import TestCase

from worktoy.attr import Field, WaitForIt
from worktoy.parse import maybe
from worktoy.static import THIS, overload, OWNER
from worktoy.mcls import BaseObject

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, Optional, Union, Self, Callable, TypeAlias


class Foo(BaseObject):
  """Testing"""

  className = WaitForIt(OWNER, '__name__')
  hereIsMyNumber = 'Call Me Maybe!'
  currentWorkingDirectory = WaitForIt(os.getcwd)
  thisIsCrazy = WaitForIt('hereIsMyNumber')

  def __str__(self, ) -> str:
    """
    Returns:
      str: The string representation of the object.
    """

    infoSpec = """The current working directory is: '%s'!"""
    info = infoSpec % self.currentWorkingDirectory
    return info


class ComplexNumber(BaseObject):
  """ComplexNumber is a class that represents a complex number."""

  __complex_value__ = None
  VALUE = WaitForIt(complex, THIS)
  REAL = Field()
  IMAG = Field()
  arg = WaitForIt(lambda self: atan2(self.IMAG, self.REAL, ), THIS)
  abs_ = WaitForIt(lambda self: abs(self.REAL + self.IMAG * 1j, ), THIS)

  @REAL.GET
  def _getREAL(self, ) -> float:
    """
    Returns:
      float: The real part of the complex number.
    """
    return self.__complex_value__.real

  @IMAG.GET
  def _getIMAG(self, ) -> float:
    """
    Returns:
      float: The imaginary part of the complex number.
    """
    return self.__complex_value__.imag

  def __complex__(self) -> complex:
    """Complex value"""
    return maybe(self.__complex_value__, 0 + 0j)

  @overload(float, float)
  @overload(int, int)
  def __init__(self, x: float, y: float) -> None:
    """
    Initialize the complex number.

    Args:
      x (float): The real part of the complex number.
      y (float): The imaginary part of the complex number.
    """
    self.__complex_value__ = float(x) + float(y) * 1j

  @overload(complex)
  def __init__(self, other: complex) -> None:
    """
    Initialize the complex number.

    Args:
      other (complex): The complex number.
    """
    self.__complex_value__ = other

  @overload()
  def __init__(self, ) -> None:
    """
    Initialize the complex number.
    """
    pass


class TestWaitForIt(TestCase):
  """TestWaitForIt tests the WaitForIt class."""

  def test_simple(self) -> None:
    """
    Test the WaitForIt class.
    """
    foo = Foo()
    self.assertEqual(foo.currentWorkingDirectory, os.getcwd())
    self.assertEqual(foo.thisIsCrazy, 'Call Me Maybe!')
    self.assertEqual(foo.className, 'Foo')

  def test_advanced(self, ) -> None:
    """
    Test the WaitForIt class in a more advanced way.
    """
    complexNumber = ComplexNumber(69, 420)
    self.assertEqual(complexNumber.VALUE, 69 + 420j)
    self.assertEqual(complexNumber.REAL, 69)
    self.assertEqual(complexNumber.IMAG, 420)
    self.assertEqual(complexNumber.arg, atan2(420, 69))
    self.assertEqual(complexNumber.abs_, abs(69 + 420j))

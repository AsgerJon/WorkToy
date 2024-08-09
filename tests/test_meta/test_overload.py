"""TestOverload tests the overloading functionality of the BaseMetaclass.
The tests focus on the color class defined above. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.meta import BaseObject, overload
from worktoy.desc import AttriBox

try:
  from typing import Callable
except ImportError:
  Callable = object


class Complex(BaseObject):
  """Complex Number representation"""

  realPart = AttriBox[float]()
  imgPart = AttriBox[float]()

  @overload()
  def __init__(self, ) -> None:
    self.realPart = 0.
    self.imgPart = 0.

  @overload(complex)
  def __init__(self, *args) -> None:
    self.realPart = args[0].real
    self.imgPart = args[0].imag

  @overload(float, float)
  @overload(float, float, float)
  def __init__(self, *args) -> None:
    self.realPart = args[0]
    self.imgPart = args[1]


class TestOverload(TestCase):
  """TestOverload tests the overloading functionality of the
  BaseMetaclass. The tests focus on the color class defined above. """

  def setUp(self) -> None:
    """Sets up each test method."""
    self.emptyPoint = Complex()
    self.complexPoint = Complex(3 + 4j)
    self.point = Complex(5., 12.)
    self.triplePoint = Complex(69, 420, 1337)

  def test_init(self) -> None:
    """Test if the __init__ method works correctly."""
    self.assertEqual(self.emptyPoint.realPart, 0.)
    self.assertEqual(self.emptyPoint.imgPart, 0.)

    self.assertEqual(self.complexPoint.realPart, 3.)
    self.assertEqual(self.complexPoint.imgPart, 4.)

    self.assertEqual(self.point.realPart, 5.)
    self.assertEqual(self.point.imgPart, 12.)

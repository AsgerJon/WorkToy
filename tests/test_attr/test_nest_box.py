"""
TestNestBox tests the NestBox class from the attr module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.mcls import BaseObject
from worktoy.static import overload
from worktoy.waitaminute import ReadOnlyError, ProtectedError
from worktoy.waitaminute import TypeException

from worktoy.attr import AttriBox, NestBox
from worktoy.static.zeroton import THIS
from worktoy.text import stringList

from . import PlanePoint, PlaneCircle

try:
  from typing import TYPE_CHECKING
except ImportError:  # pragma: no cover
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Self


class RGB(BaseObject):
  """TestNestBox tests the NestBox class."""

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Fallback Variables
  __fallback_red__ = 0
  __fallback_green__ = 0
  __fallback_blue__ = 0

  #  Public Variables
  red = NestBox[int](__fallback_red__)
  green = NestBox[int](__fallback_green__)
  blue = NestBox[int](__fallback_blue__)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(int, int, int)
  def __init__(self, red: int, green: int, blue: int, **kwargs) -> None:
    """Initialize the RGB color."""
    self.red = red
    self.green = green
    self.blue = blue

  @overload(THIS)
  def __init__(self, other: Self, **kwargs) -> None:
    """Initialize the RGB color from another RGB object."""
    self.__init__(other.red, other.green, other.blue, **kwargs)


class Brush(BaseObject):
  """Brush represents a drawing brush with a color."""

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Public Variables
  color = NestBox[RGB]()
  width = AttriBox[int](1)


class TestNestBox(TestCase):
  """TestNestBox tests the NestBox class."""

  def setUp(self) -> None:
    """Set up the test case."""
    self.brush = Brush()
    self.brush.color = RGB(255, 0, 0)

  def test_init(self) -> None:
    """Test the initialization of the Brush class."""
    self.assertIsInstance(self.brush, Brush)
    self.assertIsInstance(Brush.color, NestBox)
    self.assertIsInstance(Brush.width, AttriBox)

  def test_color_setter(self) -> None:
    """Test setting the color of the brush."""
    self.brush.color = RGB(0, 255, 0)
    self.assertEqual(self.brush.color.red, 0)
    self.assertEqual(self.brush.color.green, 255)
    self.assertEqual(self.brush.color.blue, 0)

  def test_nest_setter(self) -> None:
    """Test setting the color of the brush using NestBox."""
    self.brush.color.red = 69
    self.brush.color.green = 42
    self.brush.color.blue = 137
    self.assertEqual(self.brush.color.red, 69)
    self.assertEqual(self.brush.color.green, 42)
    self.assertEqual(self.brush.color.blue, 137)

  def test_color_getter(self) -> None:
    """Test getting the color of the brush."""
    color = self.brush.color
    self.assertIsInstance(color, RGB)
    self.assertEqual(color.red, 255)
    self.assertEqual(color.green, 0)
    self.assertEqual(color.blue, 0)

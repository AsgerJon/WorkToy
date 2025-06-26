"""
TestNestBox tests the NestBox class from the attr module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from tests import WYD
from unittest import TestCase

from worktoy.mcls import BaseObject
from worktoy.static import overload
from worktoy.waitaminute import ReadOnlyError, ProtectedError
from worktoy.waitaminute import TypeException

from worktoy.attr import AttriBox, NestBox
from worktoy.static.zeroton import THIS
from worktoy.text import stringList

from . import PlanePoint, PlaneCircle

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
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

  @overload()
  def __init__(self, **kwargs) -> None:
    """Initialize the RGB color with default values."""
    pass

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __str__(self) -> str:
    """
    Returns a string representation of the RGB color in the #RRGGBB format.
    """
    return f"#{self.red:02X}{self.green:02X}{self.blue:02X}"


class Brush(BaseObject):
  """Brush represents a drawing brush with a color."""

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Public Variables
  color = NestBox[RGB](255, 255, 255)
  width = AttriBox[int](1)


class TestNestBox(TestCase):
  """TestNestBox tests the NestBox class."""

  @classmethod
  def tearDownClass(cls) -> None:
    import sys
    import gc
    sys.modules.pop(__name__, None)
    gc.collect()

  def setUp(self) -> None:
    """Set up the test case."""
    self.brush = Brush()
    self.black = RGB()
    self.schwartz = RGB(self.black)

  def test_init(self) -> None:
    """Test the initialization of the Brush class."""
    self.assertIsInstance(self.brush, Brush)
    self.assertIsInstance(Brush.color, NestBox)
    self.assertIsInstance(Brush.width, AttriBox)

  def test_str(self) -> None:
    """Test the string representation of the RGB color."""
    self.assertEqual(str(self.black), '#000000')
    self.assertEqual(str(self.schwartz), '#000000')
    self.assertEqual(str(self.brush.color), '#FFFFFF')

  def test_color_getter(self) -> None:
    """Tests the default color of the brush."""
    self.assertIsInstance(self.brush.color, RGB)
    self.assertEqual(self.brush.color.red, 255)
    self.assertEqual(self.brush.color.green, 255)
    self.assertEqual(self.brush.color.blue, 255)

  def test_color_setter(self) -> None:
    """Test setting the color of the brush."""
    self.brush.color = RGB(0, 255, 0)
    self.assertEqual(self.brush.color.red, 0)
    self.assertEqual(self.brush.color.green, 255)
    self.assertEqual(self.brush.color.blue, 0)
    self.brush.color.red = 255
    self.brush.color.green = 0
    self.brush.color.blue = 255
    self.assertEqual(self.brush.color.red, 255)
    self.assertEqual(self.brush.color.green, 0)
    self.assertEqual(self.brush.color.blue, 255)

  def test_nest_setter(self) -> None:
    """Test setting the color of the brush using NestBox."""
    self.brush.color.red = 69
    self.brush.color.green = 42
    self.brush.color.blue = 137
    self.assertEqual(self.brush.color.red, 69)
    self.assertEqual(self.brush.color.green, 42)
    self.assertEqual(self.brush.color.blue, 137)

  def test_removed_value(self) -> None:
    """
    Testing that the Field descriptor raises MissingVariable when a value
    is removed. This should also cause the creation of a new object.
    """
    pvtName = Brush.color.getPrivateName()
    setattr(self, pvtName, None)
    r, g, b = Brush.color._getPositionalArgs()
    self.assertEqual(self.brush.color.red, r)
    self.assertEqual(self.brush.color.green, g)
    self.assertEqual(self.brush.color.blue, b)

  def test_set_wrong_but_castable(self) -> None:
    """
    Tests that setting the color to a wrong type still works, provided the
    new value can be cast to the expected type.
    """
    self.brush.color = 255, 0, 0
    self.assertEqual(self.brush.color.red, 255)
    self.assertEqual(self.brush.color.green, 0)
    self.assertEqual(self.brush.color.blue, 0)

  def test_set_wrong_type(self) -> None:
    """
    Tests that setting the color to a wrong type raises TypeException.
    """
    with self.assertRaises(TypeException) as context:
      self.brush.color = 'breh'
    exception = context.exception
    self.assertEqual(exception.varName, 'value')
    self.assertEqual(exception.actualObject, 'breh')
    self.assertEqual(exception.actualType, str)
    self.assertIs(exception.expectedType[0], RGB)

  def test_deleted_color(self) -> None:
    """
    Tests that color can be deleted
    """
    self.assertIsInstance(self.brush.color, RGB)
    del self.brush.color
    with self.assertRaises(AttributeError) as context:
      _ = self.brush.color
    exception = context.exception
    expectedWords = stringList("""has no attribute""")
    for word in expectedWords:
      self.assertIn(word.lower(), str(exception).lower())

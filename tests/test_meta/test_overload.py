"""TestOverload tests the overloading functionality of the BaseMetaclass."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.desc import OLDAttriBox
from worktoy.meta import BaseObject, overload


class Color(BaseObject):
  """Color provides a test case for functional overloading, since colors
  can be defined in multiple ways."""

  red = OLDAttriBox[int](0)
  green = OLDAttriBox[int](0)
  blue = OLDAttriBox[int](0)

  @overload(int, int, int)
  def __init__(self, red: int, green: int, blue: int) -> None:
    self.red = red
    self.green = green
    self.blue = blue
    BaseObject.__init__(self, )

  @overload(str)
  def __init__(self, hexCode: str) -> None:
    if hexCode[0] == '#':
      hexCode = hexCode[1:]
    self.red = int(hexCode[0:2], 16)
    self.green = int(hexCode[2:4], 16)
    self.blue = int(hexCode[4:6], 16)
    BaseObject.__init__(self, )

  @overload(float, float, float)
  def __init__(self, *args) -> None:
    r, g, b = args
    self.__init__(int(r * 255), int(g * 255), int(b * 255))

  @overload(dict)
  def __init__(self, rgb: dict) -> None:
    self.__init__(rgb['red'], rgb['green'], rgb['blue'])

  @overload()
  def __init__(self) -> None:
    self.__init__(0, 0, 0)

  def __str__(self) -> str:
    """Returns the hex code of the color."""
    return '#%02x%02x%02x' % (self.red, self.green, self.blue)

  def __repr__(self) -> str:
    """Returns the hex code of the color."""
    return """Color(%d, %d, %d)""" % (self.red, self.green, self.blue)

  def __sub__(self, other: Color) -> Color:
    """Subtracts two colors."""
    return Color(self.red - other.red, self.green - other.green,
                 self.blue - other.blue)

  def __abs__(self, ) -> float:
    """Returns the absolute value of the color."""
    return (self.red ** 2 + self.green ** 2 + self.blue ** 2) ** 0.5


class TestOverload(TestCase):
  """TestOverload tests the overloading functionality of the
  BaseMetaclass. The tests focus on the color class defined above. """

  def testBase(self) -> None:
    """Tests the basic functionality of the Color class."""
    black = Color()
    self.assertEqual(black.red, 0)
    self.assertEqual(black.green, 0)
    self.assertEqual(black.blue, 0)

  def testBaseHex(self) -> None:
    """Tests the hex code constructor of the Color class."""
    black = Color()
    self.assertEqual(str(black).lower(), '#000000'.lower())

  def testFloat(self) -> None:
    """Tests the float constructor of the Color class."""
    floatWhite = Color(1.0, 1.0, 1.0)
    intWhite = Color(255, 255, 255)
    self.assertLess(abs(floatWhite - intWhite), 9)
    floatBlack = Color(0.0, 0.0, 0.0)
    intBlack = Color(0, 0, 0)
    self.assertLess(abs(floatBlack - intBlack), 9)
    floatPink = Color(1.0, 0.0, 0.5)
    intPink = Color(255, 0, 127)
    self.assertLess(abs(floatPink - intPink), 9)

  def testDict(self, ) -> None:
    """Tests the dictionary constructor of the Color class."""
    orange = Color({'red': 255, 'green': 165, 'blue': 0})
    orangeStr = Color('#ffa500')
    orangeFloat = Color(1.0, 0.647, 0.0)
    self.assertEqual(str(orange).lower(), '#ffa500'.lower())
    self.assertLess(abs(orange - Color(1.0, 0.647, 0.0)), 9)

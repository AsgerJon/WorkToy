"""TestSingleton tests the Singleton class. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.desc import AttriBox
from worktoy.meta import Singleton, overload


class Unique(Singleton):
  """Unique class used to test Singleton"""

  x = AttriBox[float](0.0)
  y = AttriBox[float](0.0)

  name = AttriBox[str]('')

  @overload()
  def __init__(self, ) -> None:
    self.name = self.__class__.__name__

  @overload(str)
  def __init__(self, arg: str) -> None:
    """Constructor for the Unique class."""
    self.name = arg

  @overload(str, complex)
  def __init__(self, arg: str, _z: complex) -> None:
    self.x, self.y = _z.real, _z.imag
    self.__init__(arg)

  @overload(str, float, float)
  def __init__(self, arg: str, _x: float, _y: float) -> None:
    """Constructor for the Unique class."""
    self.x, self.y = _x, _y
    self.__init__(arg)

  @overload(float, float)
  def __init__(self, _x: float, _y: float) -> None:
    """Constructor for the Unique class."""
    self.x, self.y = _x, _y
    self.__init__()

  @overload(complex)
  def __init__(self, _z: complex) -> None:
    self.x, self.y = _z.real, _z.imag
    self.__init__()

  @overload(str, int, int)
  def __init__(self, arg: str, _x: int, _y: int) -> None:
    """Constructor for the Unique class."""
    self.x, self.y = float(_x), float(_y)
    self.__init__(arg)

  @overload(int, int)
  def __init__(self, _x: int, _y: int) -> None:
    """Constructor for the Unique class."""
    self.x, self.y = float(_x), float(_y)
    self.__init__()

  def __str__(self) -> str:
    """String representation"""
    return self.name


class TestSingleton(TestCase):
  """TestSingleton tests the Singleton class. """

  def setUp(self) -> None:
    """Sets up each test method."""

  def testSingleness(self) -> None:
    """Test if the Singleton is truly a Singleton. """
    a = Unique()
    b = Unique()
    self.assertIs(a, b)

  def testUpdate(self) -> None:
    """The Singleton should update the value of the attributes at each
    call to the class"""
    a = Unique('lol', 0, 0, )
    self.assertEqual(a.name, 'lol')
    self.assertEqual(a.x, 0.0)
    self.assertEqual(a.y, 0.0)
    b = Unique('lmao', 69, 420, )
    self.assertIs(a, b)
    self.assertEqual(a.name, 'lmao')
    self.assertEqual(a.x, 69.0)
    self.assertEqual(a.y, 420.0)

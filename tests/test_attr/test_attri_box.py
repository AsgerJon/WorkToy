"""TestAttriBox - Test the Attribox class."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase
from math import atan2, pi
from random import random

from worktoy.attr import AttriBox, Field
from worktoy.mcls import BaseMeta, BaseObject
from worktoy.parse import maybe
from worktoy.static import overload, THIS
from worktoy.waitaminute import DispatchException

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Self, Any


class Point3d(BaseObject):
  """Point3d is a class that represents a point in 3D space."""

  x = AttriBox[float](0.0)
  y = AttriBox[float](0.0)
  z = AttriBox[float](0.0)

  @overload(float, float, float)
  def __init__(self, x: float, y: float, z: float) -> None:
    """Initialize the Point3d object."""
    self.x = x
    self.y = y
    self.z = z

  @overload(THIS)
  def __init__(self, other: Self) -> None:
    """Initialize the Point3d object."""
    self.x = other.x
    self.y = other.y
    self.z = other.z

  @overload()
  def __init__(self, **kwargs) -> None:
    """Initialize the Point3d object."""
    self.x = kwargs.get('x', 0.0)
    self.y = kwargs.get('y', 0.0)
    self.z = kwargs.get('z', 0.0)

  def __str__(self) -> str:
    """Return a string representation of the Point3d object."""
    clsName = type(self).__name__
    x, y, z = ['%.3f' % a for a in (self.x, self.y, self.z)]
    return """%s(x=%s, y=%s, z=%s)""" % (clsName, x, y, z)

  def __repr__(self) -> str:
    """Return a string representation of the Point3d object."""
    clsName = type(self).__name__
    x, y, z = ['%.3f' % a for a in (self.x, self.y, self.z)]
    return """%s(%s, %s, %s)""" % (clsName, x, y, z)

  def __abs__(self, ) -> float:
    """Return the absolute value of the Point3d object."""
    return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5

  def __len__(self, ) -> int:
    """Return the length of the Point3d object."""
    return 3


class Sphere(BaseObject):
  """Represents a spatial sphere. """

  #  Real Attributes
  radius = AttriBox[float](1.0)
  center = AttriBox[Point3d](Point3d(0.0, 0.0, 0.0))

  #  Virtual Attributes
  volume = Field()
  area = Field()

  #  Virtual getters
  @volume.GET
  def _getVolume(self) -> float:
    """Return the volume of the sphere."""
    return (4.0 / 3.0) * pi * self.radius ** 3

  @area.GET
  def _getArea(self) -> float:
    """Return the surface area of the sphere."""
    return 4.0 * pi * self.radius ** 2

  @overload(float, Point3d)
  def __init__(self, radius: float, center: Point3d) -> None:
    """Initialize the Sphere object."""
    self.radius = radius
    self.center = center

  @overload(Point3d, float)
  def __init__(self, other: Self, radius: float) -> None:
    """Initialize the Sphere object."""
    self.__init__(radius, other)

  @overload(THIS)
  def __init__(self, other: Self) -> None:
    """Initialize the Sphere object."""
    self.__init__(other.radius, other.center)

  @overload(Point3d)
  def __init__(self, other: Self) -> None:
    """Initialize the Sphere object."""
    self.__init__(1.0, other)

  @overload(float)
  def __init__(self, radius: float) -> None:
    """Initialize the Sphere object."""
    self.__init__(radius, Point3d())

  @overload()
  def __init__(self, **kwargs) -> None:
    """Initialize the Sphere object."""
    self.radius = kwargs.get('radius', 1.0)
    self.center = kwargs.get('center', Point3d(0.0, 0.0, 0.0))

  def __str__(self) -> str:
    """Return a string representation of the Sphere object."""
    clsName = type(self).__name__
    radius = '%.3f' % self.radius
    center = str(self.center)
    return """%s(radius=%s, center=%s)""" % (clsName, radius, center)

  def __repr__(self) -> str:
    """Return a string representation of the Sphere object."""
    clsName = type(self).__name__
    radius = '%.3f' % self.radius
    center = str(self.center)
    return """%s(%s, %s)""" % (clsName, radius, center)


class TestAttriBox(TestCase):
  """Test the AttriBox class."""

  def setUp(self) -> None:
    """Sets up the test."""

    self.point0 = Point3d()
    self.point1 = Point3d(69., 420., 1337.)
    self.point2 = Point3d(420., 1337., 69.)
    self.center = Point3d(69., 420., 1337.)
    self.radius = 80085.
    self.sphere = Sphere(self.radius, self.center)

  def test_init(self, ) -> None:
    """Test that objects correctly initializes."""
    self.assertEqual(self.point0.x, 0.0)
    self.assertEqual(self.point0.y, 0.0)
    self.assertEqual(self.point0.z, 0.0)
    self.assertEqual(self.point1.x, 69.0)
    self.assertEqual(self.point1.y, 420.0)
    self.assertEqual(self.point1.z, 1337.0)
    self.assertEqual(self.point2.x, 420.0)
    self.assertEqual(self.point2.y, 1337.0)
    self.assertEqual(self.point2.z, 69.0)
    self.assertEqual(self.sphere.radius, self.radius)
    self.assertEqual(self.sphere.center.x, self.center.x)
    self.assertEqual(self.sphere.center.y, self.center.y)
    self.assertEqual(self.sphere.center.z, self.center.z)

  def test_set(self, ) -> None:
    """Tests that the setter works."""
    if TYPE_CHECKING:
      assert isinstance(self.point0, Point3d)
      assert isinstance(self.point1, Point3d)
      assert isinstance(self.point2, Point3d)
      assert isinstance(self.sphere, Sphere)
      assert isinstance(Point3d.x, float)
      assert isinstance(Point3d.y, float)
      assert isinstance(Point3d.z, float)
      assert isinstance(Sphere.radius, float)
      assert isinstance(Sphere.center, Point3d)

    #  Point 0
    self.assertAlmostEqual(self.point0.x, 0.0)
    self.assertAlmostEqual(self.point0.y, 0.0)
    self.assertAlmostEqual(self.point0.z, 0.0)
    self.point0.x = 69.
    self.point0.y = 420.
    self.point0.z = 80085.
    self.assertAlmostEqual(self.point0.x, 69.0)
    self.assertAlmostEqual(self.point0.y, 420.0)
    self.assertAlmostEqual(self.point0.z, 80085.0)
    #  Point 1
    self.assertAlmostEqual(self.point1.x, 69.0)
    self.assertAlmostEqual(self.point1.y, 420.0)
    self.assertAlmostEqual(self.point1.z, 1337.0)
    self.point1.x = 0.
    self.point1.y = 0.
    self.point1.z = 0.
    self.assertAlmostEqual(self.point1.x, 0.0)
    self.assertAlmostEqual(self.point1.y, 0.0)
    self.assertAlmostEqual(self.point1.z, 0.0)
    #  Point 2
    self.assertAlmostEqual(self.point2.x, 420.0)
    self.assertAlmostEqual(self.point2.y, 1337.0)
    self.assertAlmostEqual(self.point2.z, 69.0)
    self.point2.x = 69.
    self.point2.y = 420.
    self.point2.z = 80085.
    self.assertAlmostEqual(self.point2.x, 69.0)
    self.assertAlmostEqual(self.point2.y, 420.0)
    self.assertAlmostEqual(self.point2.z, 80085.0)
    #  Sphere
    self.assertAlmostEqual(self.sphere.radius, 80085.0)
    expectedCenter = self.center
    actualCenter = self.sphere.center
    self.assertAlmostEqual(actualCenter.x, expectedCenter.x)
    self.assertAlmostEqual(actualCenter.y, expectedCenter.y)
    self.assertAlmostEqual(actualCenter.z, expectedCenter.z)
    self.sphere.radius = 69.
    self.sphere.center = Point3d(0., 0., 0.)
    self.assertAlmostEqual(self.sphere.radius, 69.0)
    expectedCenter = Point3d(0.0, 0.0, 0.0)
    actualCenter = self.sphere.center
    self.assertAlmostEqual(actualCenter.x, expectedCenter.x)
    self.assertAlmostEqual(actualCenter.y, expectedCenter.y)
    self.assertAlmostEqual(actualCenter.z, expectedCenter.z)

  def test_del(self, ) -> None:
    """Test that the deleter works."""
    #  Point 0
    self.assertAlmostEqual(self.point0.x, 0.0)
    self.assertAlmostEqual(self.point0.y, 0.0)
    self.assertAlmostEqual(self.point0.z, 0.0)
    del self.point0.x
    del self.point0.y
    del self.point0.z
    with self.assertRaises(AttributeError):
      _ = self.point0.x
    with self.assertRaises(AttributeError):
      _ = self.point0.y
    with self.assertRaises(AttributeError):
      _ = self.point0.z
    #  Point 1
    self.assertAlmostEqual(self.point1.x, 69.0)
    self.assertAlmostEqual(self.point1.y, 420.0)
    self.assertAlmostEqual(self.point1.z, 1337.0)
    del self.point1.x
    del self.point1.y
    del self.point1.z
    with self.assertRaises(AttributeError):
      _ = self.point1.x
    with self.assertRaises(AttributeError):
      _ = self.point1.y
    with self.assertRaises(AttributeError):
      _ = self.point1.z
    #  Point 2
    self.assertAlmostEqual(self.point2.x, 420.0)
    self.assertAlmostEqual(self.point2.y, 1337.0)
    self.assertAlmostEqual(self.point2.z, 69.0)
    del self.point2.x
    del self.point2.y
    del self.point2.z
    with self.assertRaises(AttributeError):
      _ = self.point2.x
    with self.assertRaises(AttributeError):
      _ = self.point2.y
    with self.assertRaises(AttributeError):
      _ = self.point2.z
    #  Sphere
    self.assertAlmostEqual(self.sphere.radius, 80085.0)
    self.assertAlmostEqual(self.sphere.center.x, 69.0)
    self.assertAlmostEqual(self.sphere.center.y, 420.0)
    self.assertAlmostEqual(self.sphere.center.z, 1337.0)
    del self.sphere.radius
    del self.sphere.center
    with self.assertRaises(AttributeError):
      _ = self.sphere.radius
    with self.assertRaises(AttributeError):
      _ = self.sphere.center
    del self.sphere
    with self.assertRaises(AttributeError):
      _ = self.sphere

  def test_type_set(self) -> None:
    """Tests that setting to wrong type raises an error."""
    #  Point 0
    with self.assertRaises(TypeError):
      self.point0.x = '69'
    with self.assertRaises(TypeError):
      self.point0.y = '420'
    with self.assertRaises(TypeError):
      self.point0.z = '80085'
    #  Point 1
    with self.assertRaises(TypeError):
      self.point1.x = '69'
    with self.assertRaises(TypeError):
      self.point1.y = '420'
    with self.assertRaises(TypeError):
      self.point1.z = '1337'
    #  Point 2
    with self.assertRaises(TypeError):
      self.point2.x = '420'
    with self.assertRaises(TypeError):
      self.point2.y = '1337'
    with self.assertRaises(TypeError):
      self.point2.z = '69'

  def test_virtuals(self) -> None:
    """Testing virtual attributes."""
    expectedVolume = (4.0 / 3.0) * pi * self.radius ** 3
    actualVolume = self.sphere.volume
    self.assertAlmostEqual(actualVolume, expectedVolume)

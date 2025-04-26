"""TestFlexBox tests the FlexBox class."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase
from math import atan2, pi
from random import random

from worktoy.attr import FlexBox, Field
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

  x = FlexBox[float](0.0)
  y = FlexBox[float](0.0)
  z = FlexBox[float](0.0)

  @classmethod
  def randomSample(cls, *args) -> Self:
    """Creates a random sample """
    minVal, maxVal = None, None
    if len(args) > 1:
      minVal, maxVal = args[:2]
    elif len(args) == 1:
      minVal, maxVal = [0, *args, ][:2]
    else:
      minVal, maxVal = 0, 1
    x0 = random() * (maxVal - minVal) + minVal
    x1 = random() * (maxVal - minVal) + minVal
    x2 = random() * (maxVal - minVal) + minVal
    return cls(x0, x1, x2)

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

  def __neg__(self, ) -> Point3d:
    """Return the negation of the Point3d object."""
    cls = type(self)
    return cls(-self.x, -self.y, -self.z)

  def _resolveOther(self, other: Any) -> Self:
    """Resolve the other object."""
    cls = type(self)
    if isinstance(other, cls):
      return other
    if isinstance(other, (tuple, list)):
      try:
        return cls(*other)
      except TypeError:
        return NotImplemented
    return NotImplemented

  def __eq__(self, other: object) -> bool:
    """Compare the Point3d object with another object."""
    other = self._resolveOther(other)
    if other is NotImplemented:
      return False
    cls = type(self)
    if isinstance(other, cls):
      if self.x != other.x:
        return False
      if self.y != other.y:
        return False
      if self.z != other.z:
        return False
      return True
    return False

  def __hash__(self, ) -> int:
    """Return the hash of the Point3d object."""
    return hash((self.x, self.y, self.z))


class Sphere(BaseObject):
  """Represents a spatial sphere. """

  #  Real Attributes
  radius = FlexBox[float](1.0)
  center = FlexBox[Point3d](Point3d(0.0, 0.0, 0.0))

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

  @overload(tuple)
  @overload(list)
  def __init__(self, other: tuple) -> None:
    """Initialize the Sphere object."""
    self.__init__(*other[0])

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


class TestFlexBox(TestCase):
  """TestFlexBox tests the FlexBox class."""

  def setUp(self) -> None:
    """
    Set up the test case by creating a Sphere object.
    """
    self.center = Point3d(0.0, 0.0, 0.0)
    self.radius = 69
    self.sphere = Sphere(self.radius, self.center)
    self.point0 = Point3d(0, 0, 0, )
    self.point1 = Point3d(69, 420, 1337)
    self.point2 = Point3d(420, 1337, 80085)

  def test_init(self, ) -> None:
    """Tests that AttriBox owning classes correctly initializes"""
    #  Test the default constructor
    self.assertAlmostEqual(self.center, self.sphere.center)
    self.assertAlmostEqual(self.radius, self.sphere.radius)
    self.assertEqual(self.point0.x, 0.0)
    self.assertEqual(self.point0.y, 0.0)
    self.assertEqual(self.point0.z, 0.0)
    self.assertEqual(self.point1.x, 69.0)
    self.assertEqual(self.point1.y, 420.0)
    self.assertEqual(self.point1.z, 1337.0)
    self.assertEqual(self.point2.x, 420.0)
    self.assertEqual(self.point2.y, 1337.0)
    self.assertEqual(self.point2.z, 80085)
    self.assertEqual(self.sphere.radius, self.radius)
    self.assertEqual(self.sphere.center.x, self.center.x)
    self.assertEqual(self.sphere.center.y, self.center.y)
    self.assertEqual(self.sphere.center.z, self.center.z)

  def test_set(self) -> None:
    """
    Tests that AttriBox owning classes correctly sets the value of the
    attribute.
    """
    #  Point 0
    newPoint0 = Point3d.randomSample(69, 420)
    self.point0 = newPoint0
    self.assertAlmostEqual(self.point0.x, newPoint0.x)
    self.assertAlmostEqual(self.point0.y, newPoint0.y)
    self.assertAlmostEqual(self.point0.z, newPoint0.z)
    self.assertAlmostEqual(self.point0, newPoint0)
    #  Point 1
    newPoint1 = Point3d.randomSample(69, 420)
    self.point1 = newPoint1
    self.assertAlmostEqual(self.point1.x, newPoint1.x)
    self.assertAlmostEqual(self.point1.y, newPoint1.y)
    self.assertAlmostEqual(self.point1.z, newPoint1.z)
    self.assertAlmostEqual(self.point1, newPoint1)
    #  Point 2
    newPoint2 = Point3d.randomSample(69, 420)
    self.point2 = newPoint2
    self.assertAlmostEqual(self.point2.x, newPoint2.x)
    self.assertAlmostEqual(self.point2.y, newPoint2.y)
    self.assertAlmostEqual(self.point2.z, newPoint2.z)
    #  Sphere
    newCenter = Point3d.randomSample(69, 420)
    newRadius = random() * 100
    self.sphere.center = newCenter
    self.sphere.radius = newRadius
    self.assertAlmostEqual(self.sphere.center.x, newCenter.x)
    self.assertAlmostEqual(self.sphere.center.y, newCenter.y)
    self.assertAlmostEqual(self.sphere.center.z, newCenter.z)
    self.assertAlmostEqual(self.sphere.center, newCenter)
    self.assertAlmostEqual(self.sphere.radius, newRadius)

  def test_flex_set(self, ) -> None:
    """Testing that FlexBox attributes can apply type casting when setting
    to the wrong types."""
    #  Sphere
    newPoint0Tuple = (random(), 10 * random(), 100 * random())
    self.sphere.center = newPoint0Tuple
    if TYPE_CHECKING:
      assert isinstance(self.sphere.center, Point3d)
    self.assertAlmostEqual(self.sphere.center.x, newPoint0Tuple[0])
    self.assertAlmostEqual(self.sphere.center.y, newPoint0Tuple[1])
    self.assertAlmostEqual(self.sphere.center.z, newPoint0Tuple[2])
    newRadius = '%.3f' % (random() * 100)
    self.sphere.radius = newRadius
    self.assertAlmostEqual(self.sphere.radius, float(newRadius))

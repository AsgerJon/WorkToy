"""TestFastObject tests the FastObject class. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from random import random
from time import perf_counter_ns
from unittest import TestCase

from worktoy.base import FastObject, overload, BaseObject
from worktoy.desc import AttriBox


class PlanePoint(FastObject):
  """PlanePoint inherits from FastObject and will be further subclassed. """

  x = AttriBox[float](0)
  y = AttriBox[float](0)

  @overload(float, float)
  def __init__(self, x: float, y: float) -> None:
    self.x = x
    self.y = y

  @overload(float)
  def __init__(self, x: float) -> None:
    self.__init__(x, 0)

  @overload()
  def __init__(self) -> None:
    self.__init__(0, 0)


class SpacePoint(PlanePoint):
  """SomeClass is a class that inherits from FastObject."""

  z = AttriBox[float](0)

  @overload(float, float, float)
  def __init__(self, x: float, y: float, z: float) -> None:
    self.x = x
    self.y = y
    self.z = z

  @overload(float, float)
  def __init__(self, x: float, y: float) -> None:
    self.__init__(x, y, 0)

  @overload(float)
  def __init__(self, x: float) -> None:
    self.__init__(x, 0, 0)

  @overload()
  def __init__(self) -> None:
    self.__init__(0, 0, 0)


class ClassicPoint(BaseObject):
  """This class inherits from BaseObject do not leverage __slots__ for
  performance. """

  x = AttriBox[float](0)
  y = AttriBox[float](0)
  z = AttriBox[float](0)

  @overload(float, float, float)
  def __init__(self, x: float, y: float, z: float) -> None:
    self.x = x
    self.y = y
    self.z = z

  @overload(float, float)
  def __init__(self, x: float, y: float) -> None:
    self.__init__(x, y, 0)

  @overload(float)
  def __init__(self, x: float) -> None:
    self.__init__(x, 0, 0)

  @overload()
  def __init__(self) -> None:
    self.__init__(0, 0, 0)


def pointFactory(cls: type) -> object:
  """Creates a point object from a class. """
  return cls(random(), random(), random())


def tupleFactory(n: int, cls: type) -> tuple:
  """tupleFactory creates a class with n slots. """
  return tuple(pointFactory(cls) for _ in range(n))


class FastCloud(FastObject):
  """FastCloud contains n points with __slots__ for performance. """

  points = AttriBox[tuple]()

  def __init__(self, n: int = None) -> None:
    n = 1000 if n is None else n
    self.points = tupleFactory(n, SpacePoint)


class BaseCloud(BaseObject):
  """BaseCloud contains n points without __slots__ for performance. """

  points = AttriBox[tuple]()

  def __init__(self, n: int = None) -> None:
    n = 1000 if n is None else n
    self.points = tupleFactory(n, ClassicPoint)


def yoloPi(cls: type, n: int = None, **kwargs) -> float:
  """Computes pi from point clouds. """

  tic = perf_counter_ns()
  n = 1000 if n is None else n
  cloud = cls(n)
  radii = tuple(p.x ** 2 + p.y ** 2 + p.z ** 2 for p in cloud.points)
  inner = sum(1 for r in radii if r <= 1)
  piIsh = 6 * inner / n
  toc = perf_counter_ns()
  if not kwargs.get('verbose', False):
    return toc - tic
  deltaTime = float(toc - tic)
  log1k = 0
  while deltaTime > 1000:
    deltaTime //= 1000
    log1k += 1
  unitName = ['ns', 'µs', 'ms', 's'][log1k]
  deltaStr = '%.f %s' % (deltaTime, unitName)
  info = """Using class '%s' with '%d' points took '%s' to estimate pi 
  as '%.12f'""" % (cls.__name__, n, deltaStr, piIsh)
  print(info)
  return toc - tic


class TestFastObject(TestCase):
  """TestFastObject tests the FastObject class. """

  def setUp(self) -> None:
    """Sets up the test class"""
    self.planePoint = PlanePoint(69, 420)
    self.spacePoint = SpacePoint(69, 420, 1337)

  def testNamespace(self, ) -> None:
    """Testing that the PlanePoint class correctly identifies x and y as
    attributes. """
    nameSpace = getattr(PlanePoint, '__slots__', None)
    self.assertIsInstance(nameSpace, list)
    for name in ['x', 'y']:
      self.assertIn(name, nameSpace)

  def test_init(self, ) -> None:
    """Tests that the __init__ methods work correctly. """
    self.assertEqual(self.planePoint.x, 69)
    self.assertEqual(self.planePoint.y, 420)
    self.assertEqual(self.spacePoint.x, 69)
    self.assertEqual(self.spacePoint.y, 420)
    self.assertEqual(self.spacePoint.z, 1337)

  def test_positional_args(self) -> None:
    """Tests that SpacePoint support any number of positional arguments"""

    point2D = PlanePoint()  # No arguments
    point3D = SpacePoint()  # No arguments
    self.assertEqual(point2D.x, 0)
    self.assertEqual(point2D.y, 0)
    self.assertEqual(point3D.x, 0)
    self.assertEqual(point3D.y, 0)
    self.assertEqual(point3D.z, 0)

    point2D = PlanePoint(1)  # One argument
    point3D = SpacePoint(1)  # One argument
    self.assertEqual(point2D.x, 1)
    self.assertEqual(point2D.y, 0)
    self.assertEqual(point3D.x, 1)
    self.assertEqual(point3D.y, 0)
    self.assertEqual(point3D.z, 0)

    point2D = PlanePoint(1, 2)  # Two arguments
    point3D = SpacePoint(1, 2)  # Two arguments
    self.assertEqual(point2D.x, 1)
    self.assertEqual(point2D.y, 2)
    self.assertEqual(point3D.x, 1)
    self.assertEqual(point3D.y, 2)
    self.assertEqual(point3D.z, 0)

    point3D = SpacePoint(1, 2, 3)  # Three arguments
    self.assertEqual(point3D.x, 1)
    self.assertEqual(point3D.y, 2)
    self.assertEqual(point3D.z, 3)

  def test_slots(self, ) -> None:
    """Testing that __slots__ are correctly implemented. """
    planeSlots = getattr(self.planePoint, '__slots__', None)
    spaceSlots = getattr(self.spacePoint, '__slots__', None)
    self.assertIsInstance(planeSlots, list)
    self.assertIsInstance(spaceSlots, list)
    for name in ['x', 'y']:
      self.assertIn(name, planeSlots)
      self.assertIn(name, spaceSlots)
    self.assertIn('z', spaceSlots)

  def test_timing(self, ) -> None:
    """Testing that FastObject is in fact faster than BaseObject,
    by at least a factor of 10. """
    fastTime = yoloPi(FastCloud, 10000)
    baseTime = yoloPi(BaseCloud, 10000)
    self.assertLess(fastTime * 10, baseTime)

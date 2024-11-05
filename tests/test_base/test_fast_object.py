"""TestFastObject tests the FastObject class. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from random import random, randint
from time import perf_counter_ns
from unittest import TestCase

from worktoy.base import FastObject, overload, BaseObject
from worktoy.desc import AttriBox
from worktoy.text import monoSpace


class PlanePoint(FastObject):
  """PlanePoint inherits from FastObject and will be further subclassed.
  """

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
    pass


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

  def __str__(self) -> str:
    """String representation."""
    return self.__class__.__name__

  def __repr__(self, ) -> str:
    """Code representation."""
    return self.__class__.__name__

  x = AttriBox[int](69)
  y = AttriBox[int](420)
  z = AttriBox[int](1337)
  a = AttriBox[int](80085)
  b = AttriBox[int](133769)
  c = AttriBox[int](4201337)


class BaseCloud(BaseObject):
  """BaseCloud contains n points without __slots__ for performance. """

  def __str__(self) -> str:
    """String representation."""
    return self.__class__.__name__

  def __repr__(self, ) -> str:
    """Code representation."""
    return self.__class__.__name__

  x = AttriBox[int](69)
  y = AttriBox[int](420)
  z = AttriBox[int](1337)
  a = AttriBox[int](80085)
  b = AttriBox[int](133769)
  c = AttriBox[int](4201337)


def dataGen(n: int = None) -> tuple[int, ...]:
  """Generates a tuple of n random integers. """
  if n is None:
    return tuple(randint(0, 255) for _ in range(1024))
  return tuple(randint(0, 255) for _ in range(n))


def yoloPi(cls: type, n: int = None, **kwargs) -> float:
  """Computes pi from point clouds. """
  data = dataGen(n)
  self = cls(**kwargs)
  tic = perf_counter_ns()
  for (i, v) in enumerate(data):
    if i % 6 == 0:
      self.x = max(self.x, v)
    elif i % 6 == 1:
      self.y = max(self.y, v)
    elif i % 6 == 2:
      self.z = max(self.z, v)
    elif i % 6 == 3:
      self.a = max(self.a, v)
    elif i % 6 == 4:
      self.b = max(self.b, v)
    elif i % 6 == 5:
      self.c = max(self.c, v)
  toc = perf_counter_ns()
  return toc - tic


class NoInit(FastObject):
  """This class has no init itself!"""
  pass


class SomeInit(FastObject):
  """This one does!"""

  def __init__(self, *args, **kwargs) -> None:
    """LOL"""
    pass


class TestFastObject(TestCase):
  """TestFastObject tests the FastObject class. """

  def setUp(self) -> None:
    """Sets up the test class"""
    self.planePoint = PlanePoint(69, 420)
    self.spacePoint = SpacePoint(69, 420, 1337)

  def test_init_presence(self) -> None:
    """Testing that the namespace objects can detect the presence of an
    init method."""

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
    n = 100000
    fastTime = yoloPi(FastCloud, n) * 1e-06
    baseTime = yoloPi(BaseCloud, n) * 1e-06
    self.assertLess(fastTime * 10, baseTime)

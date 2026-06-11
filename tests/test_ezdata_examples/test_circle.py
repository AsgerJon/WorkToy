"""
TestCircle subclasses 'EZExamplesTest' from the
'tests.test_ezdata_examples' package and provides tests for the
'Circle' class from the 'tests.test_ezdata.examples' package.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from math import pi

from tests.test_ezdata.examples import Point2D, Circle, FullName
from worktoy.waitaminute.ezdata import KwargsOnlyException
from . import EZExamplesTest


class TestCircle(EZExamplesTest):
  """
  TestCircle subclasses 'EZExamplesTest' from the
  'tests.test_ezdata_examples' package and provides tests for the
  'Circle' class from the 'tests.test_ezdata.examples' package.
  """

  def test_init(self, ) -> None:
    """
    This method tests initialization of 'Circle' with different arguments.
    """
    circle = Circle()
    self.assertAlmostEqual(circle.center.x, 0.)
    self.assertAlmostEqual(circle.center.y, 0.)
    self.assertAlmostEqual(circle.radius, 1.)
    center = Point2D(69, 420)
    circle = Circle(center=center)
    self.assertAlmostEqual(circle.center.x, 69)
    self.assertAlmostEqual(circle.center.y, 420)
    self.assertAlmostEqual(circle.radius, 1.)
    circle = Circle(center=Point2D(-69, -420), radius=1337)
    self.assertAlmostEqual(circle.center.x, -69)
    self.assertAlmostEqual(circle.center.y, -420)
    self.assertAlmostEqual(circle.radius, 1337)

  def test_bad_init(self, ) -> None:
    """
    This method tests that initialization of 'Circle' with bad arguments
    raises appropriate exceptions.
    """
    point = Point2D(1, 2)
    distance = 3
    with self.assertRaises(KwargsOnlyException) as context:
      Circle(point, distance)
    e = context.exception
    self.assertIs(e.cls, Circle)
    self.assertEqual(e.argCount, 2)
    self.assertEqual(str(e), repr(e))

  def test_str(self, ) -> None:
    """
    This method tests the string representation of 'Circle' instances.
    """
    circle = Circle(center=Point2D(1, 2), radius=3)
    circleStr = str.replace(str(circle), ' ', '')
    self.assertTrue(str.startswith(circleStr, '<Circle:'))
    self.assertTrue(str.endswith(circleStr, '>'))
    self.assertIn("""center=Point2D(""", circleStr)
    self.assertIn("""radius=""", circleStr)

  def test_repr(self, ) -> None:
    """
    This method tests the official string representation of 'Circle'
    instances.
    """
    circle = Circle(center=Point2D(1, 2), radius=3)
    circleRepr = str.replace(repr(circle), ' ', '')
    self.assertTrue(str.startswith(circleRepr, 'Circle('))
    self.assertTrue(str.endswith(circleRepr, ')'))
    self.assertIn("""center=Point2D(""", circleRepr)
    self.assertIn("""radius=""", circleRepr)

  def test_equal(self, ) -> None:
    """
    This method tests equality of 'Circle' instances.
    """
    circle1 = Circle(center=Point2D(1, 2), radius=3)
    circle2 = Circle(center=Point2D(1, 2), radius=3)
    circle3 = Circle(center=Point2D(4, 5), radius=6)
    self.assertEqual(circle1, circle2)
    self.assertNotEqual(circle1, circle3)
    self.assertNotEqual(circle1, 'never')
    self.assertNotEqual(circle2, 'gonna')
    self.assertNotEqual(circle3, 'give')
    self.assertNotEqual(circle1, FullName('you', 'up'))

  def test_contains(self, ) -> None:
    """
    This method tests the 'contains' method of 'Circle' instances.
    """
    origin = Point2D(0, 0)
    p0 = Point2D(0.2, 0.2)
    p1 = Point2D(0.5, 0.5)
    p2 = Point2D(69, 420)
    circle = Circle(center=origin, radius=1)
    self.assertIn(origin, circle)
    self.assertIn(p0, circle)
    self.assertIn(p1, circle)
    self.assertNotIn(p2, circle)
    bigCircle = Circle(center=origin, radius=100)
    self.assertIn(origin, bigCircle)
    self.assertIn(p0, bigCircle)
    self.assertIn(p1, bigCircle)
    self.assertIn(circle, bigCircle)
    self.assertNotIn(p2, bigCircle)
    self.assertNotIn(object(), circle)
    self.assertNotIn(object(), bigCircle)

  def test_getitem(self) -> None:
    """
    This method tests the '__getitem__' method of 'Circle' instances.
    """
    origin = Point2D(0, 0)
    unitRadius = 1
    unitCircle = Circle(center=origin, radius=unitRadius)
    self.randomFloat.colCount = 8
    for item in self.randomFloat.row:
      expectedPoint = unitCircle[item]
      actualPoint = unitCircle[item + 2 * pi]
      self.assertAlmostEqual(expectedPoint.x, actualPoint.x)
      self.assertAlmostEqual(expectedPoint.y, actualPoint.y)
      expectedDistanceSquared = 2
      actualDistance = expectedPoint @ unitCircle[item + pi / 2]
      self.assertAlmostEqual(expectedDistanceSquared, actualDistance ** 2)
      actualDistance = expectedPoint @ unitCircle[item + pi]
      self.assertAlmostEqual(expectedDistanceSquared, actualDistance)

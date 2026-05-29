"""
TestPoint2D subclasses 'EZExamplesTest' from the
'tests.test_ezdata.examples._ez_examples_test' package and provides tests for
the 'Point2D' class from the 'tests.test_ezdata.examples' package.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING
import random

from tests.test_ezdata.examples import Point2D
from worktoy.desc import AttriBox
from worktoy.work_test.samplers import BaseSampler
from . import EZExamplesTest

if TYPE_CHECKING:  # pragma: no cover
  pass


class Point2DSampler(BaseSampler):
  """
  Point2DSampler subclasses 'BaseSampler' from the
  'worktoy.work_test.samplers' package and provides a sampler for
  'Point2D' instances.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Fallback Variables
  __fallback_col_count__: int = 8
  __fallback_row_count__: int = 8

  #  Public Variables
  xMin = AttriBox[float](-100)
  xMax = AttriBox[float](100)
  yMin = AttriBox[float](-100)
  yMax = AttriBox[float](100)

  def _getValueType(self, ) -> type:
    """
    This method returns the type of values sampled by this sampler, which is
    'Point2D'.
    """
    return Point2D

  def _getItem(self, ) -> Point2D:
    """
    This method returns a new 'Point2D' instance with random coordinates.
    """
    x = random.uniform(self.xMin, self.xMax)
    y = random.uniform(self.yMin, self.yMax)
    return Point2D(x, y)


class TestPoint2D(EZExamplesTest):
  """
  TestPoint2D subclasses 'EZExamplesTest' from the
  'tests.test_ezdata.examples._ez_examples_test' package and provides
  tests for
  the 'Point2D' class from the 'tests.test_ezdata.examples' package.
  """

  point2DSampler = Point2DSampler()

  def setUp(self) -> None:
    """
    This method sets up the test environment for each test method by
    initializing a 'Point2DSampler' instance.
    """
    self.randomFloat.minVal = -100
    self.randomFloat.maxVal = 100
    self.randomFloat.rowCount = 8
    self.randomFloat.colCount = 8

  def test_init(self, ) -> None:
    """
    This method tests initialization of 'Point2D' with different number of
    arguments.
    """
    origin = Point2D()
    i = Point2D(1)
    j = Point2D(0, 1)
    self.assertFalse(origin.x)
    self.assertFalse(origin.y)
    self.assertFalse(origin)
    self.assertTrue(i.x)
    self.assertFalse(i.y)
    self.assertFalse(j.x)
    self.assertTrue(j.y)

  def test_equal(self, ) -> None:
    """
    This method tests equality and arithmetic operations of 'Point2D'
    instances.
    """
    origin = Point2D()
    i = Point2D(1)
    j = Point2D(0, 1)
    i2 = Point2D(1, 0)

    self.assertEqual(origin, Point2D())
    self.assertEqual(i, i2)
    self.assertNotEqual(i, j)

  def test_unary(self, ) -> None:
    """
    This method tests unary operations of 'Point2D' instances.
    """
    for point in self.point2DSampler.row:
      self.assertEqual(+point, point)
      self.assertEqual(-(-point), point)
      self.assertFalse(-point + point)

  def test_add(self, ) -> None:
    """
    This method tests addition of 'Point2D' instances.
    """
    for p in self.point2DSampler.row:
      for q in self.point2DSampler.row:
        self.assertEqual(p + q, q + p)
        pq = p + q
        expectedX = p.x + q.x
        expectedY = p.y + q.y
        self.assertAlmostEqual(pq.x, expectedX)
        self.assertAlmostEqual(pq.y, expectedY)

  def test_sub(self, ) -> None:
    """
    This method tests subtraction of 'Point2D' instances.
    """
    for p in self.point2DSampler.row:
      self.assertFalse(p - p)
      for q in self.point2DSampler.row:
        pq = p - q
        expectedX = p.x - q.x
        expectedY = p.y - q.y
        self.assertAlmostEqual(pq.x, expectedX)
        self.assertAlmostEqual(pq.y, expectedY)

  def test_matmul(self, ) -> None:
    """
    This method tests the matrix multiplication operator of 'Point2D'
    instances,
    which computes the distance between two points.
    """
    for p in self.point2DSampler.row:
      for q in self.point2DSampler.row:
        pq = p @ q
        expected = ((p.x - q.x) ** 2 + (p.y - q.y) ** 2)
        actual = pq ** 2
        self.assertAlmostEqual(expected, actual)
      for scalar in self.randomFloat.row:
        ps = p @ scalar
        expectedX = p.x * scalar
        expectedY = p.y * scalar
        self.assertAlmostEqual(ps.x, expectedX)
        self.assertAlmostEqual(ps.y, expectedY)

  def test_mul(self, ) -> None:
    """
    This method tests the multiplication operator of 'Point2D' instances,
    which computes the dot product of two points or the scalar multiplication
    of a point.
    """
    for p in self.point2DSampler.row:
      for q in self.point2DSampler.row:
        pq = p * q
        expected = p.x * q.x + p.y * q.y
        self.assertAlmostEqual(pq, expected)
      for scalar in self.randomFloat.row:
        ps = p * scalar
        sp = scalar * p  # test reflected operator
        self.assertEqual(ps, sp)
        expectedX = p.x * scalar
        expectedY = p.y * scalar
        self.assertAlmostEqual(ps.x, expectedX)
        self.assertAlmostEqual(ps.y, expectedY)

  def test_arithmetic_not_implemented(self, ) -> None:
    """
    This method tests that arithmetic operations of 'Point2D' instances with
    incompatible types return 'NotImplemented'.
    """
    origin = Point2D()
    # noinspection PyTypeChecker
    self.assertIs(Point2D.__add__(origin, (69, 420)), NotImplemented)
    # noinspection PyTypeChecker
    self.assertIs(Point2D.__sub__(origin, (69, 420)), NotImplemented)
    # noinspection PyTypeChecker
    self.assertIs(Point2D.__matmul__(origin, (69, 420)), NotImplemented)
    # noinspection PyTypeChecker
    self.assertIs(Point2D.__mul__(origin, (69, 420)), NotImplemented)
    # noinspection PyTypeChecker
    self.assertIs(Point2D.__mul__(origin, 'scalar'), NotImplemented)

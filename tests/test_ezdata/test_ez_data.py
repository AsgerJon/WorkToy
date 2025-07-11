"""
TestEZData - Test the EZData class.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from . import EZTest
from worktoy.ezdata import EZData

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  pass


class Point2D(EZData):
  """Point2D represents a point in 2D space."""

  x = 69
  y = 420


class Point3D(Point2D):
  """Point3D represents a point in 3D space."""

  z = 1337


class TestEZData(EZTest):
  """TestEZData - Test the EZData class."""

  def setUp(self) -> None:
    """Set up the test case."""
    self.point2d_0 = Point2D()
    self.point2d_1 = Point2D(1)
    self.point2d_2 = Point2D(1, 2)
    self.point2d_3 = Point2D(1, 2, x=3)
    self.point2d_4 = Point2D(1, 2, x=3, y=4)
    self.point2d_5 = Point2D(1, x=5)
    self.point2d_6 = Point2D(1, y=6)
    self.point2d_7 = Point2D(x=7, y=8, )
    self.point3d_0 = Point3D()
    self.point3d_1 = Point3D(1)
    self.point3d_2 = Point3D(1, 2)
    self.point3d_3 = Point3D(1, 2, 3)
    self.point3d_4 = Point3D(1, 2, 3, x=4)
    self.point3d_5 = Point3D(1, 2, 3, x=4, y=5)
    self.point3d_6 = Point3D(1, 2, 3, y=6)
    self.point3d_7 = Point3D(1, 2, 3, x=4, y=5, z=6)

  def test_init(self, ) -> None:
    """Test the initialization of EZData."""
    self.assertIsInstance(self.point2d_0, EZData)
    self.assertIsInstance(self.point3d_0, EZData)
    self.assertEqual(self.point2d_0.x, 69)
    self.assertEqual(self.point2d_0.y, 420)
    self.assertEqual(self.point2d_1.x, 1)
    self.assertEqual(self.point2d_1.y, 420)
    self.assertEqual(self.point2d_2.x, 1)
    self.assertEqual(self.point2d_2.y, 2)
    self.assertEqual(self.point2d_3.x, 3)
    self.assertEqual(self.point2d_3.y, 2)
    self.assertEqual(self.point2d_4.x, 3)
    self.assertEqual(self.point2d_4.y, 4)
    self.assertEqual(self.point2d_5.x, 5)
    self.assertEqual(self.point2d_5.y, 420)
    self.assertEqual(self.point2d_6.x, 1)
    self.assertEqual(self.point2d_6.y, 6)
    self.assertEqual(self.point2d_7.x, 7)
    self.assertEqual(self.point2d_7.y, 8)
    self.assertEqual(self.point3d_0.x, 69)
    self.assertEqual(self.point3d_0.y, 420)
    self.assertEqual(self.point3d_0.z, 1337)
    self.assertEqual(self.point3d_1.x, 1)
    self.assertEqual(self.point3d_1.y, 420)
    self.assertEqual(self.point3d_1.z, 1337)
    self.assertEqual(self.point3d_2.x, 1)
    self.assertEqual(self.point3d_2.y, 2)
    self.assertEqual(self.point3d_2.z, 1337)
    self.assertEqual(self.point3d_3.x, 1)
    self.assertEqual(self.point3d_3.y, 2)
    self.assertEqual(self.point3d_3.z, 3)
    self.assertEqual(self.point3d_4.x, 4)
    self.assertEqual(self.point3d_4.y, 2)
    self.assertEqual(self.point3d_4.z, 3)
    self.assertEqual(self.point3d_5.x, 4)
    self.assertEqual(self.point3d_5.y, 5)
    self.assertEqual(self.point3d_5.z, 3)
    self.assertEqual(self.point3d_6.x, 1)
    self.assertEqual(self.point3d_6.y, 6)
    self.assertEqual(self.point3d_6.z, 3)
    self.assertEqual(self.point3d_7.x, 4)
    self.assertEqual(self.point3d_7.y, 5)
    self.assertEqual(self.point3d_7.z, 6)

  def test_eq(self) -> None:
    """Test the equality of EZData instances."""
    self.assertEqual(self.point2d_0, Point2D())
    self.assertNotEqual(self.point2d_0, Point2D(1))
    self.assertEqual(self.point3d_0, Point3D())
    self.assertNotEqual(self.point3d_0, Point3D(1))

  def test_ad_hoc(self) -> None:
    """Test ad-hoc EZData instances."""

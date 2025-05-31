"""
TestEZData - Test the EZData class.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.ezdata import EZData, EZMeta

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False


class Point2D(EZData):
  """Point2D represents a point in 2D space."""

  x = 69
  y = 420


class Point3D(EZData):
  """Point3D represents a point in 3D space."""

  x = 69
  y = 420
  z = 1337


class TestEZData(TestCase):
  """TestEZData - Test the EZData class."""

  def setUp(self) -> None:
    """Set up the test case."""
    self.point2d_0 = Point2D()
    self.point2d_1 = Point2D(0, 80085)
    self.point3d_0 = Point3D()
    self.point3d_1 = Point3D(0, 1337, 80085)

  def test_values(self) -> None:
    """Test the values of the EZData classes."""
    self.assertEqual(self.point2d_0.x, 69)
    self.assertEqual(self.point2d_0.y, 420)
    self.assertEqual(self.point3d_0.x, 69)
    self.assertEqual(self.point3d_0.y, 420)
    self.assertEqual(self.point3d_0.z, 1337)

  def test_accessor(self, ) -> None:
    """Test the accessor of the EZData classes."""
    self.assertEqual(self.point2d_0.x, 69)
    self.assertEqual(self.point2d_0.y, 420)
    self.point2d_0.x = 0
    self.point2d_0.y = 80085
    self.assertEqual(self.point2d_0.x, 0)
    self.assertEqual(self.point2d_0.y, 80085)

    self.assertEqual(self.point3d_0.x, 69)
    self.assertEqual(self.point3d_0.y, 420)
    self.assertEqual(self.point3d_0.z, 1337)

  def test_get_set_item(self) -> None:
    """Tests the get and set item methods of the EZData classes."""
    self.point3d_0['x'] = 0
    self.point3d_0['y'] = 1337
    self.point3d_0['z'] = 80085

    self.assertEqual(self.point3d_0['x'], 0)
    self.assertEqual(self.point3d_0['y'], 1337)
    self.assertEqual(self.point3d_0['z'], 80085)

  def test_inline(self, ) -> None:
    """Tests creation of EZData classes inline."""

    class Outer:
      """Outer class for inline testing."""
      P2D = EZData(x=69, y=420)
      p2D = None

      def __init__(self, x: int, y: int) -> None:
        """Initialize the Outer class."""
        self.p2D = self.P2D(x, y)

      def __str__(self, ) -> str:
        """Returns the string representation of the Outer class."""
        return """%s[p2D=%s]""" % (type(self).__name__, self.p2D,)

    self.assertIsInstance(Outer.P2D, EZMeta)
    self.assertIsInstance(Outer(69, 420), Outer)
    self.assertIsInstance(Outer(69, 420).p2D, Outer.P2D)

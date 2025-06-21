"""
TestAttriBox tests the AttriBox class.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.waitaminute import ReadOnlyError, ProtectedError
from worktoy.waitaminute import TypeException

from worktoy.attr import AttriBox
from worktoy.static.zeroton import THIS
from worktoy.text import stringList

from . import PlanePoint, PlaneCircle

try:
  from typing import TYPE_CHECKING
except ImportError:  # pragma: no cover
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Self


class TestAttriBox(TestCase):
  """TestAttriBox tests the AttriBox class."""

  def setUp(self) -> None:
    """Set up the test case."""
    self.point1 = PlanePoint(.80085, .1337)
    self.point2 = PlanePoint(69, 420)
    self.point3 = PlanePoint(1337 + 80085j)
    self.circle1 = PlaneCircle(self.point1, 69.0)
    self.circle2 = PlaneCircle(self.point2, 420)

  def test_boxes(self, ) -> None:
    """Test the AttriBox class."""
    self.assertIsInstance(PlanePoint.x, AttriBox)
    self.assertIsInstance(PlanePoint.y, AttriBox)
    self.assertIsInstance(PlaneCircle.center, AttriBox)
    self.assertIsInstance(PlaneCircle.radius, AttriBox)

  def test_init(self, ) -> None:
    """Test the AttriBox class initialization."""
    self.assertIsInstance(self.point1, PlanePoint)
    self.assertIsInstance(self.point2, PlanePoint)
    self.assertIsInstance(self.point3, PlanePoint)
    self.assertIsInstance(self.circle1, PlaneCircle)
    self.assertIsInstance(self.circle2, PlaneCircle)

  def test_good_get(self, ) -> None:
    """Test getting values. """
    self.assertEqual(self.point1.x, .80085)
    self.assertEqual(self.point1.y, .1337)
    self.assertEqual(self.point2.x, 69)
    self.assertEqual(self.point2.y, 420)
    self.assertEqual(self.point3.x, 1337)
    self.assertEqual(self.point3.y, 80085)
    self.assertEqual(self.circle1.center.x, .80085)
    self.assertEqual(self.circle1.center.y, .1337)
    self.assertEqual(self.circle1.radius, 69.0)
    self.assertEqual(self.circle2.center.x, 69)
    self.assertEqual(self.circle2.center.y, 420)
    self.assertEqual(self.circle2.radius, 420)

  def test_good_set(self, ) -> None:
    """Test setting values."""
    self.assertEqual(self.point1.x, .80085)
    self.assertEqual(self.point1.y, .1337)
    self.point1.x = 69.
    self.point1.y = 420
    self.assertEqual(self.point1.x, 69.)
    self.assertEqual(self.point1.y, 420)

    self.assertEqual(self.point2.x, 69.)
    self.assertEqual(self.point2.y, 420.)
    self.point2.x = 1337
    self.point2.y = 80085
    self.assertEqual(self.point2.x, 1337)
    self.assertEqual(self.point2.y, 80085)

    self.assertEqual(self.point3.x, 1337)
    self.assertEqual(self.point3.y, 80085)
    self.point3.x = 0.80085
    self.point3.y = 0.1337
    self.assertEqual(self.point3.x, 0.80085)
    self.assertEqual(self.point3.y, 0.1337)

    self.assertEqual(self.circle1.center.x, self.point1.x)
    self.assertEqual(self.circle1.center.y, self.point1.y)
    self.assertEqual(self.circle1.radius, 69.0)
    self.circle1.center = self.point2
    self.circle1.radius = 420
    self.assertEqual(self.circle1.center.x, self.point2.x)
    self.assertEqual(self.circle1.center.y, self.point2.y)
    self.assertEqual(self.circle1.radius, 420)

    self.assertEqual(self.circle2.center.x, self.point2.x)
    self.assertEqual(self.circle2.center.y, self.point2.y)
    self.assertEqual(self.circle2.radius, 420)
    self.circle2.center = self.point3
    self.circle2.radius = 69.0
    self.assertEqual(self.circle2.center.x, self.point3.x)
    self.assertEqual(self.circle2.center.y, self.point3.y)
    self.assertEqual(self.circle2.radius, 69.0)

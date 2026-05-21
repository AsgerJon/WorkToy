"""
TestExamples subclasses 'KeeTest' from the 'tests.test_keenum' package and
provides tests for various classes from the 'tests.test_keenum.examples'
package.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from .examples import RGB, Point3D
from . import KeeTest

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestExamples(KeeTest):
  """
  TestExamples subclasses 'KeeTest' from the 'tests.test_keenum' package and
  provides tests for various classes from the 'tests.test_keenum.examples'
  package.
  """

  def test_rgb_init(self, ) -> None:
    """
    This method tests initialization of 'RGB' with different number of
    arguments.
    """

    black = RGB()
    red = RGB(255)
    yellow = RGB(255, 255)
    white = RGB(255, 255, 255)
    self.assertFalse(black.r)
    self.assertFalse(black.g)
    self.assertFalse(black.b)
    self.assertFalse(red.g)
    self.assertFalse(red.b)
    self.assertFalse(yellow.b)
    self.assertEqual(white.r, yellow.r)
    self.assertEqual(white.g, yellow.g)
    self.assertEqual(white.r, red.r)

  def test_point_3d_init(self, ) -> None:
    """
    This method tests initialization of 'Point3D' with different number of
    arguments.
    """

    origin = Point3D()
    i = Point3D(1)
    j = Point3D(0, 1)
    k = Point3D(0, 0, 1)
    self.assertFalse(origin.x)
    self.assertFalse(origin.y)
    self.assertFalse(origin.z)
    self.assertTrue(i.x)
    self.assertFalse(i.y)
    self.assertFalse(i.z)
    self.assertFalse(j.x)
    self.assertTrue(j.y)
    self.assertFalse(j.z)
    self.assertFalse(k.x)
    self.assertFalse(k.y)
    self.assertTrue(k.z)

  def test_rgb_equal(self, ) -> None:
    """
    This method tests equality of 'RGB' instances sharing different
    channels.
    """

    red = RGB(255)
    yellow = RGB(255, 255)
    white = RGB(255, 255, 255)

    self.assertNotEqual(red, yellow)
    self.assertNotEqual(yellow, white)
    self.assertNotEqual(white, red)

    black = RGB()
    schwartz = RGB(0, )
    noir = RGB(0, 0)
    sort_ = RGB(0, 0, 0)

    self.assertEqual(black, schwartz)
    self.assertEqual(black, noir)
    self.assertEqual(black, sort_)
    self.assertEqual(schwartz, noir)
    self.assertEqual(schwartz, sort_)
    self.assertEqual(noir, sort_)

  def test_point_3d_equal(self, ) -> None:
    """
    This method tests equality of 'Point3D' instances sharing different
    coordinates.
    """

    o = Point3D()
    ori = Point3D(0)
    origin = Point3D(0, 0)

    i = Point3D(1)
    j = Point3D(0, 1)
    k = Point3D(0, 0, 1)

    self.assertNotEqual(i, j)
    self.assertNotEqual(j, k)
    self.assertNotEqual(k, i)
    self.assertNotEqual(o, j)
    self.assertNotEqual(o, k)
    self.assertNotEqual(o, i)

    self.assertEqual(o, ori)
    self.assertEqual(o, origin)
    self.assertEqual(ori, origin)

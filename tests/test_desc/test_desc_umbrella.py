"""
TestDescUmbrella covers obscure edge cases and esoteric fallbacks of the
classes found in the 'worktoy.desc' module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from typing import TYPE_CHECKING

from . import ComplexAttriBox, PlaneCircle, PlanePoint
from worktoy.mcls import AbstractNamespace
from worktoy.mcls.space_hooks import SpaceDesc, AbstractSpaceHook

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Self


class TestDescUmbrella(TestCase):
  """
  TestDescUmbrella covers obscure edge cases and esoteric fallbacks of the
  classes found in the 'worktoy.desc' module.
  """

  @classmethod
  def tearDownClass(cls) -> None:
    import sys
    import gc
    sys.modules.pop(__name__, None)
    gc.collect()

  def test_space_desc(self) -> None:
    """
    TestSpaceDesc tests the SpaceDesc descriptor class.
    """

    self.assertIsInstance(AbstractSpaceHook.space, SpaceDesc)

  def test_complex_box(self) -> None:
    """
    TestComplexBox tests the ComplexBox class.
    """

    z0 = ComplexAttriBox()
    z1 = ComplexAttriBox(0.1337, 0.80085)
    z2 = ComplexAttriBox(69, 420)
    z3 = ComplexAttriBox(1337 + 80085j)
    z4 = ComplexAttriBox((69, 420))
    z5 = ComplexAttriBox(8008135, )
    z11 = ComplexAttriBox(z1)

    self.assertIsInstance(z0, ComplexAttriBox)
    self.assertIsInstance(z1, ComplexAttriBox)
    self.assertIsInstance(z2, ComplexAttriBox)
    self.assertIsInstance(z3, ComplexAttriBox)
    self.assertIsInstance(z4, ComplexAttriBox)
    self.assertIsInstance(z11, ComplexAttriBox)

    self.assertEqual(z0.RE, 0.0)
    self.assertEqual(z0.IM, 0.0)
    self.assertEqual(z1.RE, 0.1337)
    self.assertEqual(z1.IM, 0.80085)
    self.assertEqual(z2.RE, 69.0)
    self.assertEqual(z2.IM, 420.0)
    self.assertEqual(z3.RE, 1337.0)
    self.assertEqual(z3.IM, 80085.0)
    self.assertEqual(z4.RE, 69.0)
    self.assertEqual(z4.IM, 420.0)
    self.assertEqual(z5.RE, 8008135.0)
    self.assertEqual(z5.IM, 0.0)
    self.assertEqual(z11.RE, 0.1337)
    self.assertEqual(z11.IM, 0.80085)

  def test_plane_point(self) -> None:
    """
    TestPlanePoint tests the PlanePoint class.
    """

    p0 = PlanePoint()
    p1 = PlanePoint(69, 420, lmao=True)
    p2 = PlanePoint(1337 + 80085j, lmao=True)
    p3 = PlanePoint(69, 420)
    p4 = PlanePoint(1337 + 80085j)
    p5 = PlanePoint(x=1337, y=80085)
    p11 = PlanePoint(p1)
    p12 = PlanePoint(p11, lmao=True)

    self.assertIsInstance(p0, PlanePoint)
    self.assertIsInstance(p1, PlanePoint)
    self.assertIsInstance(p2, PlanePoint)
    self.assertIsInstance(p3, PlanePoint)
    self.assertIsInstance(p4, PlanePoint)
    self.assertIsInstance(p5, PlanePoint)
    self.assertIsInstance(p11, PlanePoint)
    self.assertIsInstance(p12, PlanePoint)

    self.assertEqual(p0.x, 0.0)
    self.assertEqual(p0.y, 0.0)
    self.assertEqual(p1.x, 69.0)
    self.assertEqual(p1.y, 420.0)
    self.assertEqual(p2.x, 1337.0)
    self.assertEqual(p2.y, 80085.0)
    self.assertEqual(p3.x, 69.0)
    self.assertEqual(p3.y, 420.0)
    self.assertEqual(p4.x, 1337.0)
    self.assertEqual(p4.y, 80085.0)
    self.assertEqual(p5.x, 1337.0)
    self.assertEqual(p5.y, 80085.0)
    self.assertEqual(p11.x, 69.0)
    self.assertEqual(p11.y, 420.0)
    self.assertEqual(p12.x, 69.0)
    self.assertEqual(p12.y, 420.0)

  def test_plane_circle(self) -> None:
    """
    TestPlaneCircle tests the PlaneCircle class.
    """
    c0 = PlaneCircle()
    c1 = PlaneCircle(69 + 420j, 1337., lmao=True)
    c2 = PlaneCircle(.1337, .80085, .8008135, lmao=True)
    c3 = PlaneCircle(center=PlanePoint(69, 420), radius=1337.)
    c11 = PlaneCircle(c1)

    self.assertIsInstance(c0, PlaneCircle)
    self.assertIsInstance(c1, PlaneCircle)
    self.assertIsInstance(c2, PlaneCircle)
    self.assertIsInstance(c3, PlaneCircle)
    self.assertIsInstance(c11, PlaneCircle)
    self.assertEqual(c0.center.x, 0.0)
    self.assertEqual(c0.center.y, 0.0)
    self.assertEqual(c0.radius, 0.0)
    self.assertEqual(c1.center.x, 69.0)
    self.assertEqual(c1.center.y, 420.0)
    self.assertEqual(c1.radius, 1337.0)
    self.assertEqual(c2.center.x, 0.1337)
    self.assertEqual(c2.center.y, 0.80085)
    self.assertEqual(c2.radius, 0.8008135)
    self.assertEqual(c3.center.x, 69.0)
    self.assertEqual(c3.center.y, 420.0)
    self.assertEqual(c3.radius, 1337.0)
    self.assertEqual(c11.center.x, 69.0)
    self.assertEqual(c11.center.y, 420.0)
    self.assertEqual(c11.radius, 1337.0)

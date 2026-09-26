"""
TestSpacePoint tests overloaded methods on subclasses as exposed by the
'SpacePoint' class.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.dispatch import TypeSig

from . import DispatcherTest
from .examples import SpacePoint, PlanePoint


class TestSpacePoint(DispatcherTest):
  """
  TestSpacePoint tests overloaded methods on subclasses as exposed by the
  'SpacePoint' class.
  """

  def test_good_get(self, ) -> None:
    """Testing the 'get' functionality of the 'SpacePoint' class."""
    p = SpacePoint(0, 0, 0)
    self.assertAlmostEqual(p.x, 0.0)
    self.assertAlmostEqual(p.y, 0.0)
    self.assertAlmostEqual(p.z, 0.0)
    p = SpacePoint(3, 4, 5)
    self.assertAlmostEqual(p.x, 3.0)
    self.assertAlmostEqual(p.y, 4.0)
    self.assertAlmostEqual(p.z, 5.0)

  def test_dispatcher(self, ) -> None:
    """Testing the dispatcher functionality of the 'SpacePoint' class.
    The dispatcher cloned from 'PlanePoint' keeps the signatures of the
    parent and adds those declared on 'SpacePoint', with 'THIS' resolved
    to 'SpacePoint', so its copy constructor copies all three
    coordinates into a new point."""
    d = SpacePoint.__dict__['__init__'].__sig_funcs__
    sigs = [sig for sig, _ in d]
    self.assertIn(TypeSig(float, float), sigs)
    self.assertIn(TypeSig(PlanePoint), sigs)
    self.assertIn(TypeSig(float, float, float), sigs)
    self.assertIn(TypeSig(SpacePoint), sigs)
    s = SpacePoint(1, 2, 3)
    s2 = SpacePoint(s)
    self.assertIsNot(s2, s)
    self.assertEqual((s2.x, s2.y, s2.z), (1.0, 2.0, 3.0))

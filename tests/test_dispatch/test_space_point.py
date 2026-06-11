"""
TestSpacePoint tests overloaded methods on subclasses as exposed by the
'SpacePoint' class.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from . import DispatcherTest
from .examples import SpacePoint


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
    """Testing the dispatcher functionality of the 'SpacePoint' class."""
    d = SpacePoint.__dict__['__init__'].__sig_funcs__
    s = SpacePoint(1, 2, 3)
    s2 = SpacePoint(s)

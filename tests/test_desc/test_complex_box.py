"""
TestComplexBox tests the 'AttriBox' descriptor functionalities exposed by
the 'ComplexBox' class.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import ComplexBox, DescTest

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestComplexBox(DescTest):
  """
  TestComplexBox tests the 'AttriBox' descriptor functionalities exposed by
  the 'ComplexBox' class.
  """

  def test_good_get(self, ) -> None:
    """Test the 'get' functionality of the 'ComplexBox' class."""
    c = ComplexBox(0, 0)
    self.assertAlmostEqual(c.RE, 0.0)
    self.assertAlmostEqual(c.IM, 0.0)
    self.assertAlmostEqual(c.ABS, 0.0)
    c = ComplexBox(3, 4)
    self.assertAlmostEqual(c.RE, 3.0)
    self.assertAlmostEqual(c.IM, 4.0)
    self.assertAlmostEqual(c.ABS, 5.0)
    c = ComplexBox(1, 1)
    self.assertAlmostEqual(c.RE, 1.0)
    self.assertAlmostEqual(c.IM, 1.0)
    self.assertAlmostEqual(c.ABS ** 2, 2.0)

  def test_good_set(self, ) -> None:
    """Test the 'set' functionality of the 'ComplexBox' class."""
    c = ComplexBox(0, 0)
    self.assertAlmostEqual(c.RE, 0.0)
    self.assertAlmostEqual(c.IM, 0.0)
    self.assertAlmostEqual(c.ABS, 0.0)
    c.RE = 3.0
    c.IM = 4.0
    self.assertAlmostEqual(c.RE, 3.0)
    self.assertAlmostEqual(c.IM, 4.0)
    self.assertAlmostEqual(c.ABS, 5.0)
    c.RE = 1.0
    c.IM = 1.0
    self.assertAlmostEqual(c.RE, 1.0)
    self.assertAlmostEqual(c.IM, 1.0)
    self.assertAlmostEqual(c.ABS ** 2, 2.0)

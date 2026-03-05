"""
TestComplexFields provides tests the descriptor functionalities exposed by
the 'ComplexFields' class.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.keenum import AccessNum
from . import DescTest, ComplexFields, ComplexFieldsSubclass

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestComplexFields(DescTest):
  """
  TestComplexFields provides tests the descriptor functionalities exposed by
  the 'ComplexFields' class.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def test_good_get(self, ) -> None:
    """Test the 'get' functionality of the 'ComplexFields' class."""
    c = ComplexFields(0, 0)
    self.assertAlmostEqual(c.RE, 0.0)
    self.assertAlmostEqual(c.IM, 0.0)
    self.assertAlmostEqual(c.ABS, 0.0)
    c = ComplexFields(3, 4)
    self.assertAlmostEqual(c.RE, 3.0)
    self.assertAlmostEqual(c.IM, 4.0)
    self.assertAlmostEqual(c.ABS, 5.0)
    c = ComplexFields(1, 1)
    self.assertAlmostEqual(c.RE, 1.0)
    self.assertAlmostEqual(c.IM, 1.0)
    self.assertAlmostEqual(c.ABS ** 2, 2.0)

  def test_good_set(self, ) -> None:
    """Test the 'set' functionality of the 'ComplexFields' class."""
    c = ComplexFields(0, 0)
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

  def test_good_subclass(self) -> None:
    """Test the 'subclass' functionality of the 'ComplexFields' class."""
    z = ComplexFieldsSubclass(0, 0)
    self.assertAlmostEqual(z.RE, 0.0)
    self.assertAlmostEqual(z.IM, 0.0)
    self.assertAlmostEqual(z.ABS, 0.0)

  def test_registry(self) -> None:
    """Test the 'registry' functionality of the 'ComplexFields' class."""
    z = ComplexFields(69, 420)
    self.assertEqual(z.RE, 69)
    self.assertEqual(z.IM, 420)
    z.RE = 420
    z.IM = 1337
    self.assertEqual(z.RE, 420)
    self.assertEqual(z.IM, 1337)
    del z.RE
    del z.IM
    regs = z.getAccessRegistry()
    exp = (
      ('RE', AccessNum.SET, 69),
      ('IM', AccessNum.SET, 420),
      ('RE', AccessNum.GET, 69),
      ('IM', AccessNum.GET, 420),
      ('RE', AccessNum.SET, 420),
      ('IM', AccessNum.SET, 1337),
      ('RE', AccessNum.GET, 420),
      ('IM', AccessNum.GET, 1337),
      ('RE', AccessNum.DELETE, None),
      ('IM', AccessNum.DELETE, None),
      )
    for (key, op, value), (expKey, expOp, expValue) in zip(regs, exp, ):
      self.assertIs(op, expOp)
      self.assertEqual(key, expKey)
      self.assertEqual(value, expValue)

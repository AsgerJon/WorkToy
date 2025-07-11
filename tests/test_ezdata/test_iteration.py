"""
TestIteration tests the iterability of the data classes created by EZData.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from icecream import ic

from . import EZTest, RegularClass

if TYPE_CHECKING:  # pragma: no cover
  pass

ic.configureOutput(includeContext=True)


class TestIteration(EZTest):
  """
  TestIteration tests the iterability of the data classes created by EZData.
  """

  def setUp(self) -> None:
    """Set up the test case. """
    self.reg0 = RegularClass(0, )
    self.reg1 = RegularClass(0, 1)
    self.reg2 = RegularClass(0, 1, 2)
    self.reg3 = RegularClass(0, 1, 2, 3)
    self.reg4 = RegularClass(0, 1, 2, 3, 4)
    self.reg5 = RegularClass(0, 1, 2, 3, 4, 5)

    self.regs = [
        self.reg0,
        self.reg1,
        self.reg2,
        self.reg3,
        self.reg4,
        self.reg5,
    ]

  def test_iteration(self) -> None:
    """Test the iteration of the data classes."""

    for i, reg in enumerate(self.regs):
      self.assertIsInstance(reg, RegularClass)
      j = 0
      for j, f in enumerate(reg):
        if j > i:
          break
        self.assertEqual(j, f)

  def test_ad_hoc(self) -> None:
    """Test ad-hoc iteration."""

  def test_star(self) -> None:
    """Test the star operator on the data class."""

    for reg in self.regs:
      self.assertEqual(len(RegularClass.__slots__), len((*reg,)))

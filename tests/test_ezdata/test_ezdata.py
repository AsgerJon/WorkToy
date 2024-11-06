"""TestEZData tests the functionality of EZData"""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.ezdata import EZData


class Complex(EZData):
  """Complex encapsulates complex numbers in a dataclass"""


class TestEZData(TestCase):
  """TestEZData tests the functionality of EZData"""

  def setUp(self) -> None:
    """Sets up each method"""
    self.ezData = Complex()
    self.inlineClass = EZData()

  def testInit(self, ) -> None:
    """Tests the initialization of the EZData class"""
    self.assertEqual(self.ezData.IM, 0.0)

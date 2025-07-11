"""
TestEZData runs the basic tests for the EZData class and its subclasses.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from . import EZTest

from worktoy.ezdata import EZData, EZMeta, EZSpace, EZSlot, EZSpaceHook


class EZRegular(EZData):
  """Regular EZData class setting attributes directly as variables."""

  x = 69
  y = 420


class TestEZData(EZTest):
  """
  TestEZData runs the basic tests for the EZData class and its subclasses.
  """

  def test_existence(self) -> None:
    """Test that the EZData class exists."""
    self.assertTrue(EZData)
    self.assertTrue(EZRegular)
    self.assertIsInstance(EZRegular, EZMeta)
    self.assertIsSubclass(EZRegular, EZData)

  def test_instance(self) -> None:
    """Test that the EZData class can be instantiated."""
    ez = EZRegular()
    self.assertIsInstance(ez, EZRegular)
    self.assertIsInstance(ez, EZData)

  def test_good_getter(self) -> None:
    """Tests that the EZData classes can access their explicit attributes.
    No default values and no changed values. """
    ez = EZRegular()
    self.assertEqual(ez.x, 69)
    self.assertEqual(ez.y, 420)

  def test_good_setter(self) -> None:
    """Tests that the EZData classes can set their explicit attributes."""
    ez = EZRegular()
    self.assertEqual(ez.x, 69)
    self.assertEqual(ez.y, 420)
    ez.x = 100
    ez.y = 200
    self.assertEqual(ez.x, 100)
    self.assertEqual(ez.y, 200)

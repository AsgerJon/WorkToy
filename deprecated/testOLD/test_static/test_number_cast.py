"""TestNumberCast tests the number casting system. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase
from worktoy.static.casting import IntCast, FloatCast, ComplexCast, AutoCast
from worktoy.waitaminute import CastMismatch


class TestNumberCast(TestCase):
  """Test the number casting system."""

  def setUp(self) -> None:
    """Sets up cast objects for testing."""
    self.intSamples = [69, 420, 1337, 80085]
    self.floatSamples = [69., 420., 1337., 80085., ]
    self.complexSamples = [69 + 0j, 420 + 0j, 1337 + 0j]
    self.samples = [self.intSamples, self.floatSamples, self.complexSamples]
    self.intCast = IntCast()
    self.floatCast = FloatCast()
    self.complexCast = ComplexCast()

  def test_int_cast(self) -> None:
    """Test the int cast."""
    for INT, FLOAT, COMPLEX in zip(*self.samples):
      self.assertEqual(INT, self.intCast(INT))
      self.assertEqual(INT, self.intCast(FLOAT))
      self.assertEqual(INT, self.intCast(COMPLEX))

  def test_float_cast(self) -> None:
    """Test the float cast."""
    for INT, FLOAT, COMPLEX in zip(*self.samples):
      self.assertEqual(FLOAT, self.floatCast(FLOAT))
      self.assertEqual(FLOAT, self.floatCast(INT))
      self.assertEqual(FLOAT, self.floatCast(COMPLEX))

  def test_complex_cast(self) -> None:
    """Test the complex cast."""
    for INT, FLOAT, COMPLEX in zip(*self.samples):
      self.assertEqual(COMPLEX, self.complexCast(COMPLEX))
      self.assertEqual(COMPLEX, self.complexCast(INT))
      self.assertEqual(COMPLEX, self.complexCast(FLOAT))

  def test_errors(self, ) -> None:
    """Test the errors."""
    # Test the errors
    with self.assertRaises(CastMismatch):
      self.intCast(69.80085)
    with self.assertRaises(CastMismatch):
      self.intCast(69 + 420j)
    with self.assertRaises(CastMismatch):
      self.floatCast(69 + 420j)

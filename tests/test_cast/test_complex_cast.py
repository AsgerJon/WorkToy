"""TestComplexCast tests casting of strings to complex numbers. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.static import ComplexCastException, complexCast


class TestComplexCast(TestCase):
  """TestComplexCast tests casting of strings to complex numbers. """

  def setUp(self, ) -> None:
    """Sets up each test. """
    self.sampleValues = [
        69, 420.69, 420 + 69j, '69', '420.69', '420+69j',
    ]
    self.expectedValues = [
        69, 420.69, 420 + 69j, 69, 420.69, 420 + 69j,
    ]

  def test_complex_cast(self, ) -> None:
    """Test casting to complex"""
    for sample, expected in zip(self.sampleValues, self.expectedValues):
      self.assertEqual(complexCast(sample), expected)

  def test_error(self, ) -> None:
    """Testing that the correct exception is raised. """
    with self.assertRaises(ComplexCastException) as context:
      complexCast('sixty-nine, four twenty')
    if isinstance(context, ComplexCastException):
      self.assertEqual(context.value, 'sixty-nine, four twenty')
      self.assertEqual(context.target, complex)

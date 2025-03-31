"""TestFloatCast tests casting of python objects to floats. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.static import FloatCastException, floatCast


class TestFloatCast(TestCase):
  """TestFloatCast tests casting of python objects to floats. """

  def setUp(self, ) -> None:
    """Sets up each test. """
    self.floatSample = 1.0
    self.intSample = 1
    self.complexSample = 1.0 + 0.0j
    self.strSample = '1.0'
    self.boolSample = True

  def test_float_cast(self, ) -> None:
    """Test casting to float"""
    self.assertEqual(floatCast(self.floatSample), self.floatSample)
    self.assertEqual(floatCast(self.intSample), 1.0)
    self.assertEqual(floatCast(self.complexSample), 1.0)
    self.assertEqual(floatCast(self.strSample), 1.0)

  def test_error(self, ) -> None:
    """Testing that the correct exception is raised. """
    with self.assertRaises(FloatCastException) as context:
      floatCast('sixty-nine, four twenty')
    if isinstance(context, FloatCastException):
      self.assertEqual(context.value, 'sixty-nine, four twenty')
      self.assertEqual(context.target, float)

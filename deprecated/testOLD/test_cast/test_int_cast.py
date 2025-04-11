"""TestIntCast tests casting of python objects to integers. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.static import IntCastException, intCast


class TestIntCast(TestCase):
  """TestIntCast tests casting of python objects to integers. """

  def setUp(self, ) -> None:
    """Sets up each test. """
    self.intSample = 1
    self.floatSample = 1.0
    self.complexSample = 1.0 + 0.0j
    self.strSample = '1.0'
    self.boolSample = True

  def test_int_cast(self, ) -> None:
    """Test casting to int"""
    self.assertEqual(intCast(self.intSample), self.intSample)
    self.assertEqual(intCast(self.floatSample), 1)
    self.assertEqual(intCast(self.complexSample), 1)
    self.assertEqual(intCast(self.strSample), 1)

  def test_error(self, ) -> None:
    """Testing that the correct exception is raised. """
    with self.assertRaises(IntCastException) as context:
      intCast('sixty-nine, four twenty')
    if isinstance(context, IntCastException):
      self.assertEqual(context.value, 'sixty-nine, four twenty')
      self.assertEqual(context.target, int)

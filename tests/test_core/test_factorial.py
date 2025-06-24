"""
TestFactorial tests the factorial function from the 'worktoy.core' module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

import os
from unittest import TestCase
from typing import TYPE_CHECKING

from worktoy.core import factorial

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestFactorial(TestCase):
  """
  TestFactorial tests the factorial function from the 'worktoy.core' module.
  """

  @classmethod
  def tearDownClass(cls) -> None:
    import sys
    import gc
    sys.modules.pop(__name__, None)
    gc.collect()

  def test_factorial(self) -> None:
    """
    Tests that the factorial function returns the correct value for small
    integers.
    """
    prev = 1
    for i in range(1, 5):
      self.assertEqual(factorial(i), prev * i)
      prev *= i

  def test_factorial_unit(self) -> None:
    """
    Tests that the factorial function returns 1 for 0! and 1!.
    """
    self.assertEqual(factorial(0), 1)
    self.assertEqual(factorial(1), 1)

  def test_factorial_negative(self) -> None:
    """
    Tests that the factorial function raises a ValueError for negative
    integers.
    """
    with self.assertRaises(ValueError) as context:
      factorial(-1)
    e = context.exception
    self.assertIsInstance(e, ValueError)
    self.assertIn('is not defined for negative numbers', str(e))

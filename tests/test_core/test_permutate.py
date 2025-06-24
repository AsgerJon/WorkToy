"""
TestPermutate tests that the permutate function works as expected.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

import os
from unittest import TestCase
from typing import TYPE_CHECKING

from worktoy.core import permutate, factorial

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestPermutate(TestCase):
  """
  TestPermutate tests that the permutate function works as expected.
  """

  @classmethod
  def tearDownClass(cls) -> None:
    import sys
    import gc
    sys.modules.pop(__name__, None)
    gc.collect()

  def test_empty(self) -> None:
    """
    Test that permutate returns an empty list when given an empty list.
    """
    self.assertFalse(permutate()[0])

  def test_single(self) -> None:
    """
    Test that permutate returns a list with a single element when given a
    single element.
    """
    self.assertEqual(permutate(1), [(1,)])

  def test_two(self) -> None:
    """
    Test that permutate returns the correct permutations for two elements.
    """
    self.assertEqual(permutate(1, 2), [(1, 2), (2, 1)])

  def test_three(self) -> None:
    """
    Test that permutate returns the correct permutations for three elements.
    """
    expected = [
        (1, 2, 3),
        (1, 3, 2),
        (2, 1, 3),
        (2, 3, 1),
        (3, 1, 2),
        (3, 2, 1)
    ]
    actual = permutate(1, 2, 3)
    for exp, act in zip(expected, actual):
      self.assertEqual(exp, act)

  def test_many(self) -> None:
    """
    Test that permutate returns the correct permutations for many elements.
    """
    for i in range(4, 6):
      actualLength = len(permutate(*range(i)))
      expectedLength = factorial(i)
      self.assertEqual(actualLength, expectedLength)

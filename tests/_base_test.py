"""
BaseTest subclasses unittest.TestCase to provide a base class shared by
testclasses across the 'tests' package. It implements module unloading in
the 'tearDownClass' method and adds 'assertIsSubclass' (and negation).
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase
from random import randint
from typing import TYPE_CHECKING

from worktoy.utilities import maybe

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Iterator

  IntSample: TypeAlias = Iterator[tuple[int, ...]]


class BaseTest(TestCase):
  """BaseTest provides a base class shared by the testing classes in the
  tests package. It implements module unloading in the 'tearDownClass'
  method and adds 'assertIsSubclass' (and negation)."""

  @staticmethod
  def generateRandomIntegers(*args) -> IntSample:
    """
    Generates a list of tuples containing random integers.
    Arguments:
      args = (n, N, a, b)
        n: Number of tuples to generate. Default is 1.
        N: Number of integers in each tuple. Default is 1.
        a: Minimum integer value (inclusive). Default is 0.
        b: Maximum integer value (exclusive). Default is 256.
      if a > b, then a and b are swapped.
    Returns:
      A list of 'N' tuples, each containing 'n' random integers in
      range [a, b).
    """
    n, N, a, b, *_ = [*args, None, None, None, None]
    n, N, a, b = maybe(n, 1), maybe(N, 1), maybe(a, 0), maybe(b, 256),
    a, b = (a, b) if a < b else (b, a)
    for _ in range(N):
      yield tuple(randint(a, b - 1) for _ in range(n))

  @classmethod
  def tearDownClass(cls) -> None:
    """Remove the test class from sys.modules and run the garbage
    collector."""
    import sys
    import gc
    sys.modules.pop(cls.__module__, None)
    gc.collect()

  def assertIsSubclass(self, subClass: type, superClass: type, ) -> None:
    """Assert that 'subClass' is a subclass of 'superClass'."""
    self.assertTrue(issubclass(subClass, superClass))

  def assertIsNotSubclass(self, subClass: type, superClass: type, ) -> None:
    """Assert that 'subClass' is not a subclass of 'superClass'."""
    self.assertFalse(issubclass(subClass, superClass))

  def assertNotIsSubclass(self, *args) -> None:
    """Same as above"""
    self.assertIsNotSubclass(*args)

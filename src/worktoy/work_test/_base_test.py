"""
BaseTest subclasses unittest.TestCase to provide a base class shared by
testclasses across the 'tests' package. It implements module unloading in
the 'tearDownClass' method and adds 'assertIsSubclass' (and negation).
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase
from random import randint, random
from typing import TYPE_CHECKING

from ..desc import Field
from ..utilities import maybe

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Iterator

  IntSample: TypeAlias = Iterator[tuple[int, ...]]
  TypicalExceptions: TypeAlias = Iterator[type[Exception]]
  ExcType: TypeAlias = type[BaseException]

#  So Python 3.14 saw 'assertIsSubclass' and 'assertNotIsSubclass' added to
#  'unittest.TestCase', but since we support back to 3.7, but also up to
#  3.14, we need the following 'try-except-else':

try:
  _ = TestCase.assertIsSubclass
except AttributeError:  # pragma: no cover
  class _Temp(TestCase):
    def assertIsSubclass(self, cls: type, base: type, msg=None) -> None:
      """Assert that 'subClass' is a subclass of 'superClass'."""
      self.assertTrue(issubclass(cls, base))

    def assertNotIsSubclass(self, cls: type, base: type, msg=None) -> None:
      """Assert that 'subClass' is not a subclass of 'superClass'."""
      self.assertFalse(issubclass(cls, base))
else:  # version >= 3.14
  _Temp = TestCase


class BaseTest(_Temp):
  """
  BaseTest provides a base class shared by the testing classes in the
  tests package. It implements module unloading in the 'tearDownClass'
  method and adds 'assertIsNotInstance' and 'assertIsNotSubclass'.
  """

  attrErrTrace = Field()
  exceptions = Field()

  @attrErrTrace.GET
  def _getAttributeErrorTrace(self, ) -> str:
    return """object has no attribute"""

  @exceptions.GET
  def _getTypicalExceptions(self, ) -> TypicalExceptions:
    yield from (
      ValueError,
      KeyError,
      IndexError,
      RuntimeError,
      OSError,
      PermissionError,
      TypeError,
      FileExistsError,
      FileNotFoundError,
      )

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

  @staticmethod
  def randFloat(*args) -> float:
    a, b, *_ = (*args, 0.0, 1.0)
    minVal, maxVal = min(a, b), max(a, b)
    return random() * (maxVal - minVal) + minVal

  @classmethod
  def randFloats(cls, N: int = None, *args) -> Iterator[float]:
    for _ in range(maybe(N, 1)):
      yield cls.randFloat(*args)

  @classmethod
  def randFloatTuple(cls, N: int = None, *args) -> tuple[float, ...]:
    return (*cls.randFloats(N, *args),)

  @classmethod
  def randFloatTuples(cls, *args) -> Iterator[tuple[float, ...]]:
    n, N, a, b, *_ = (*args, None, None, None, None)
    n, N = maybe(n, 1), maybe(N, 1)
    a, b = maybe(a, 0.0), maybe(b, 1.0)
    minVal, maxVal = min(a, b), max(a, b)
    for _ in range(n):
      yield cls.randFloatTuple(N, minVal, maxVal)

  @classmethod
  def tearDownClass(cls) -> None:
    """Remove the test class from sys.modules and run the garbage
    collector."""
    import sys
    import gc
    sys.modules.pop(cls.__module__, None)
    gc.collect()

  assertIsNotSubclass = _Temp.assertNotIsSubclass
  assertIsNotInstance = _Temp.assertNotIsInstance

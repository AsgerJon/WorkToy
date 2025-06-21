"""
TestClassIterNext verifies '__class_iter__' and '__class_next__' hooks.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.mcls import AbstractMetaclass
from worktoy.waitaminute import TypeException

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Iterator


class LazyClass(metaclass=AbstractMetaclass):
  """
  LazyClass implements class-level iteration via a generator.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  @classmethod
  def __class_iter__(cls) -> Iterator[int]:
    """
    Yields fixed values.
    """
    yield from [69, 420, 1337, 80085, 8008135]


class StatefulClass(metaclass=AbstractMetaclass):
  """
  StatefulClass implements class-level iteration using internal state.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __iter_contents__ = None

  #  Fallback Variables
  __fallback_contents__ = [69, 420, 1337, 80085, 8008135]

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def __class_iter__(cls) -> type[StatefulClass]:
    """
    Prepares iteration state and returns class as iterator.
    """
    cls.__iter_contents__ = [*reversed(cls.__fallback_contents__), ]
    return cls

  @classmethod
  def __class_next__(cls) -> int:
    """
    Manually produces next item or raises StopIteration.
    """
    if cls.__iter_contents__:
      return cls.__iter_contents__.pop()
    cls.__iter_contents__ = None
    raise StopIteration


class TestClassIterNext(TestCase):
  """
  TestClassIterNext verifies '__class_iter__' and '__class_next__' hooks.
  """

  def testLazyClassIteration(self) -> None:
    """
    Tests that LazyClass yields expected values.
    """
    expected = [69, 420, 1337, 80085, 8008135]
    self.assertEqual(list(LazyClass), expected)

  def testStatefulClassIteration(self) -> None:
    """
    Tests StatefulClass iteration using internal state.
    """
    expectations = [69, 420, 1337, 80085, 8008135]
    for actual, expected in zip(StatefulClass, expectations):
      self.assertEqual(actual, expected)

  def testStateReset(self) -> None:
    """
    Tests iteration reset behavior on StatefulClass.
    """
    val1 = list(StatefulClass)
    val2 = list(StatefulClass)
    self.assertEqual(val1, val2)

  def testStopIterationRaised(self) -> None:
    """
    Ensures StopIteration is raised after exhaustion.
    """
    it = iter(StatefulClass)
    for _ in range(5):
      next(it)
    with self.assertRaises(StopIteration):
      next(it)

  def testStatefulIteratorEmpties(self) -> None:
    """
    Confirms that StatefulClass empties its internal state after iteration.
    """
    list(StatefulClass)
    self.assertFalse(StatefulClass.__iter_contents__)


def testManualNextCalls(self) -> None:
  """
  Verifies StatefulClass manually yields all expected values.
  """
  expected = [69, 420, 1337, 80085, 8008135]
  it = iter(StatefulClass)
  for val in expected:
    self.assertEqual(next(it), val)
  with self.assertRaises(StopIteration):
    next(it)

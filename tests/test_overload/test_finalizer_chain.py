"""
TestFinalizerChain subclasses 'OverloadTest' and pins that an exception
raised by a finalizer is chained from the exception the dispatched call
raised, and from nothing else. The dispatcher asked 'sys.exc_info()' for
the exception in flight, which also reports an exception the caller is
handling, so a call made inside an 'except' block that returned normally
had its finalizer's exception marked as caused by the caller's.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.dispatch import overload
from worktoy.mcls import BaseObject

from . import OverloadTest


class Finalized(BaseObject):
  """Finalized has a finalizer that raises."""

  @overload(int)
  def bar(self, x: int) -> int:
    return x

  @overload(str)
  def bar(self, s: str) -> str:
    raise KeyError(s)

  @overload.finalize
  def bar(self, *args) -> None:
    raise ValueError('finalizer')


class TestFinalizerChain(OverloadTest):
  """
  TestFinalizerChain provides tests for the chaining of an exception a
  finalizer raises.
  """

  def test_not_caused_by_caller(self) -> None:
    """A call returning normally inside an 'except' block raises the
    finalizer's exception with no cause."""
    try:
      raise RuntimeError('caller')
    except RuntimeError:
      with self.assertRaises(ValueError) as context:
        Finalized().bar(1)
    self.assertIsNone(context.exception.__cause__)

  def test_caused_by_call(self) -> None:
    """A call that raised has the finalizer's exception chained from its
    own, inside an 'except' block or not."""
    try:
      raise RuntimeError('caller')
    except RuntimeError:
      with self.assertRaises(ValueError) as context:
        Finalized().bar('x')
    self.assertIsInstance(context.exception.__cause__, KeyError)
    with self.assertRaises(ValueError) as context:
      Finalized().bar('y')
    self.assertIsInstance(context.exception.__cause__, KeyError)

  def test_outside_handler(self) -> None:
    """A call returning normally outside any handler raises the
    finalizer's exception with no cause."""
    with self.assertRaises(ValueError) as context:
      Finalized().bar(1)
    self.assertIsNone(context.exception.__cause__)

"""
TestDispatchUnhashableClass subclasses 'DispatcherTest' and pins that a
call with an argument whose class cannot be hashed goes on to the
'isinstance' pass. The exact-type lookup hashes the classes of the
arguments, which raised Python's own 'TypeError' for a class whose
metaclass defines '__eq__' without '__hash__', before any signature was
tried.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.dispatch import overload
from worktoy.mcls import BaseObject

from . import DispatcherTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class UnhashableMeta(type):
  """UnhashableMeta makes its classes unhashable."""

  def __eq__(cls, other: Any) -> bool:
    return cls is other  # pragma: no cover

  __hash__ = None


class Weird(metaclass=UnhashableMeta):
  """Weird is a class that cannot be hashed."""


class Takes(BaseObject):
  """Takes overloads 'bar' for 'int' and for any object."""

  @overload(int)
  def bar(self, x: int) -> str:
    return 'int'

  @overload(object)
  def bar(self, x: Any) -> str:
    return 'object'


class TestDispatchUnhashableClass(DispatcherTest):
  """
  TestDispatchUnhashableClass provides tests for dispatching an argument
  of an unhashable class.
  """

  def test_reaches_isinstance(self) -> None:
    """The call is matched by 'isinstance'."""
    self.assertEqual(Takes().bar(Weird()), 'object')

  def test_hashable_exact(self) -> None:
    """A hashable argument is still matched by its exact type."""
    self.assertEqual(Takes().bar(1), 'int')

"""
TestKeeUnhashableValue subclasses 'KeeTest' and pins that a 'KeeNum'
looked up by a value that cannot be hashed falls back to comparing the
member values one by one, as it does when a member value cannot be
hashed. The lookup used to look the value up in the cache of hashable
values directly, which raised Python's own 'TypeError' for the call,
the subscript and 'fromValue' alike.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeNum, Kee
from worktoy.waitaminute.keenum import KeeResolveError

from . import KeeTest


class Pairs(KeeNum):
  """Pairs holds members of hashable tuple values."""

  A = Kee[tuple]((1, 2))
  B = Kee[tuple]((3, 4))


class UnhashableTuple(tuple):
  """UnhashableTuple compares as a tuple and refuses to be hashed."""

  __hash__ = None


class TestKeeUnhashableValue(KeeTest):
  """
  TestKeeUnhashableValue provides tests for looking up a 'KeeNum' by a
  value that cannot be hashed.
  """

  def test_call_misses(self) -> None:
    """A call with an unhashable value matching no member raises
    'KeeResolveError'."""
    with self.assertRaises(KeeResolveError):
      Pairs((1, [2]))

  def test_subscript_misses(self) -> None:
    """A subscript with such a value raises 'KeeResolveError'."""
    with self.assertRaises(KeeResolveError):
      _ = Pairs[(1, [2])]

  def test_from_value_misses(self) -> None:
    """'fromValue' with such a value raises 'KeeResolveError'."""
    with self.assertRaises(KeeResolveError):
      Pairs.fromValue((1, [2]))

  def test_unhashable_equal_value(self) -> None:
    """An unhashable value equal to a member value finds the member."""
    self.assertIs(Pairs(UnhashableTuple((3, 4))), Pairs.B)
    self.assertIs(Pairs.fromValue(UnhashableTuple((1, 2))), Pairs.A)

  def test_hashable_value(self) -> None:
    """A hashable value still finds its member."""
    self.assertIs(Pairs((3, 4)), Pairs.B)

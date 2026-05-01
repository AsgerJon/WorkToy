"""
TestPermuter subclasses 'DispatcherTest' from 'tests.test_dispatch' and
provides tests for the 'Permuter' class from 'worktoy.dispatch'.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.utilities.combinatorics import Arrangement
from . import DispatcherTest
from worktoy.dispatch import Permuter
from worktoy.waitaminute import TypeException
from worktoy.waitaminute.desc import WriteOnceError

if TYPE_CHECKING:  # pragma: no cover
  # @formatter:off
  from typing import Any, Callable, Optional
  from worktoy.dispatch._call_me_maybe import _Wrapped  # noqa
  from worktoy.utilities import QuickDesc  # noqa

  class Permuter:  # noqa
    __function_case__: Optional[tuple[Callable]]
    __arg_arrangement__: Optional[Arrangement]
    __wrapped__: _Wrapped
    arrangement: QuickDesc[Arrangement]
    def __init__(self, *args, ) -> None: ...
    def setArrangement(self, arrangement: Arrangement) -> None: ...
    def __lshift__(self, arrangement: Arrangement) -> Permuter: ...
    def __ilshift__(self, arrangement: Arrangement) -> Permuter: ...
    def __rrshift__(self, arrangement: Arrangement) -> Permuter: ...
  # @formatter:on


def _identity(a: Any, b: Any, c: Any) -> Any:
  """Three-arg function returning args as a tuple — easy to assert
  against."""
  return a, b, c


def _two_args(x: Any, y: Any) -> Any:
  return x, y


def _arr(items: tuple, forward: tuple) -> Arrangement:
  """Construct an Arrangement from explicit items + forward recipe.
  Test helper — production code should iterate 'Arrangements(*items)'."""
  return Arrangement(items, forward)


class TestPermuter(DispatcherTest):
  """Permuter constructor and behavior."""

  #  ________________________________________________________________
  #  Good construction overloads
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_init_empty(self) -> None:
    """Permuter() leaves both func and arrangement unset."""
    p = Permuter()
    self.assertIsNone(p.__function_case__)
    self.assertIsNone(p.__arg_arrangement__)

  def test_init_func_only(self) -> None:
    p = Permuter(_identity)
    self.assertIs(p.__wrapped__, _identity)
    self.assertIsNone(p.__arg_arrangement__)

  def test_init_arrangement_only(self) -> None:
    a = _arr(('A', 'B', 'C'), (2, 0, 1))
    p = Permuter(a)
    self.assertIs(p.arrangement, a)
    self.assertIsNone(p.__function_case__)

  def test_init_func_then_arrangement(self) -> None:
    a = _arr(('A', 'B', 'C'), (2, 0, 1))
    p = Permuter(_identity, a)
    self.assertIs(p.__wrapped__, _identity)
    self.assertIs(p.arrangement, a)

  def test_init_arrangement_then_func(self) -> None:
    """Argument order should not matter — dispatch is type-driven."""
    a = _arr(('A', 'B', 'C'), (2, 0, 1))
    p = Permuter(a, _identity)
    self.assertIs(p.__wrapped__, _identity)
    self.assertIs(p.arrangement, a)

  #  ________________________________________________________________
  #  Bad construction overloads
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_init_rejects_too_many_args(self) -> None:
    a = _arr(('A', 'B'), (0, 1))
    with self.assertRaises(ValueError):
      Permuter(_identity, a, _two_args)

  def test_init_rejects_duplicate_arrangement(self) -> None:
    a1 = _arr(('A', 'B'), (0, 1))
    a2 = _arr(('A', 'B'), (1, 0))
    with self.assertRaises(ValueError):
      Permuter(a1, a2)

  def test_init_rejects_duplicate_func(self) -> None:
    with self.assertRaises(ValueError):
      Permuter(_identity, _two_args)

  def test_init_rejects_unknown_type(self) -> None:
    with self.assertRaises(TypeException):
      Permuter(42)

  #  ________________________________________________________________
  #  Good Operator Usage
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_lshift_returns_new_instance(self) -> None:
    """`p << arrangement` should not mutate p; returns a new Permuter."""
    p = Permuter(_identity)
    a = _arr(('A', 'B', 'C'), (2, 0, 1))
    q = p << a
    self.assertIsNot(p, q)
    self.assertIsNone(p.__arg_arrangement__)
    self.assertIs(q.arrangement, a)
    self.assertIs(q.__wrapped__, _identity)

  def test_ilshift_mutates_in_place(self) -> None:
    p = Permuter(_identity)
    a = _arr(('A', 'B', 'C'), (2, 0, 1))
    q = p
    p <<= a
    self.assertIs(p, q)
    self.assertIs(p.arrangement, a)

  def test_rrshift_equivalent_to_lshift(self) -> None:
    """`arrangement >> p` produces the same result as `p << arrangement`."""
    p: Permuter = Permuter(_identity)
    a: Arrangement = _arr(('A', 'B', 'C'), (2, 0, 1))
    q = a >> p
    self.assertIs(q.__wrapped__, _identity)
    self.assertIs(q.arrangement, a)

  #  ________________________________________________________________
  #  Bad Operator - Verifying 'NotImplemented' as return value
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_not_implemented_returns(self) -> None:
    p = Permuter(_identity)
    self.assertIs(p.__lshift__(69), NotImplemented)  # noqa
    self.assertIs(p.__ilshift__(420), NotImplemented)  # noqa

  #  ________________________________________________________________
  #  Bad Operator - Verifying exception
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_ilshift_again(self) -> None:
    a1 = _arr(('A', 'B', 'C'), (0, 1, 2))
    a2 = _arr(('A', 'B', 'C'), (2, 1, 0))
    p = Permuter(_identity, a1)
    with self.assertRaises(WriteOnceError) as context:
      p <<= a2
    e = context.exception
    self.assertIs(e.desc, p)
    self.assertEqual(e.oldValue, a1)
    self.assertEqual(e.newValue, a2)

  #  ________________________________________________________________
  #  Functionality — the actual point of the class
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_invoke_reorders_positional_args(self) -> None:
    """Caller supplies args in arranged order; func receives them in
    canonical (items) order. With items=(A,B,C) and forward=(2,0,1),
    the arranged values are (C,A,B). A user passing ('c','a','b')
    expects the wrapped function to see ('a','b','c')."""
    a = _arr(('A', 'B', 'C'), (2, 0, 1))
    p = Permuter(_identity, a)
    self.assertEqual(p('c', 'a', 'b'), ('a', 'b', 'c'))

  def test_invoke_two_arg_swap(self) -> None:
    a = _arr(('X', 'Y'), (1, 0))
    p = Permuter(_two_args, a)
    self.assertEqual(p('y', 'x'), ('x', 'y'))

  def test_invoke_identity_arrangement_is_passthrough(self) -> None:
    a = _arr(('A', 'B', 'C'), (0, 1, 2))
    p = Permuter(_identity, a)
    self.assertEqual(p(1, 2, 3), (1, 2, 3))

  def test_invoke_three_cycle(self) -> None:
    """Regression test for the original bug: a 3-cycle (not a
    transposition) must round-trip correctly. Items (A,B,C) with
    forward (1,2,0) produces arranged values (B,C,A); user calls
    with ('b','c','a') and the function must receive ('a','b','c')."""
    a = _arr(('A', 'B', 'C'), (1, 2, 0))
    p = Permuter(_identity, a)
    self.assertEqual(p('b', 'c', 'a'), ('a', 'b', 'c'))

  def test_invoke_passes_kwargs_through_unmodified(self) -> None:
    """Arrangement only touches positional args; kwargs pass through."""

    def f(a, b, *, k) -> tuple[Any, Any, Any]:
      return a, b, k

    a = _arr(('A', 'B'), (1, 0))
    p = Permuter(f, a)
    self.assertEqual(p('y', 'x', k='kw'), ('x', 'y', 'kw'))

  #  ________________________________________________________________
  #  Good setter
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_set_arrangement_good(self) -> None:
    p = Permuter(_identity)
    a = _arr(('A', 'B', 'C'), (2, 0, 1))
    p.setArrangement(a)
    self.assertIs(p.arrangement, a)

  #  ________________________________________________________________
  #  Bad setter — write-once
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_set_arrangement_again(self) -> None:
    """Once arrangement is set, it cannot be changed."""
    a1 = _arr(('A', 'B', 'C'), (0, 1, 2))
    a2 = _arr(('A', 'B', 'C'), (2, 1, 0))
    p = Permuter(_identity, a1)
    with self.assertRaises(WriteOnceError) as context:
      p.setArrangement(a2)
    e = context.exception
    self.assertIs(e.desc, p)
    self.assertEqual(e.oldValue, a1)
    self.assertEqual(e.newValue, a2)

  #  ________________________________________________________________
  #  Bad setter — type check
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_set_arrangement_wrong_type(self) -> None:
    """setArrangement should only accept Arrangement instances."""
    p = Permuter(_identity)
    susArrangement = """Hi, I'm an arrangement, trust me bro!"""
    with self.assertRaises(TypeException) as context:
      p.setArrangement(susArrangement)  # noqa
    e = context.exception
    self.assertEqual(e.varName, 'arrangement')
    self.assertEqual(e.actualObject, susArrangement)
    self.assertIs(e.actualType, str)
    self.assertIn(Arrangement, e.expectedTypes)

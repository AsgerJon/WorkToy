"""
TestLoadARGS exercises the variadic '*ARGS[T]' overload syntax. The
'@overload(...)' decorator expands a trailing 'ARGS' sentinel into
concrete signatures for lengths 0 through
'overload.__variadic_fastpath_limit__', plus a single variadic entry
that the dispatcher consults via list iteration when the call length
exceeds the expansion limit. These tests cover both tiers and the
interaction with explicit overrides.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.core.sentinels import ARGS
from worktoy.dispatch import Dispatcher, TypeSig, overload
from worktoy.mcls import BaseObject
from worktoy.waitaminute.dispatch import DispatchException
from . import OverloadTest

if TYPE_CHECKING:  # pragma: no cover
  pass


class IntCollector(BaseObject):
  """Variadic-only collector. Accepts any number of 'int' arguments."""

  @overload(*ARGS[int])
  def __init__(self, *nums: int) -> None:
    self.nums = nums


class PrefixedCollector(BaseObject):
  """One required 'str' prefix followed by any number of 'int' args."""

  @overload(str, *ARGS[int])
  def __init__(self, name: str, *nums: int) -> None:
    self.name = name
    self.nums = nums


class MixedCollector(BaseObject):
  """Variadic plus an explicit override for the 2-int case. The
  explicit override is registered after the variadic, so it
  overwrites the '(str, int, int)' entry that the variadic
  expansion would otherwise have populated."""

  @overload(str, *ARGS[int])
  def __init__(self, name: str, *nums: int) -> None:
    self.kind = 'variadic'
    self.name = name
    self.nums = nums

  @overload(str, int, int)
  def __init__(self, name: str, x: int, y: int) -> None:
    self.kind = 'pair'
    self.name = name
    self.nums = (x, y)


class StrictCollector(BaseObject):
  """Strict variadic. The 'strict=True' kwarg disables 'typeCast'
  on the resulting signatures, so calls whose arg types do not
  isinstance-match 'int' must raise rather than coerce."""

  @overload(*ARGS[int], strict=True)
  def __init__(self, *nums: int) -> None:
    self.nums = nums


class DualVariadic(BaseObject):
  """Two variadic overloads stacked under the same method name.
  The second '@overload' registration finds 'collect' already in
  the namespace's variadic map and appends to the existing list
  rather than creating a new entry."""

  @overload(*ARGS[int])
  def collect(self, *nums: int) -> str:
    return 'int'

  @overload(*ARGS[str])
  def collect(self, *names: str) -> str:
    return 'str'


class ParentWithVariadic(BaseObject):
  """Parent class registering a variadic overload that 'ChildOf
  ParentVariadic' should inherit during its own namespace
  construction."""

  @overload(*ARGS[int])
  def collect(self, *nums: int) -> str:
    return 'parent-int'


class ChildOfParentVariadic(ParentWithVariadic):
  """Empty body - the variadic inheritance happens via
  'BaseSpace.__init__' walking the parent's '__namespace__' and
  re-registering each '(name, sig, func)' pair."""


class TestLoadARGS(OverloadTest):
  """
  TestLoadARGS covers the FASTEST-tier expansion of '*ARGS[T]' and the
  FAST/SLOW-tier list iteration that picks up calls beyond the
  expansion limit.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  FASTEST-tier expansion: lengths 0..5  # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def test_empty(self) -> None:
    """A variadic-only overload matches a zero-arg call via the
    expanded 'TypeSig()' entry."""
    collector = IntCollector()
    self.assertEqual(collector.nums, ())

  def test_one_int(self) -> None:
    """A single-arg call matches the expanded 'TypeSig(int)' entry."""
    collector = IntCollector(69)
    self.assertEqual(collector.nums, (69,))

  def test_three_ints(self) -> None:
    """A three-arg call within the expansion limit hits FASTEST."""
    collector = IntCollector(1, 2, 3)
    self.assertEqual(collector.nums, (1, 2, 3))

  def test_five_ints(self) -> None:
    """A call at the exact expansion limit (5) still hits FASTEST."""
    collector = IntCollector(1, 2, 3, 4, 5)
    self.assertEqual(collector.nums, (1, 2, 3, 4, 5))

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  FAST-tier variadic catcher: lengths beyond the limit  # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def test_six_ints(self) -> None:
    """A six-arg call exceeds the expansion; the FAST variadic
    iteration picks it up."""
    collector = IntCollector(1, 2, 3, 4, 5, 6)
    self.assertEqual(collector.nums, (1, 2, 3, 4, 5, 6))

  def test_ten_ints(self) -> None:
    """A ten-arg call demonstrates the variadic catcher handles
    arbitrarily long tails."""
    args = tuple(range(10))
    collector = IntCollector(*args)
    self.assertEqual(collector.nums, args)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Prefix + variadic  # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def test_prefix_only(self) -> None:
    """The prefix-only call matches the expanded 'TypeSig(str)'
    entry - the zero-tail expansion of '(str, *ARGS[int])'."""
    collector = PrefixedCollector('alpha')
    self.assertEqual(collector.name, 'alpha')
    self.assertEqual(collector.nums, ())

  def test_prefix_with_ints(self) -> None:
    """Prefix plus a short int tail hits FASTEST via the expansion."""
    collector = PrefixedCollector('beta', 10, 20, 30)
    self.assertEqual(collector.name, 'beta')
    self.assertEqual(collector.nums, (10, 20, 30))

  def test_prefix_with_long_tail(self) -> None:
    """Prefix plus an int tail exceeding the expansion limit falls
    into the variadic catcher."""
    collector = PrefixedCollector('gamma', 1, 2, 3, 4, 5, 6, 7)
    self.assertEqual(collector.name, 'gamma')
    self.assertEqual(collector.nums, (1, 2, 3, 4, 5, 6, 7))

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Explicit override of an expanded entry  # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def test_override_two_int_case(self) -> None:
    """A subsequent explicit '@overload(str, int, int)' overwrites
    the '(str, int, int)' entry the variadic expansion populated.
    The two-int call therefore routes to the explicit overload, not
    to the variadic function."""
    collector = MixedCollector('delta', 7, 8)
    self.assertEqual(collector.kind, 'pair')
    self.assertEqual(collector.nums, (7, 8))

  def test_other_lengths_still_variadic(self) -> None:
    """Lengths the explicit override does not cover still resolve
    to the variadic function - both within the FASTEST expansion
    and via the variadic catcher."""
    one = MixedCollector('eps', 1)
    three = MixedCollector('zeta', 1, 2, 3)
    seven = MixedCollector('eta', 1, 2, 3, 4, 5, 6, 7)
    self.assertEqual(one.kind, 'variadic')
    self.assertEqual(three.kind, 'variadic')
    self.assertEqual(seven.kind, 'variadic')

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Negative paths  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def test_wrong_type_in_tail_raises(self) -> None:
    """A non-int in the tail position breaks the variadic match
    (and the FASTEST/FAST tiers have no matching signature), so the
    dispatcher falls through to FALLBACK or raises
    'DispatchException'."""
    with self.assertRaises(DispatchException):
      _ = IntCollector(1, 2, 'three', 4)

  def test_wrong_prefix_type_raises(self) -> None:
    """A non-str in the prefix position breaks both the FASTEST
    expansion (no '(int, int)' entry) and the variadic catcher
    (prefix isinstance fails)."""
    with self.assertRaises(DispatchException):
      _ = PrefixedCollector(123, 4, 5, 6, 7, 8, 9)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Subclass matching via isinstance  # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def test_bool_matches_int_variadic(self) -> None:
    """'bool' is a subclass of 'int', so a 'True' in the variadic
    tail passes 'isinstance(arg, int)' and matches. Within the
    expansion limit, this still goes through FAST (since
    'TypeSig(bool)' is not in the FASTEST dict)."""
    collector = IntCollector(True, False, True)
    self.assertEqual(collector.nums, (True, False, True))

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Coverage for the rarely-exercised dispatch branches  # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def test_prefix_too_short_raises(self) -> None:
    """A prefixed variadic overload with prefix length 1 cannot
    match a zero-arg call: every concrete expansion entry has
    length at least 1, and both the FAST and SLOW variadic loops
    short-circuit via 'len(args) < len(prefix)'. With no fallback,
    the call must raise 'DispatchException'."""
    with self.assertRaises(DispatchException):
      _ = PrefixedCollector()

  def test_slow_variadic_tail_cast(self) -> None:
    """When the prefix isinstance-matches but the tail args need
    'typeCast' to reach the variadic inner type, dispatch reaches
    the SLOW variadic tier. The prefix isinstance-true branch
    inside SLOW variadic appends the prefix args directly, and the
    tail loop casts each string to 'int' before forwarding."""
    collector = PrefixedCollector(
      'alpha', '1', '2', '3', '4', '5', '6', '7',
    )
    self.assertEqual(collector.name, 'alpha')
    self.assertEqual(collector.nums, (1, 2, 3, 4, 5, 6, 7))

  def test_strict_variadic_rejects_cast(self) -> None:
    """A strict variadic overload ('strict=True') has
    '__allow_flex__ = False' on every expansion entry and on the
    variadic sig itself. A call with arg types that would only
    match via 'typeCast' is rejected at the SLOW variadic tier
    (the 'not sig.__allow_flex__' continue), since the strict flag
    forbids coercion."""
    with self.assertRaises(DispatchException):
      _ = StrictCollector('1', '2', '3')

  def test_strict_variadic_accepts_exact_types(self) -> None:
    """A strict variadic still dispatches correctly when the
    arguments are exact-type matches. The strict flag only blocks
    'typeCast' coercion in the SLOW tier; FASTEST and FAST
    isinstance matching continue to work."""
    short = StrictCollector(1, 2, 3)
    long_ = StrictCollector(1, 2, 3, 4, 5, 6, 7)
    self.assertEqual(short.nums, (1, 2, 3))
    self.assertEqual(long_.nums, (1, 2, 3, 4, 5, 6, 7))

  def test_clone_copies_variadics(self) -> None:
    """'Dispatcher.clone' must also copy the variadic-function
    list. Without the copy, a clone of a Dispatcher carrying a
    variadic overload would silently lose the long-tail catcher."""
    original = Dispatcher()
    variadicSig = TypeSig(ARGS[int])

    def func(self_, *nums) -> None:
      """variadic body"""

    # noinspection PyTypeChecker
    original.addVariadicSigFunc(variadicSig, func)
    clone = original.clone()
    self.assertEqual(
      clone._getVariadicFuncs(), original._getVariadicFuncs(),
    )
    self.assertIsNot(
      clone._getVariadicFuncs(), original._getVariadicFuncs(),
    )

  def test_dual_variadic_under_same_name(self) -> None:
    """Two '@overload(*ARGS[T])' decorators on the same method name
    register two variadics under one key in the namespace's
    variadic map. The second 'addVariadic' call finds the name
    already present and appends to the existing list rather than
    initializing a new one. Both variadics must dispatch
    correctly: long int tails route to the int variadic, long str
    tails route to the str variadic."""
    obj = DualVariadic()
    self.assertEqual(obj.collect(1, 2, 3, 4, 5, 6, 7), 'int')
    self.assertEqual(obj.collect('a', 'b', 'c', 'd', 'e', 'f', 'g'), 'str')

  def test_child_inherits_parent_variadic(self) -> None:
    """A 'BaseObject' subclass of a class with a variadic overload
    must inherit that variadic. 'BaseSpace.__init__' walks the
    parent's namespace, calls 'getVariadics' on it, and re-
    registers each '(name, sig, func)' pair on the child's own
    variadic map."""
    child = ChildOfParentVariadic()
    self.assertEqual(child.collect(1, 2, 3, 4, 5, 6, 7), 'parent-int')

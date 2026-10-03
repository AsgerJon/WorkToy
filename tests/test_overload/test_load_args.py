"""
TestLoadARGS exercises the variadic '*ARGS[T]' overload syntax. A trailing
'ARGS' sentinel makes the signature a variadic declaration, which the
dispatcher holds once and matches at any length: by exact type first, the
prefix and the one type the trailing arguments share as a hash key, then
through 'isinstance', then through casts. These tests cover calls of
every length and the interaction with explicit declarations.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core.sentinels import ARGS
from worktoy.dispatch import Dispatcher, TypeSig, overload
from worktoy.mcls import BaseObject
from worktoy.waitaminute.dispatch import DispatchException
from . import OverloadTest


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
  """Variadic plus an explicit declaration for the 2-int case, a call
  the variadic accepts as well. The explicit declaration takes that
  call, since a concrete signature is matched first."""

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
  """Two variadic overloads under the same method name. The second
  '@overload' registration finds 'collect' already in the namespace's
  variadic map and appends to the existing list rather than creating a
  new entry. Both variadics accept the empty call, so the explicit
  '@overload()' declaration settles which function receives it;
  without it, class creation raises 'DuplicateSignature' for the
  ambiguous empty signature."""

  @overload(*ARGS[int])
  def collect(self, *nums: int) -> str:
    return 'int'

  @overload(*ARGS[str])
  def collect(self, *names: str) -> str:
    return 'str'

  @overload()
  def collect(self) -> str:
    return 'empty'


class ParentWithVariadic(BaseObject):
  """Parent class registering a variadic overload that
  'ChildOfParentVariadic' should inherit when its class is created."""

  @overload(*ARGS[int])
  def collect(self, *nums: int) -> str:
    return 'parent-int'


class ChildOfParentVariadic(ParentWithVariadic):
  """Empty body. When the class compiles, its namespace walks the
  method resolution order and collects the variadic registration from
  the namespace of 'ParentWithVariadic'."""


class TestLoadARGS(OverloadTest):
  """
  TestLoadARGS covers the exact-type matching of '*ARGS[T]' at every
  length and the 'isinstance' and cast passes that pick up the calls
  exact type does not match.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Exact type, short calls  # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def test_empty(self) -> None:
    """A variadic-only overload matches a zero-arg call."""
    collector = IntCollector()
    self.assertEqual(collector.nums, ())

  def test_one_int(self) -> None:
    """A single-arg call matches."""
    collector = IntCollector(69)
    self.assertEqual(collector.nums, (69,))

  def test_three_ints(self) -> None:
    """A three-arg call matches."""
    collector = IntCollector(1, 2, 3)
    self.assertEqual(collector.nums, (1, 2, 3))

  def test_five_ints(self) -> None:
    """A five-arg call matches."""
    collector = IntCollector(1, 2, 3, 4, 5)
    self.assertEqual(collector.nums, (1, 2, 3, 4, 5))

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Exact type, long calls  # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def test_six_ints(self) -> None:
    """A six-arg call matches as the shorter ones do."""
    collector = IntCollector(1, 2, 3, 4, 5, 6)
    self.assertEqual(collector.nums, (1, 2, 3, 4, 5, 6))

  def test_ten_ints(self) -> None:
    """A ten-arg call demonstrates that the one signature handles
    arbitrarily long tails."""
    args = tuple(range(10))
    collector = IntCollector(*args)
    self.assertEqual(collector.nums, args)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Prefix + variadic  # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def test_prefix_only(self) -> None:
    """The prefix-only call matches, with nothing after the prefix."""
    collector = PrefixedCollector('alpha')
    self.assertEqual(collector.name, 'alpha')
    self.assertEqual(collector.nums, ())

  def test_prefix_with_ints(self) -> None:
    """Prefix plus a short int tail matches."""
    collector = PrefixedCollector('beta', 10, 20, 30)
    self.assertEqual(collector.name, 'beta')
    self.assertEqual(collector.nums, (10, 20, 30))

  def test_prefix_with_long_tail(self) -> None:
    """Prefix plus a long int tail matches as well."""
    collector = PrefixedCollector('gamma', 1, 2, 3, 4, 5, 6, 7)
    self.assertEqual(collector.name, 'gamma')
    self.assertEqual(collector.nums, (1, 2, 3, 4, 5, 6, 7))

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Explicit declaration of a call the variadic accepts  # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def test_override_two_int_case(self) -> None:
    """An explicit '@overload(str, int, int)' takes the two-int call,
    which the variadic accepts as well, since a concrete signature is
    matched first."""
    collector = MixedCollector('delta', 7, 8)
    self.assertEqual(collector.kind, 'pair')
    self.assertEqual(collector.nums, (7, 8))

  def test_other_lengths_still_variadic(self) -> None:
    """Lengths the explicit declaration does not cover still resolve
    to the variadic function, short and long alike."""
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
    """A non-int in the tail position breaks the variadic match in every
    pass, so the dispatcher falls through to FALLBACK or raises
    'DispatchException'."""
    with self.assertRaises(DispatchException):
      _ = IntCollector(1, 2, 'three', 4)

  def test_wrong_prefix_type_raises(self) -> None:
    """A non-str in the prefix position breaks the variadic match by
    exact type and by 'isinstance' alike."""
    with self.assertRaises(DispatchException):
      _ = PrefixedCollector(123, 4, 5, 6, 7, 8, 9)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Subclass matching via isinstance  # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def test_bool_matches_int_variadic(self) -> None:
    """'bool' is a subclass of 'int', so a 'True' in the variadic
    tail passes 'isinstance(arg, int)' and matches, through the FAST
    pass, since 'bool' is not 'int' by exact type."""
    collector = IntCollector(True, False, True)
    self.assertEqual(collector.nums, (True, False, True))

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Coverage for the rarely-exercised dispatch branches  # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def test_prefix_too_short_raises(self) -> None:
    """A prefixed variadic overload with prefix length 1 cannot
    match a zero-arg call: every pass short-circuits on a call shorter
    than the prefix. With no fallback, the call must raise
    'DispatchException'."""
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
    '__allow_flex__ = False' on its signature. A call with arg types
    that would only match via 'typeCast' is rejected at the SLOW
    variadic tier (the 'not sig.__allow_flex__' continue), since the
    strict flag forbids coercion."""
    with self.assertRaises(DispatchException):
      _ = StrictCollector('1', '2', '3')

  def test_strict_variadic_accepts_exact_types(self) -> None:
    """A strict variadic still dispatches correctly when the
    arguments are exact-type matches, short and long. The strict flag
    only blocks 'typeCast' coercion in the SLOW tier; the exact-type
    and 'isinstance' matching continue to work."""
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

  def test_clone_dispatches_variadics(self) -> None:
    """A clone of a 'Dispatcher' carrying a variadic overload must
    dispatch through it once placed on a class, both for calls matching
    without a cast and for calls that need one. The clone therefore has
    to carry everything the variadic passes consult, not only the
    signature list itself."""
    original = Dispatcher()

    def func(self_, *nums) -> str:
      """variadic body"""
      return 'variadic'

    # noinspection PyTypeChecker
    original.addVariadicSigFunc(TypeSig(ARGS[int]), func)

    class Host:
      """Host receives the clone as an ordinary class attribute."""
      collect = original.clone()

    self.assertEqual(Host().collect(1, 2, 3), 'variadic')
    self.assertEqual(Host().collect('1', '2', '3'), 'variadic')

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
    self.assertEqual(obj.collect(), 'empty')

  def test_child_inherits_parent_variadic(self) -> None:
    """A 'BaseObject' subclass of a class with a variadic overload
    must inherit that variadic. 'BaseSpace.collectVariadics' walks the
    method resolution order and collects the '(sig, func)' pair from
    the parent's namespace into the child's 'Dispatcher'."""
    child = ChildOfParentVariadic()
    self.assertEqual(child.collect(1, 2, 3, 4, 5, 6, 7), 'parent-int')

"""
TestVariadicPrefixOverlap pins the collision semantics for overload
registrations accepting one call. Two variadic declarations sharing a
prefix both accept the prefix-only call by exact type, and with nothing
settling which function receives that call, class creation raises
'DuplicateSignature'. An explicit declaration of the contested signature
settles the ambiguity regardless of declaration order, a plain method
definition of the same name in the same class body raises
'OverloadConflict' rather than settling it, two explicit declarations of
the same signature with different functions raise immediately, and
inherited registrations always lose to the class body's own.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core.sentinels import ARGS
from worktoy.dispatch import overload
from worktoy.mcls import BaseObject
from worktoy.waitaminute.dispatch import DuplicateSignature
from worktoy.waitaminute.meta import OverloadConflict
from . import OverloadTest


def _sharedExplicit(self, n: int) -> str:
  """Module-level function bound twice in 'RepeatedExplicit', so the
  repeated explicit registration carries the same function object and
  passes without complaint."""
  return 'shared'


class ExplicitAfter(BaseObject):
  """ExplicitAfter settles the contested empty-tail signature with an
  explicit declaration after both variadics."""

  @overload(int, *ARGS[str])
  def f(self, n: int, *tail: str) -> str:
    return 'strs'

  @overload(int, *ARGS[int])
  def f(self, n: int, *tail: int) -> str:
    return 'ints'

  @overload(int)
  def f(self, n: int) -> str:
    return 'explicit'


class ExplicitBetween(BaseObject):
  """ExplicitBetween settles the contested signature with an explicit
  declaration between the two variadics."""

  @overload(int, *ARGS[str])
  def f(self, n: int, *tail: str) -> str:
    return 'strs'

  @overload(int)
  def f(self, n: int) -> str:
    return 'explicit'

  @overload(int, *ARGS[int])
  def f(self, n: int, *tail: int) -> str:
    return 'ints'


class StackedVariadics(BaseObject):
  """StackedVariadics stacks two variadic declarations on one
  function, so the call both accept has one receiver and no ambiguity
  arises."""

  @overload(int, *ARGS[str])
  @overload(int, *ARGS[int])
  def f(self, n: int, *tail) -> str:
    return 'both'


class RepeatedExplicit(BaseObject):
  """RepeatedExplicit registers the same function object explicitly
  under the same signature twice."""

  f = overload(int)(_sharedExplicit)
  f = overload(int)(_sharedExplicit)  # noqa: F811


def _sharedVariadic(self, n: int, *tail) -> str:
  """Module-level function bound through two separate variadic
  wrappers in 'RepeatedVariadic', so the prefix-only call both accept
  has one receiving function."""
  return 'shared-variadic'


class RepeatedVariadic(BaseObject):
  """RepeatedVariadic registers the same function object through two
  variadic wrappers both accepting the prefix-only call. Agreeing on
  the function, the overlap raises nothing."""

  f = overload(int, *ARGS[str])(_sharedVariadic)
  f = overload(int, *ARGS[int])(_sharedVariadic)  # noqa: F811


class ExplicitPosition(BaseObject):
  """ExplicitPosition declares a variadic over 'object', then an explicit
  'int', then an explicit 'object', a call the variadic accepts as well.
  The explicit declaration takes the place its own declaration gives
  it, after 'int', rather than the earlier place of the variadic."""

  @overload(object, *ARGS[object])
  def f(self, *items: object) -> str:
    return 'variadic'

  @overload(int)
  def f(self, n: int) -> str:
    return 'int'

  @overload(object)
  def f(self, item: object) -> str:
    return 'object'


class Root(BaseObject):
  """Root declares the overload that the inheritance fixtures below
  receive, merge, and override."""

  @overload(int)
  def g(self, n: int) -> str:
    return 'root'


class LeftBranch(Root):
  """LeftBranch passes Root's overloads through unchanged."""

  pass


class RightBranch(Root):
  """RightBranch passes Root's overloads through unchanged."""

  pass


class Diamond(LeftBranch, RightBranch):
  """Diamond merges the same inherited registration from both
  branches, colliding inherited with inherited."""

  pass


class OverrideChild(Root):
  """OverrideChild redeclares the inherited signature, displacing the
  inherited registration with its own."""

  @overload(int)
  def g(self, n: int) -> str:
    return 'child'


class TestVariadicPrefixOverlap(OverloadTest):
  """
  TestVariadicPrefixOverlap provides tests for the collision semantics
  of overload signatures accepting one call, across variadic
  declarations, explicit declarations, plain overrides, and inheritance.
  """

  def test_ambiguous_prefix_raises(self) -> None:
    """
    Testing that two variadic declarations sharing a prefix with no
    explicit declaration of the contested signature raise
    'DuplicateSignature' at class creation.
    """
    with self.assertRaises(DuplicateSignature):
      class Ambiguous(BaseObject):
        @overload(int, *ARGS[str])
        def f(self, n: int, *tail: str) -> str:
          return 'strs'  # pragma: no cover

        @overload(int, *ARGS[int])
        def f(self, n: int, *tail: int) -> str:
          return 'ints'  # pragma: no cover

  def test_settling_one_ambiguity_keeps_others(self) -> None:
    """
    Testing that an explicit declaration settles only the ambiguity of
    its own name. Both 'f' and 'g' leave the prefix-only signature
    ambiguous, and only 'g' receives an explicit declaration of it, so
    class creation still raises 'DuplicateSignature' for 'f'.
    """
    with self.assertRaises(DuplicateSignature):
      class HalfSettled(BaseObject):
        @overload(int, *ARGS[str])
        def f(self, n: int, *tail: str) -> str:
          return 'strs'  # pragma: no cover

        @overload(int, *ARGS[int])
        def f(self, n: int, *tail: int) -> str:
          return 'ints'  # pragma: no cover

        @overload(int, *ARGS[str])
        def g(self, n: int, *tail: str) -> str:
          return 'strs'  # pragma: no cover

        @overload(int, *ARGS[int])
        def g(self, n: int, *tail: int) -> str:
          return 'ints'  # pragma: no cover

        @overload(int)
        def g(self, n: int) -> str:
          return 'explicit'  # pragma: no cover

  def test_explicit_settles_regardless_of_order(self) -> None:
    """
    Testing that an explicit declaration of the contested signature
    settles the ambiguity whether it appears after or between the
    variadic declarations.
    """
    for cls in (ExplicitAfter, ExplicitBetween):
      obj = cls()
      self.assertEqual(obj.f(1), 'explicit')
      self.assertEqual(obj.f(1, 'x'), 'strs')
      self.assertEqual(obj.f(1, 2), 'ints')

  def test_explicit_takes_declaration_position(self) -> None:
    """
    Testing that an explicit declaration of a call a variadic
    declaration accepts as well is tried at its own place in declaration
    order. A 'bool' matches both 'int' and 'object' only through
    'isinstance', and 'int' was declared first, so it receives the call.
    """
    obj = ExplicitPosition()
    self.assertEqual(obj.f(True), 'int')
    self.assertEqual(obj.f('x'), 'object')
    self.assertEqual(obj.f(1, 2), 'variadic')

  def test_stacked_variadics_share_function(self) -> None:
    """
    Testing that stacking two variadic declarations on one function
    raises nothing, since the call both accept has one receiving
    function.
    """
    obj = StackedVariadics()
    self.assertEqual(obj.f(1), 'both')
    self.assertEqual(obj.f(1, 'x'), 'both')
    self.assertEqual(obj.f(1, 2), 'both')

  def test_plain_definition_refused(self) -> None:
    """
    Testing that a plain definition of a name the class body has
    overloaded does not settle an ambiguity by dropping the overloads,
    but raises 'OverloadConflict' at the plain definition.
    """
    with self.assertRaises(OverloadConflict):
      class PlainAfterAmbiguity(BaseObject):
        @overload(int, *ARGS[str])
        def f(self, n: int, *tail: str) -> str:
          return 'strs'  # pragma: no cover

        @overload(int, *ARGS[int])
        def f(self, n: int, *tail: int) -> str:
          return 'ints'  # pragma: no cover

        def f(self, *args) -> str:  # noqa: F811
          return 'plain'  # pragma: no cover

  def test_repeated_explicit_same_function(self) -> None:
    """
    Testing that explicitly registering the same function object under
    the same signature twice passes without complaint.
    """
    obj = RepeatedExplicit()
    self.assertEqual(obj.f(1), 'shared')

  def test_repeated_variadic_same_function(self) -> None:
    """
    Testing that two variadic wrappers around the same function object
    accept the prefix-only call alike without raising, since both name
    the same receiver.
    """
    obj = RepeatedVariadic()
    self.assertEqual(obj.f(1), 'shared-variadic')
    self.assertEqual(obj.f(1, 'x'), 'shared-variadic')
    self.assertEqual(obj.f(1, 2), 'shared-variadic')

  def test_explicit_duplicate_raises(self) -> None:
    """
    Testing that two explicit declarations of the same signature with
    different functions raise 'DuplicateSignature' immediately.
    """
    with self.assertRaises(DuplicateSignature):
      class Duplicated(BaseObject):
        @overload(int)
        def f(self, n: int) -> str:
          return 'first'  # pragma: no cover

        @overload(int)
        def f(self, n: int) -> str:
          return 'second'  # pragma: no cover

  def test_diamond_inherited_merge(self) -> None:
    """
    Testing that the same registration arriving through both branches
    of a diamond merges silently and dispatches to the root function.
    """
    self.assertEqual(Diamond().g(1), 'root')

  def test_subclass_overrides_inherited(self) -> None:
    """
    Testing that a subclass redeclaring an inherited signature
    displaces the inherited registration without complaint, leaving
    the parent untouched.
    """
    self.assertEqual(OverrideChild().g(1), 'child')
    self.assertEqual(Root().g(1), 'root')

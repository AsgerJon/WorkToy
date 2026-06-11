"""
TestVariadicPrefixOverlap pins the collision semantics for overload
registrations of equal signatures. Two variadic declarations sharing a
prefix both expand a concrete signature for the prefix-only call, and
with nothing settling which function receives that call, class
creation raises 'DuplicateSignature'. An explicit declaration of the
contested signature settles the ambiguity regardless of declaration
order, a plain method definition overrides the name entirely, two
explicit declarations of the same signature with different functions
raise immediately, and inherited registrations always lose to the
class body's own.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core.sentinels import ARGS
from worktoy.dispatch import overload
from worktoy.mcls import BaseObject
from worktoy.waitaminute.dispatch import DuplicateSignature
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
  function, so their overlapping expansions agree and no ambiguity
  arises."""

  @overload(int, *ARGS[str])
  @overload(int, *ARGS[int])
  def f(self, n: int, *tail) -> str:
    return 'both'


class PlainOverridesAmbiguity(BaseObject):
  """PlainOverridesAmbiguity declares two ambiguous variadics and then
  overrides the name with a plain definition, which drops every
  overload registration along with the ambiguity."""

  @overload(int, *ARGS[str])
  def f(self, n: int, *tail: str) -> str:
    return 'strs'  # pragma: no cover

  @overload(int, *ARGS[int])
  def f(self, n: int, *tail: int) -> str:
    return 'ints'  # pragma: no cover

  def f(self, *args) -> str:  # noqa: F811
    return 'plain'


class RepeatedExplicit(BaseObject):
  """RepeatedExplicit registers the same function object explicitly
  under the same signature twice."""

  f = overload(int)(_sharedExplicit)
  f = overload(int)(_sharedExplicit)  # noqa: F811


def _sharedVariadic(self, n: int, *tail) -> str:
  """Module-level function bound through two separate variadic
  wrappers in 'RepeatedVariadic', so their colliding prefix-only
  expansions agree on the receiving function."""
  return 'shared-variadic'


class RepeatedVariadic(BaseObject):
  """RepeatedVariadic registers the same function object through two
  variadic wrappers whose expansions collide on the prefix-only
  signature. Agreeing on the function, the collision raises nothing."""

  f = overload(int, *ARGS[str])(_sharedVariadic)
  f = overload(int, *ARGS[int])(_sharedVariadic)  # noqa: F811


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
  of equal overload signatures across variadic expansions, explicit
  declarations, plain overrides, and inheritance.
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

  def test_stacked_variadics_share_function(self) -> None:
    """
    Testing that stacking two variadic declarations on one function
    raises nothing, since the overlapping expansions agree on the
    receiving function.
    """
    obj = StackedVariadics()
    self.assertEqual(obj.f(1), 'both')
    self.assertEqual(obj.f(1, 'x'), 'both')
    self.assertEqual(obj.f(1, 2), 'both')

  def test_plain_definition_overrides(self) -> None:
    """
    Testing that a plain definition of the name drops the ambiguous
    registrations entirely, so the class creates and the plain
    definition receives every call.
    """
    obj = PlainOverridesAmbiguity()
    self.assertEqual(obj.f(1), 'plain')
    self.assertEqual(obj.f(1, 'x', 2.5), 'plain')

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
    collide on the prefix-only signature without raising, since both
    name the same receiver.
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

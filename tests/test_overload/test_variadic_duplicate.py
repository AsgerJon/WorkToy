"""
TestVariadicDuplicate subclasses 'OverloadTest' and pins that one class
body declaring the same variadic signature twice under a name, with
different functions, raises 'DuplicateSignature' at the second
declaration, as an equal concrete signature does. The second declaration
used to be recorded and then dropped without a word when the
registrations were collected, so the first function took every call.
A subclass may redeclare an inherited variadic signature, and different
variadic signatures that overlap remain no conflict.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core.sentinels import ARGS
from worktoy.dispatch import overload, TypeSig
from worktoy.mcls import BaseObject
from worktoy.waitaminute.dispatch import DuplicateSignature

from . import OverloadTest


class Parent(BaseObject):
  """Parent declares a variadic signature."""

  @overload(ARGS[int])
  def put(self, *args) -> str:
    return 'parent'


class Child(Parent):
  """Child redeclares the variadic signature it inherits."""

  @overload(ARGS[int])
  def put(self, *args) -> str:
    return 'child'


class WideFirst(BaseObject):
  """WideFirst declares 'ARGS[int]' before '(int, ARGS[int])'."""

  @overload(ARGS[int])
  def put(self, *args) -> str:
    return 'wide'

  @overload(int, ARGS[int])
  def put(self, *args) -> str:
    return 'prefixed'


class PrefixedFirst(BaseObject):
  """PrefixedFirst declares '(int, ARGS[int])' before 'ARGS[int]'."""

  @overload(int, ARGS[int])
  def put(self, *args) -> str:
    return 'prefixed'

  @overload(ARGS[int])
  def put(self, *args) -> str:
    return 'wide'


class TestVariadicDuplicate(OverloadTest):
  """
  TestVariadicDuplicate provides tests for a variadic signature declared
  more than once.
  """

  def test_different_function_refused(self) -> None:
    """A second equal variadic signature bound to another function raises
    'DuplicateSignature', naming the signature and both functions."""
    with self.assertRaises(DuplicateSignature) as context:
      class Foo(BaseObject):
        @overload(ARGS[int])
        def bar(self, *args) -> str:
          return 'first'

        @overload(ARGS[int])
        def bar(self, *args) -> str:
          return 'second'

    e = context.exception
    self.assertEqual(e.sig, TypeSig(ARGS[int]))
    self.assertEqual(e.existing(None), 'first')
    self.assertEqual(e.duplicate(None), 'second')

  def test_same_signature_stacked(self) -> None:
    """The same variadic signature stacked twice on one function is no
    duplicate."""

    class Bag(BaseObject):
      @overload(ARGS[int])
      @overload(ARGS[int])
      def put(self, *args) -> int:
        return len(args)

    self.assertEqual(Bag().put(1, 2, 3), 3)

  def test_subclass_redeclares(self) -> None:
    """A subclass may redeclare an inherited variadic signature; the
    nearest class takes the call."""
    self.assertEqual(Child().put(1, 2), 'child')
    self.assertEqual(Parent().put(1, 2), 'parent')

  def test_overlapping_signatures(self) -> None:
    """Different variadic signatures accepting one call are no conflict:
    the most recent declaration takes it."""
    self.assertEqual(WideFirst().put(1, 2), 'prefixed')
    self.assertEqual(PrefixedFirst().put(1, 2), 'wide')

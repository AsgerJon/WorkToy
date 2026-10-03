"""
TestDuplicateFallback subclasses 'OverloadTest' and pins that one class
body may register only one fallback and one finalizer under a name. A
second one used to replace the first without a word, where two explicit
declarations of one signature raise; it now raises 'DuplicateSignature'
too, naming the role, 'fallback' or 'finalizer', in place of a
signature. The same function registered again changes nothing, and a
subclass may still replace the fallback or the finalizer it inherits.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.dispatch import overload
from worktoy.mcls import BaseObject
from worktoy.waitaminute.dispatch import DuplicateSignature

from . import OverloadTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class TestDuplicateFallback(OverloadTest):
  """
  TestDuplicateFallback provides tests for a second fallback or finalizer
  in one class body.
  """

  def test_second_fallback_refused(self) -> None:
    """A second fallback under one name raises 'DuplicateSignature',
    naming both functions and the role."""
    with self.assertRaises(DuplicateSignature) as context:
      class Foo(BaseObject):
        @overload.fallback
        def bar(self, *args: Any) -> str:
          return 'first'  # pragma: no cover

        @overload.fallback
        def bar(self, *args: Any) -> str:
          return 'second'  # pragma: no cover
    e = context.exception
    self.assertEqual(e.sig, 'fallback')
    self.assertEqual(e.existing.__name__, 'bar')
    self.assertIsNot(e.existing, e.duplicate)
    self.assertIn('already has a fallback function registered', str(e))
    self.assertEqual(str(e), repr(e))

  def test_second_finalizer_refused(self) -> None:
    """A second finalizer under one name raises 'DuplicateSignature',
    naming the role."""
    with self.assertRaises(DuplicateSignature) as context:
      class Foo(BaseObject):
        @overload.finalize
        def bar(self, *args: Any) -> None:
          pass  # pragma: no cover

        @overload.finalize
        def bar(self, *args: Any) -> None:
          pass  # pragma: no cover
    self.assertEqual(context.exception.sig, 'finalizer')
    info = str(context.exception)
    self.assertIn('already has a finalizer function registered', info)

  def test_same_function_again(self) -> None:
    """The same fallback bound again under its own name changes
    nothing."""

    class Foo(BaseObject):
      @overload.fallback
      def bar(self, *args: Any) -> str:
        return 'fallback'

      bar = bar

    self.assertEqual(Foo().bar(1, 2), 'fallback')

  def test_subclass_replaces_inherited(self) -> None:
    """A subclass registering its own fallback and finalizer replaces the
    inherited ones."""
    calls = []

    class Parent(BaseObject):
      @overload.fallback
      def bar(self, *args: Any) -> str:
        return 'parent'  # pragma: no cover

      @overload.finalize
      def bar(self, *args: Any) -> None:
        calls.append('parent')  # pragma: no cover

    class Child(Parent):
      @overload.fallback
      def bar(self, *args: Any) -> str:
        return 'child'

      @overload.finalize
      def bar(self, *args: Any) -> None:
        calls.append('child')

    self.assertEqual(Child().bar(), 'child')
    self.assertEqual(calls, ['child'])

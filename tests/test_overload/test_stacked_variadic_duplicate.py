"""
TestStackedVariadicDuplicate subclasses 'OverloadTest' and pins that an
explicit signature stacked on a variadic one counts as an explicit
declaration whichever of the two decorators comes first, beside the
variadic declaration held as written. Stacked above the variadic, the
explicit signature used to be stored under a signature expanded from the
variadic, marked as an expansion, so a later explicit declaration of the
same signature displaced it without a word, where the other order raised
'DuplicateSignature'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core.sentinels import ARGS
from worktoy.dispatch import overload, TypeSig
from worktoy.mcls import BaseObject
from worktoy.waitaminute.dispatch import DuplicateSignature

from . import OverloadTest


class TestStackedVariadicDuplicate(OverloadTest):
  """
  TestStackedVariadicDuplicate provides tests for an explicit signature
  stacked on a variadic one.
  """

  def test_explicit_above_is_explicit(self) -> None:
    """The explicit signature stacked above a variadic one is held by the
    'overload' as a concrete declaration, beside the variadic one."""
    ov = overload(int)(overload(ARGS[int])(lambda self, *args: args))
    self.assertEqual([sig for sig, _ in ov], [TypeSig(int)])
    self.assertEqual([sig for sig, _ in ov.getVariadics()],
                     [TypeSig(ARGS[int])])

  def test_explicit_above_then_duplicate(self) -> None:
    """A later explicit declaration of the signature stacked above the
    variadic raises 'DuplicateSignature'."""
    with self.assertRaises(DuplicateSignature):
      class Foo(BaseObject):
        @overload(int)
        @overload(ARGS[int])
        def bar(self, *args) -> str:
          return 'A'  # pragma: no cover

        @overload(int)
        def bar(self, x: int) -> str:
          return 'B'  # pragma: no cover

  def test_explicit_below_then_duplicate(self) -> None:
    """With the decorators swapped, the later explicit declaration raises
    'DuplicateSignature' as well."""
    with self.assertRaises(DuplicateSignature):
      class Foo(BaseObject):
        @overload(ARGS[int])
        @overload(int)
        def bar(self, *args) -> str:
          return 'A'  # pragma: no cover

        @overload(int)
        def bar(self, x: int) -> str:
          return 'B'  # pragma: no cover

  def test_same_signature_stacked_twice(self) -> None:
    """The same explicit signature stacked twice on one function is kept
    once, as an explicit declaration, and in the place it first took."""
    ov = overload(int)(overload(float)(overload(int)(lambda self, x: x)))
    sigs = [sig for sig, _ in ov]
    self.assertEqual(sigs, [TypeSig(int), TypeSig(float)])

  def test_stacked_dispatches_every_length(self) -> None:
    """The stacked function still takes calls of every length, the one
    the explicit signature names included."""

    class Foo(BaseObject):
      @overload(int)
      @overload(ARGS[int])
      def bar(self, *args) -> tuple:
        return args

    foo = Foo()
    self.assertEqual(foo.bar(), ())
    self.assertEqual(foo.bar(1), (1,))
    self.assertEqual(foo.bar(*range(9)), (*range(9),))

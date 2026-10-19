"""
TestTypeSigDeclaredTypes subclasses 'DispatcherTest' and pins that a
'TypeSig' keeps the types it was declared with beside the types it
dispatches on, so 'THIS' can be restored once 'swapTHIS' has replaced
it, and a clone of a placed 'Dispatcher' resolves 'THIS' to the class
the clone is placed on. 'swapTHIS' used to be the end of the sentinel, so
a clone made after placement carried the class of the original.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core.sentinels import ARGS, THIS
from worktoy.dispatch import Dispatcher, TypeSig, overload
from worktoy.mcls import BaseObject

from . import DispatcherTest


def _one(self, other) -> str:
  return type(other).__name__


class TestTypeSigDeclaredTypes(DispatcherTest):
  """
  TestTypeSigDeclaredTypes provides tests for the declared types of a
  'TypeSig' and for restoring 'THIS'.
  """

  def test_declared_kept_through_swap(self) -> None:
    """After 'swapTHIS' the raw types name the class and the declared
    types still name the sentinel."""
    sig = TypeSig(THIS, int, ARGS[THIS])
    sig.swapTHIS(str)
    self.assertEqual(sig.getRawTypes()[:2], (str, int))
    self.assertIs(sig.getRawTypes()[2].__inner_type__, str)
    self.assertEqual(sig.getDeclaredTypes()[:2], (THIS, int))
    self.assertIs(sig.getDeclaredTypes()[2].__inner_type__, THIS)

  def test_restore(self) -> None:
    """'restoreTHIS' puts the sentinel back, in place, and the signature
    hashes as declared again."""
    sig = TypeSig(THIS)
    declaredHash = hash(sig)
    sig.swapTHIS(int)
    self.assertNotEqual(hash(sig), declaredHash)
    sig.restoreTHIS()
    self.assertEqual(sig.getRawTypes(), (THIS,))
    self.assertEqual(hash(sig), declaredHash)

  def test_copy_is_declared(self) -> None:
    """A copy made by calling the signature carries the current types as
    its own declaration."""
    sig = TypeSig(THIS)
    sig.swapTHIS(int)
    copied = sig()
    self.assertEqual(copied.getDeclaredTypes(), (int,))

  def test_clone_keeps_class_by_default(self) -> None:
    """A clone of a placed dispatcher carries the class of the original,
    so a subclass may add a 'THIS' overload of its own beside it."""

    class First(BaseObject):
      @overload(THIS)
      def f(self, other: First) -> str:
        return type(other).__name__

    class Second:
      f = First.__dict__['f'].clone()

    secondSig, = Second.__dict__['f']._getDeclaredSigs()
    self.assertEqual(secondSig.getRawTypes(), (First,))
    self.assertEqual(secondSig.getDeclaredTypes(), (THIS,))

  def test_clone_restored_resolves_own_class(self) -> None:
    """A clone restored before placement resolves 'THIS' to its own
    class, and the original keeps its class."""

    class First(BaseObject):
      @overload(THIS)
      def f(self, other: First) -> str:
        return type(other).__name__

    clone = First.__dict__['f'].clone()
    clone.restoreTHIS()
    restoredSig, = clone._getDeclaredSigs()
    self.assertEqual(restoredSig.getRawTypes(), (THIS,))

    class Second:
      f = clone

    firstSig, = First.__dict__['f']._getDeclaredSigs()
    secondSig, = Second.__dict__['f']._getDeclaredSigs()
    self.assertEqual(firstSig.getRawTypes(), (First,))
    self.assertEqual(secondSig.getRawTypes(), (Second,))
    self.assertEqual(Second().f(Second()), 'Second')
    self.assertEqual(First().f(First()), 'First')

  def test_clone_keeps_flags(self) -> None:
    """The copied signatures keep whether casts are allowed."""
    dispatcher = Dispatcher()
    dispatcher.overload(THIS)(_one)
    dispatcher.overload(int, strict=False)(_one)
    clone = dispatcher.clone()
    strictSig, looseSig = clone._getDeclaredSigs()
    self.assertFalse(strictSig.__allow_flex__)
    self.assertTrue(looseSig.__allow_flex__)

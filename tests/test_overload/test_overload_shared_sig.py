"""
TestOverloadSharedSig subclasses 'OverloadTest' and pins that an
'overload' object bound in two unrelated class bodies resolves 'THIS' to
each class separately. The namespace used to register the very 'TypeSig'
objects the 'overload' holds, and naming the first class rewrote 'THIS'
in them in place, so the second class found 'THIS' already fixed to the
first.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core.sentinels import ARGS, THIS
from worktoy.dispatch import overload
from worktoy.mcls import BaseObject
from worktoy.waitaminute.dispatch import DispatchException

from . import OverloadTest


def _one(self, other) -> str:
  return type(other).__name__


def _many(self, *others) -> int:
  return len(others)


class TestOverloadSharedSig(OverloadTest):
  """
  TestOverloadSharedSig provides tests for one 'overload' object bound in
  two class bodies.
  """

  def test_each_class_resolves_this(self) -> None:
    """Each class dispatches on instances of itself, and the other's
    instances are refused."""
    shared = overload(THIS)(_one)

    class First(BaseObject):
      f = shared

    class Second(BaseObject):
      f = shared

    self.assertEqual(First().f(First()), 'First')
    self.assertEqual(Second().f(Second()), 'Second')
    with self.assertRaises(DispatchException):
      Second().f(First())
    firstSig, = First.__dict__['f']._getDeclaredSigs()
    secondSig, = Second.__dict__['f']._getDeclaredSigs()
    self.assertEqual(firstSig.getRawTypes(), (First,))
    self.assertEqual(secondSig.getRawTypes(), (Second,))

  def test_overload_keeps_sentinel(self) -> None:
    """The 'overload' object itself still holds 'THIS'."""
    shared = overload(THIS)(_one)

    class First(BaseObject):
      f = shared

    (sig, _), = [*shared]
    self.assertEqual(sig.getRawTypes(), (THIS,))

  def test_variadic_resolved_separately(self) -> None:
    """A variadic 'ARGS[THIS]' resolves per class as well."""
    shared = overload(ARGS[THIS])(_many)

    class First(BaseObject):
      f = shared

    class Second(BaseObject):
      f = shared

    self.assertEqual(First().f(First(), First()), 2)
    self.assertEqual(Second().f(Second()), 1)
    with self.assertRaises(DispatchException):
      Second().f(First())

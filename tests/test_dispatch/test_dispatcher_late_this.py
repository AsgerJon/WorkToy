"""
TestDispatcherLateThis subclasses 'DispatcherTest' and pins that a
'Dispatcher' already placed on a class resolves 'THIS' in a signature
registered afterwards, through 'Owner.__dict__[name]' as the '__get__'
docstring invites. 'THIS' used to be rewritten only as the class named
the dispatcher, so a later registration kept the sentinel and matched
nothing.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core.sentinels import ARGS, THIS
from worktoy.dispatch import Dispatcher, TypeSig

from . import DispatcherTest


def _one(self, other) -> str:
  return 'one'


def _many(self, *others) -> int:
  return len(others)


def _pair(self, other, n) -> tuple:
  return (type(other).__name__, n)


class TestDispatcherLateThis(DispatcherTest):
  """
  TestDispatcherLateThis provides tests for signatures registered on a
  placed 'Dispatcher'.
  """

  def test_late_concrete(self) -> None:
    """A concrete 'THIS' registered after placement names the owner."""

    class Hand:
      f = Dispatcher()

    dispatcher = Hand.__dict__['f']
    dispatcher.overload(THIS)(_one)
    sig, = dispatcher._getDeclaredSigs()
    self.assertEqual(sig.getRawTypes(), (Hand,))
    self.assertEqual(Hand().f(Hand()), 'one')

  def test_late_variadic(self) -> None:
    """A variadic 'ARGS[THIS]' registered after placement names the
    owner."""

    class Hand:
      f = Dispatcher()

    dispatcher = Hand.__dict__['f']
    dispatcher.addVariadicSigFunc(TypeSig(ARGS[THIS]), _many)
    sig, = dispatcher._getDeclaredSigs()
    self.assertIs(sig.getRawTypes()[-1].__inner_type__, Hand)
    self.assertEqual(Hand().f(Hand(), Hand()), 2)

  def test_late_flex(self) -> None:
    """A 'flex' registration after placement names the owner in every
    arrangement."""

    class Hand:
      f = Dispatcher()

    Hand.__dict__['f'].flex(THIS, int)(_pair)
    self.assertEqual(Hand().f(Hand(), 1), ('Hand', 1))
    self.assertEqual(Hand().f(1, Hand()), ('Hand', 1))

  def test_before_placement_unchanged(self) -> None:
    """A dispatcher not yet placed keeps 'THIS' until it is named."""
    dispatcher = Dispatcher()
    dispatcher.overload(THIS)(_one)
    sig, = dispatcher._getDeclaredSigs()
    self.assertEqual(sig.getRawTypes(), (THIS,))

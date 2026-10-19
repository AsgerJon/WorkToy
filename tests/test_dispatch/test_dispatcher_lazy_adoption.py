"""
TestDispatcherLazyAdoption subclasses 'DispatcherTest' and pins that a
'Dispatcher' installed on a finished class with 'setattr', which never
receives '__set_name__', adopts the class and the name it is held under
the first time it is read through that class. Such a dispatcher used to
fail at the first call with 'MissingVariable' for its field name, and a
'THIS' it registered stayed a sentinel.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core.sentinels import THIS
from worktoy.dispatch import Dispatcher
from worktoy.waitaminute import MissingVariable

from . import DispatcherTest


def _one(self, other) -> str:
  return type(other).__name__


def _num(self, n: int) -> int:
  return n


class TestDispatcherLazyAdoption(DispatcherTest):
  """
  TestDispatcherLazyAdoption provides tests for a dispatcher installed
  with 'setattr'.
  """

  def test_adopts_on_first_read(self) -> None:
    """A dispatcher set on a class after the fact takes the class and the
    name on first read, and 'THIS' resolves to the class."""

    class Owner:
      pass

    dispatcher = Dispatcher()
    dispatcher.overload(THIS)(_one)
    dispatcher.overload(int)(_num)
    setattr(Owner, 'f', dispatcher)
    self.assertIsNone(dispatcher.getFieldOwner())
    self.assertEqual(Owner().f(Owner()), 'Owner')
    self.assertEqual(Owner().f(3), 3)
    self.assertIs(dispatcher.getFieldOwner(), Owner)
    self.assertEqual(dispatcher.getFieldName(), 'f')
    sig, _ = dispatcher._getDeclaredSigs()
    self.assertEqual(sig.getRawTypes(), (Owner,))

  def test_class_level_read_adopts(self) -> None:
    """A read through the class, which gives the compiled function,
    adopts as well."""

    class Owner:
      pass

    dispatcher = Dispatcher()
    dispatcher.overload(int)(_num)
    Owner.g = dispatcher
    self.assertEqual(Owner.g(Owner(), 5), 5)
    self.assertIs(dispatcher.getFieldOwner(), Owner)
    self.assertEqual(dispatcher.getFieldName(), 'g')

  def test_holder_is_the_owner(self) -> None:
    """Read through a subclass, the dispatcher adopts the class that
    holds it, so 'THIS' names the parent and the subclass matches
    through 'isinstance'."""

    class Parent:
      pass

    class Child(Parent):
      pass

    dispatcher = Dispatcher()
    dispatcher.overload(THIS)(_one)
    Parent.f = dispatcher
    self.assertEqual(Child().f(Child()), 'Child')
    self.assertIs(dispatcher.getFieldOwner(), Parent)
    sig, = dispatcher._getDeclaredSigs()
    self.assertEqual(sig.getRawTypes(), (Parent,))

  def test_placed_dispatcher_unchanged(self) -> None:
    """A dispatcher the class body placed keeps its owner and name."""

    class Owner:
      f = Dispatcher()

    dispatcher = Owner.__dict__['f']
    dispatcher.overload(int)(_num)

    class Other(Owner):
      pass

    self.assertEqual(Other().f(2), 2)
    self.assertIs(dispatcher.getFieldOwner(), Owner)

  def test_unheld_dispatcher_still_refused(self) -> None:
    """A dispatcher no class holds has nothing to adopt and is refused
    as before."""

    class Stranger:
      pass

    dispatcher = Dispatcher()
    dispatcher.overload(int)(_num)
    with self.assertRaises(MissingVariable):
      dispatcher.__get__(None, Stranger)

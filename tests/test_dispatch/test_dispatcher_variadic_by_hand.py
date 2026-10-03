"""
TestDispatcherVariadicByHand subclasses 'DispatcherTest' and pins that
'Dispatcher.overload' registers a signature ending in an 'ARGS' as a
variadic one, as the 'overload' decorator does. It used to store the
signature as one concrete entry, so calls of any other length missed it
and a call of its length reached 'isinstance' with the 'ARGS' instance
and raised Python's own 'TypeError'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.core.sentinels import ARGS
from worktoy.dispatch import Dispatcher

from . import DispatcherTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


def _ints(self: Any, *args) -> tuple:
  return 'ints', args


def _named(self: Any, name: str, *args) -> tuple:
  return name, args


class TestDispatcherVariadicByHand(DispatcherTest):
  """
  TestDispatcherVariadicByHand provides tests for a variadic signature
  registered on a 'Dispatcher' by hand.
  """

  def test_variadic_any_length(self) -> None:
    """A signature of 'ARGS[int]' takes calls of any length."""
    d = Dispatcher()
    d.overload(ARGS[int])(_ints)

    class Foo:
      bar = d

    foo = Foo()
    self.assertEqual(foo.bar(), ('ints', ()))
    self.assertEqual(foo.bar(1), ('ints', (1,)))
    self.assertEqual(foo.bar(*range(8)), ('ints', (*range(8),)))

  def test_variadic_with_prefix(self) -> None:
    """A signature with a fixed prefix before 'ARGS' takes the prefix and
    any number of the tail."""
    d = Dispatcher()
    d.overload(str, ARGS[int])(_named)

    class Foo:
      bar = d

    self.assertEqual(Foo().bar('a'), ('a', ()))
    self.assertEqual(Foo().bar('a', 1, 2), ('a', (1, 2)))

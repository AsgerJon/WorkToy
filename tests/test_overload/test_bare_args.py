"""
TestBareArgs subclasses 'OverloadTest' and pins that a bare 'ARGS' in an
overload signature, written without the star, is read as '*ARGS': a
variadic tail of arguments of any type.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.core.sentinels import ARGS
from worktoy.dispatch import overload, Dispatcher, TypeSig
from worktoy.mcls import BaseObject
from worktoy.waitaminute import TypeException
from worktoy.waitaminute.dispatch import DuplicateSignature

from . import OverloadTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class Tail(BaseObject):
  """Tail declares an 'int' followed by a bare 'ARGS'."""

  @overload(int, ARGS)
  def take(self, first: int, *rest: Any) -> tuple:
    return first, rest


class TestBareArgs(OverloadTest):
  """
  TestBareArgs provides tests for a bare 'ARGS' in an overload signature.
  """

  def test_bare_args_takes_a_tail(self) -> None:
    """This method tests that '@overload(int, ARGS)' does not declare a
    signature no call matches. It takes an 'int' followed by any number of
    arguments of any type."""
    tail = Tail()
    self.assertEqual(tail.take(1), (1, ()))
    self.assertEqual(tail.take(1, 'a', 2.5), (1, ('a', 2.5)))

  def test_bare_args_equals_starred(self) -> None:
    """This method tests that a bare 'ARGS' and '*ARGS' do not declare two
    different signatures. Both under one name with two functions raise
    'DuplicateSignature'."""
    with self.assertRaises(DuplicateSignature):
      class Both(BaseObject):
        @overload(int, ARGS)
        def take(self, *args: Any) -> str:
          return 'bare'  # pragma: no cover

        @overload(int, *ARGS)
        def take(self, *args: Any) -> str:
          return 'starred'  # pragma: no cover

  def test_dispatcher_by_hand(self) -> None:
    """This method tests that a 'Dispatcher' wired by hand does not read a
    bare 'ARGS' differently from 'overload'. It takes the tail as well."""

    class Plain:
      take = Dispatcher()

      @take.overload(int, ARGS)
      def take(self, first: int, *rest: Any) -> tuple:
        return first, rest

    self.assertEqual(Plain().take(1, 'a'), (1, ('a',)))

  def test_flex_refuses_bare_args(self) -> None:
    """This method tests that 'overload.flex' and 'Dispatcher.flex' do not
    accept a bare 'ARGS'. They refuse it with 'TypeException', as they
    refuse '*ARGS'."""
    with self.assertRaises(TypeException):
      overload.flex(int, ARGS)
    with self.assertRaises(TypeException):
      overload.flex(int, *ARGS)
    with self.assertRaises(TypeException):
      Dispatcher().flex(int, ARGS)

  def test_star_args_reads_bare_args(self) -> None:
    """This method tests that 'TypeSig.starARGS' does not keep a bare
    'ARGS' as written. It gives 'ARGS[object]' in its place and keeps
    every other entry."""
    self.assertEqual(TypeSig.starARGS(int, ARGS), (int, ARGS[object]))
    self.assertEqual(TypeSig.starARGS(int, ARGS[str]), (int, ARGS[str]))

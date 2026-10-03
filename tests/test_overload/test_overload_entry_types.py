"""
TestOverloadEntryTypes subclasses 'OverloadTest' and pins that a declared
signature holds classes only, the last entry optionally an 'ARGS' of a
class. Nothing used to check the entries, so a parametrized generic such
as 'List[int]', a 'typing.Union' or an 'ARGS' before the end built the
class, and the first call missing the exact-type lookup reached
'isinstance' with it and raised Python's own 'TypeError', before any
later signature, cast or fallback was tried. 'overload', 'overload.flex',
'Dispatcher.overload' and 'Dispatcher.flex' now refuse such an entry
with 'TypeException' at the declaration. A flexible signature takes no
'ARGS' at all, since its entries are rearranged.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from numbers import Number
from typing import TYPE_CHECKING, List, Union

from worktoy.core.sentinels import ARGS, THIS
from worktoy.dispatch import overload, Dispatcher
from worktoy.mcls import BaseObject
from worktoy.waitaminute import TypeException

from . import OverloadTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


def _load(self: Any, *args) -> tuple:
  return args


class Pretender:
  """Pretender claims to be a class through '__class__', as 'list[int]'
  does on Python 3.9 and 3.10, so 'isinstance(Pretender(), type)' answers
  'True'."""

  @property
  def __class__(self) -> type:
    return type


class TestOverloadEntryTypes(OverloadTest):
  """
  TestOverloadEntryTypes provides tests for the entries of a declared
  signature.
  """

  def test_generic_refused(self) -> None:
    """A parametrized generic is refused, naming its position."""
    with self.assertRaises(TypeException) as context:
      overload(int, List[int])
    self.assertEqual(context.exception.varName, 'types[1]')
    self.assertEqual(context.exception.actualObject, List[int])
    self.assertEqual(context.exception.expectedTypes, (type,))

  def test_pretender_refused(self) -> None:
    """An object claiming to be a class through '__class__' is
    refused."""
    pretender = Pretender()
    self.assertIsInstance(pretender, type)
    with self.assertRaises(TypeException):
      overload(pretender)

  def test_union_refused(self) -> None:
    """A 'typing.Union' is refused."""
    with self.assertRaises(TypeException):
      overload(Union[int, str])

  def test_args_before_end_refused(self) -> None:
    """An 'ARGS' anywhere but at the end is refused."""
    with self.assertRaises(TypeException) as context:
      overload(ARGS[int], str)
    self.assertEqual(context.exception.varName, 'types[0]')

  def test_args_of_non_class_refused(self) -> None:
    """An 'ARGS' of something that is not a class is refused."""
    with self.assertRaises(TypeException) as context:
      overload(int, ARGS[List[int]])
    self.assertEqual(context.exception.varName, 'types[1]')
    self.assertEqual(context.exception.actualObject, List[int])

  def test_dispatcher_overload_refuses(self) -> None:
    """'Dispatcher.overload' refuses the same entries."""
    with self.assertRaises(TypeException):
      Dispatcher().overload(List[int])
    with self.assertRaises(TypeException):
      Dispatcher().overload(ARGS[int], int)

  def test_flex_refuses(self) -> None:
    """'overload.flex' and 'Dispatcher.flex' refuse a non-class entry and
    any 'ARGS'."""
    for flex in (overload.flex, Dispatcher().flex):
      with self.subTest(flex=flex):
        with self.assertRaises(TypeException):
          flex(int, List[int])
        with self.assertRaises(TypeException):
          flex(int, ARGS[str])

  def test_classes_accepted(self) -> None:
    """Classes, abstract bases, 'THIS', and a final 'ARGS' of a class or
    of 'THIS' are accepted and dispatch."""

    class Foo(BaseObject):
      @overload(Number, str)
      def bar(self, *args) -> str:
        return 'number'

      @overload(THIS)
      def bar(self, *args) -> str:
        return 'this'

      @overload(int, ARGS[str])
      def bar(self, *args) -> str:
        return 'variadic'

      @overload(ARGS[THIS])
      def bar(self, *args) -> str:
        return 'variadic this'

    foo = Foo()
    self.assertEqual(foo.bar(1.5, 'x'), 'number')
    self.assertEqual(foo.bar(foo), 'this')
    self.assertEqual(foo.bar(1, 'a', 'b', 'c'), 'variadic')
    self.assertEqual(foo.bar(foo, foo, foo), 'variadic this')
    d = Dispatcher()
    d.overload(Number, str)(_load)

    class Baz:
      qux = d

    self.assertEqual(Baz().qux(1, 'a'), (1, 'a'))

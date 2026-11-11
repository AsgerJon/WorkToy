"""
PromiseOverloadRefusals promises the declarations '@overload' refuses,
from 'worktoy.dispatch'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import sys
from unittest import TestCase, skipIf

from worktoy.dispatch import overload
from worktoy.mcls import BaseObject
from worktoy.waitaminute import TypeException, UncheckableType
from worktoy.waitaminute.dispatch import BareOverload, DuplicateSignature


class PromiseOverloadRefusals(TestCase):
  """
  A mistaken declaration fails at its line or as the class is created,
  never at the first call. '@overload' without parentheses raises
  'BareOverload'. An entry that is no class raises 'TypeException', and
  'None' a 'TypeError', since a call passing 'None' is declared with
  'type(None)'. A class 'isinstance' cannot check, such as a 'Protocol'
  not marked '@runtime_checkable', raises 'UncheckableType'. One body
  declaring the same signature twice for a name raises
  'DuplicateSignature'. An '@overload' in a class whose metaclass is not
  based on 'BaseMeta' raises 'TypeError' as the class is created,
  wrapped by the interpreter in a 'RuntimeError' before Python 3.12, and
  calling the record an '@overload' returns raises 'TypeError'. Source:
  the docstrings of 'overload' and 'overload.flex'.
  """

  def test_bare(self) -> None:
    with self.assertRaises(BareOverload) as context:
      class Bare(BaseObject):
        @overload
        def f(self, x) -> None:
          pass
    self.assertIsInstance(context.exception, TypeError)
    self.assertEqual(context.exception.decorator, 'overload')
    self.assertTrue(callable(context.exception.func))

  def test_entry_not_a_class(self) -> None:
    with self.assertRaises(TypeException) as context:
      class Wrong(BaseObject):
        @overload(3)
        def f(self, x) -> None:
          pass
    e = context.exception
    self.assertEqual(e.actualObject, 3)
    self.assertIs(e.actualType, int)
    self.assertEqual(e.expectedTypes, (type,))

  def test_none_entry(self) -> None:
    with self.assertRaises(TypeError):
      class Wrong(BaseObject):
        @overload(None)
        def f(self, x) -> None:
          pass

  @skipIf(sys.version_info < (3, 8), 'typing.Protocol arrived in 3.8')
  def test_uncheckable(self) -> None:
    from typing import Protocol

    class Sized(Protocol):
      def size(self) -> int: ...

    with self.assertRaises(UncheckableType) as context:
      class Wrong(BaseObject):
        @overload(Sized)
        def f(self, x) -> None:
          pass
    e = context.exception
    self.assertIs(e.entry, Sized)
    self.assertEqual(e.position, 0)
    self.assertIsInstance(e.declaration, str)
    self.assertIsInstance(e.refusal, TypeError)

  def test_duplicate_signature(self) -> None:
    with self.assertRaises(DuplicateSignature) as context:
      class Twice(BaseObject):
        @overload(int)
        def f(self, x: int) -> int:
          return 1

        @overload(int)
        def f(self, x: int) -> int:
          return 2
    e = context.exception
    self.assertIsInstance(e, TypeError)
    self.assertTrue(callable(e.existing))
    self.assertTrue(callable(e.duplicate))

  def test_plain_class(self) -> None:
    #  Before Python 3.12 the interpreter wraps a refusal raised while it
    #  places the attributes of a class in a 'RuntimeError'.
    with self.assertRaises((TypeError, RuntimeError)) as context:
      class Plain:
        @overload(int)
        def f(self, x: int) -> None:
          pass
    refusal = context.exception.__cause__ or context.exception
    self.assertIsInstance(refusal, TypeError)

  def test_record_called(self) -> None:
    record = overload(int)(lambda self, x: x)
    with self.assertRaises(TypeError):
      record(None, 1)

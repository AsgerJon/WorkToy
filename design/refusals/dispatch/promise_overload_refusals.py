"""
RefusedOverloadRefusals holds the declarations '@overload' refuses,
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


class RefusedOverloadRefusals(TestCase):
  """
  Each of the following is refused, and the exception named is the one raised
  as of 1.2.3. A mistaken declaration fails at its line or as the class is
  created, never at the first call. '@overload' without parentheses raises
  'BareOverload'. An entry that is no class raises 'TypeException', and
  'None' a 'TypeError', since a call passing 'None' is declared with
  'type(None)'. A class 'isinstance' cannot check, such as a 'Protocol' not
  marked '@runtime_checkable', raises 'UncheckableType'. One body declaring
  the same signature twice for a name raises 'DuplicateSignature'. An
  '@overload' in a class whose metaclass is not based on 'BaseMeta' raises
  'TypeError' as the class is created, wrapped by the interpreter in a
  'RuntimeError' before Python 3.12, and calling the record an '@overload'
  returns raises 'TypeError'. Source: the docstrings of 'overload' and
  'overload.flex'.
  """

  def test_bare(self) -> None:
    with self.assertRaises(Exception) as refused:
      class Bare(BaseObject):
        @overload
        def f(self, x) -> None:
          pass
    self.assertIsInstance(refused.exception, BareOverload)

  def test_entry_not_a_class(self) -> None:
    with self.assertRaises(Exception) as refused:
      class Wrong(BaseObject):
        @overload(3)
        def f(self, x) -> None:
          pass
    self.assertIsInstance(refused.exception, TypeException)

  def test_none_entry(self) -> None:
    with self.assertRaises(Exception) as refused:
      class Wrong(BaseObject):
        @overload(None)
        def f(self, x) -> None:
          pass
    self.assertIsInstance(refused.exception, TypeError)

  @skipIf(sys.version_info < (3, 8), 'typing.Protocol arrived in 3.8')
  def test_uncheckable(self) -> None:
    from typing import Protocol

    class Sized(Protocol):
      def size(self) -> int: ...

    with self.assertRaises(Exception) as refused:
      class Wrong(BaseObject):
        @overload(Sized)
        def f(self, x) -> None:
          pass
    self.assertIsInstance(refused.exception, UncheckableType)

  def test_duplicate_signature(self) -> None:
    with self.assertRaises(Exception) as refused:
      class Twice(BaseObject):
        @overload(int)
        def f(self, x: int) -> int:
          return 1

        @overload(int)
        def f(self, x: int) -> int:
          return 2
    self.assertIsInstance(refused.exception, DuplicateSignature)

  def test_plain_class(self) -> None:
    #  Before Python 3.12 the interpreter wraps a refusal raised while it
    #  places the attributes of a class in a 'RuntimeError'.
    with self.assertRaises(Exception) as refused:
      class Plain:
        @overload(int)
        def f(self, x: int) -> None:
          pass
    self.assertIsInstance(refused.exception, (TypeError, RuntimeError))

  def test_record_called(self) -> None:
    record = overload(int)(lambda self, x: x)
    with self.assertRaises(Exception) as refused:
      record(None, 1)
    self.assertIsInstance(refused.exception, TypeError)

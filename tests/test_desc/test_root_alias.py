"""
TestRootAlias tests '_RootAlias' from 'worktoy.desc', the type alias a
box subscript gives for anything but a plain class.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import sys
from typing import TypeVar, List
from unittest import skipIf

from worktoy.desc import AttriBox, FastBox
from worktoy.desc._root_alias import _RootAlias
from worktoy.waitaminute.desc import PhantomBoxError
from . import DescTest

T = TypeVar('T')


class TestRootAlias(DescTest):
  """
  A box subscripted with a type variable or a generic is a type alias,
  for hints and for the bases of a generic subclass, and must fail at
  once when written in a class body as if it were a box. The tests pin
  the alias for both kinds of subscript, its substitution staying an
  alias of this class, a generic subclass of a box building boxes, and
  the three refusals: bound in a body, called, and read after 'setattr'.
  """

  def test_typevar_subscript_is_alias(self) -> None:
    alias = AttriBox[T]
    self.assertIsInstance(alias, _RootAlias)
    self.assertIs(alias.__origin__, AttriBox)
    self.assertEqual(alias.__args__, (T,))
    self.assertIsInstance(FastBox[T], _RootAlias)

  def test_substitution_keeps_class(self) -> None:
    filled = AttriBox[T][int]
    self.assertIsInstance(filled, _RootAlias)
    self.assertEqual(filled.__args__, (int,))
    self.assertIs(filled.__origin__, AttriBox)

  @skipIf(sys.version_info < (3, 9), 'list[int] came in 3.9')
  def test_generic_subscript_is_alias(self) -> None:
    self.assertIsInstance(AttriBox[List[int]], _RootAlias)
    self.assertIsInstance(AttriBox[list[int]], _RootAlias)

  def test_from_alias(self) -> None:
    alias = _RootAlias.fromAlias(List[int])
    self.assertIsInstance(alias, _RootAlias)
    self.assertIs(alias.__origin__, list)
    self.assertEqual(alias.__args__, (int,))
    self.assertEqual(alias._name, 'List')

  def test_generic_subclass_builds_boxes(self) -> None:
    class Sub(AttriBox[T]):
      pass

    box = Sub[int](5)
    self.assertIsInstance(box, Sub)
    self.assertIs(box.getFieldType(), int)

    class Owner:
      n = Sub[int](5)

    self.assertEqual(Owner().n, 5)

  @skipIf(sys.version_info < (3, 9), 'list[int] came in 3.9')
  def test_bound_in_class_body_refused(self) -> None:
    alias = AttriBox[list[int]]
    with self.assertRaises(PhantomBoxError) as context:
      alias.__set_name__(int, 'items')
    self.assertIs(context.exception.alias, alias)
    self.assertIs(context.exception.owner, int)
    self.assertEqual(context.exception.fieldName, 'items')
    self.assertIn("'items = AttriBox[list[int]]' in class 'int'",
                  str(context.exception))
    with self.assertRaises((PhantomBoxError, RuntimeError)) as context:
      class Bad:
        items = AttriBox[list[int]]
    exception = context.exception.__cause__ or context.exception
    self.assertEqual(exception.owner.__name__, 'Bad')
    self.assertEqual(exception.fieldName, 'items')
    self.assertIs(exception.alias.__origin__, AttriBox)
    self.assertIn("in class 'Bad'", str(exception))

  @skipIf(sys.version_info < (3, 9), 'list[int] came in 3.9')
  def test_called_refused(self) -> None:
    alias = AttriBox[list[int]]
    with self.assertRaises(PhantomBoxError) as context:
      alias([])
    self.assertIs(context.exception.alias, alias)
    self.assertIsNone(context.exception.owner)
    self.assertIsNone(context.exception.fieldName)
    self.assertIn("The declaration 'AttriBox[list[int]]' produced",
                  str(context.exception))

  @skipIf(sys.version_info < (3, 9), 'list[int] came in 3.9')
  def test_read_after_setattr_refused(self) -> None:
    class Late:
      pass

    alias = AttriBox[list[int]]
    setattr(Late, 'items', alias)
    with self.assertRaises(PhantomBoxError) as context:
      _ = Late.items
    self.assertIs(context.exception.owner, Late)
    self.assertIs(context.exception.alias, alias)
    self.assertIsNone(context.exception.fieldName)
    self.assertIn("in class 'Late'", str(context.exception))
    with self.assertRaises(PhantomBoxError) as context:
      _ = Late().items
    self.assertIs(context.exception.alias, alias)
    self.assertIs(context.exception.owner, Late)
    self.assertIsNone(context.exception.fieldName)
    with self.assertRaises(PhantomBoxError) as context:
      hasattr(Late, 'items')
    self.assertIs(context.exception.alias, alias)
    self.assertIs(context.exception.owner, Late)
    self.assertIn("rather than an 'AttriBox'", str(context.exception))

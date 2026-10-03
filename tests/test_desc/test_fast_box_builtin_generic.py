"""
TestFastBoxBuiltinGeneric subclasses 'DescTest' from the 'tests.test_desc'
package and pins that 'FastBox' settles its declaration at class creation
the way 'AttriBox' does. A subscript naming anything but a plain class, a
parametrized generic such as 'list[int]' or 'List[int]', goes to the
generic machinery, and a class body binding the resulting alias raises
'PhantomBoxError'. A box that never received a field type, written
'FastBox()' or produced by calling such an alias, raises 'MissingVariable'.
Before, every one of these declarations built a class, and the mistake
surfaced on a later read or write, if at all: 'FastBox[list[int]]' read
back a plain '[]'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import sys
from typing import List

from worktoy.desc import FastBox
from worktoy.mcls import BaseObject
from worktoy.waitaminute import MissingVariable, TypeException
from worktoy.waitaminute.desc import PhantomBoxError

from . import DescTest


class TestFastBoxBuiltinGeneric(DescTest):
  """
  TestFastBoxBuiltinGeneric provides tests for the declarations 'FastBox'
  refuses at class creation, and for the plain classes it must still claim
  as field types.
  """

  def test_builtin_generic_without_call(self) -> None:
    """
    A builtin parametrized generic written without the trailing call is
    refused with 'PhantomBoxError' as the class is created, and the
    refusal names 'FastBox' as the box the subscript was written against.
    """
    if sys.version_info < (3, 9):  # pragma: no cover (Python < 3.9)
      self.skipTest('builtin generics are not subscriptable before 3.9')
    subscript = list[int]
    with self.assertRaises((PhantomBoxError, RuntimeError)) as context:
      class Foo:  # noqa
        bar = FastBox[subscript]
    e = self._unwrapSetName(context.exception, PhantomBoxError)
    self.assertIsInstance(e, PhantomBoxError)
    self.assertEqual(e.fieldName, 'bar')
    self.assertIn('FastBox[list[int]]', str(e))

  def test_builtin_generic_with_call(self) -> None:
    """
    A builtin parametrized generic written with the trailing call builds
    a box that never received a field type, which is refused with
    'MissingVariable' as the class is created.
    """
    if sys.version_info < (3, 9):  # pragma: no cover (Python < 3.9)
      self.skipTest('builtin generics are not subscriptable before 3.9')
    subscript = list[int]
    with self.assertRaises((MissingVariable, RuntimeError)) as context:
      class Foo:  # noqa
        bar = FastBox[subscript]()
    e = self._unwrapSetName(context.exception, MissingVariable)
    self.assertIsInstance(e, MissingVariable)
    self.assertEqual(e.varName, '__field_type__')

  def test_typing_generic_without_call(self) -> None:
    """
    A parametrized generic from 'typing', which no version takes for a
    plain class, is refused with 'PhantomBoxError' as well. It used to
    build a class whose first read failed to instantiate 'List'.
    """
    with self.assertRaises((PhantomBoxError, RuntimeError)) as context:
      class Foo:  # noqa
        bar = FastBox[List[int]]
    e = self._unwrapSetName(context.exception, PhantomBoxError)
    self.assertIsInstance(e, PhantomBoxError)
    self.assertIn('List[int]', str(e))

  def test_box_without_field_type(self) -> None:
    """
    A 'FastBox' with no subscript has no field type and no later chance
    to learn one, so the class body declaring it is refused with
    'MissingVariable' rather than the first read.
    """
    with self.assertRaises((MissingVariable, RuntimeError)) as context:
      class Foo:  # noqa
        bar = FastBox()
    e = self._unwrapSetName(context.exception, MissingVariable)
    self.assertIsInstance(e, MissingVariable)
    self.assertEqual(e.varName, '__field_type__')
    self.assertIn(type, e.expectedTypes)

  def test_subscript_neither_class_nor_generic(self) -> None:
    """
    A subscript that the generic machinery refuses as well, such as two
    types where 'FastBox' takes one, raises 'TypeException' naming the
    subscript.
    """
    with self.assertRaises(TypeException) as context:
      _ = FastBox[int, str]
    e = context.exception
    self.assertEqual(e.varName, 'fieldType')
    self.assertEqual(e.actualObject, (int, str))

  def test_class_answering_every_name(self) -> None:
    """
    A class whose '__class_getattr__' answers every name, '__origin__'
    included, is still a plain class and is claimed as a field type.
    """

    class Anything(BaseObject):
      @classmethod
      def __class_getattr__(cls, name: str) -> str:
        return 'answer for %s' % name

    self.assertEqual(Anything.__origin__, 'answer for __origin__')

    class Foo:
      bar = FastBox[Anything]()

    self.assertIsInstance(Foo().bar, Anything)

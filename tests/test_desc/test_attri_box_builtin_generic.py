"""
TestAttriBoxBuiltinGeneric subclasses 'DescTest' from the 'tests.test_desc'
package and pins how 'AttriBox' and the boxes derived from it, 'FixBox'
and 'KeeBox', treat a builtin parametrized generic such as 'list[int]' in
their subscript. Python 3.9 and 3.10 answer 'True' to
'isinstance(list[int], type)', so a box that trusted that answer took the
generic for a plain type on those two versions: the class built, and the
first read raised a 'TypeError' from 'isinstance'. The subscript now goes
to the generic machinery on every version, where 'PhantomBoxError' refuses
it at class creation, as the changelog for 1.1.0 says. 'KeeBox' accepts
only an enumeration in its subscript and refuses the generic even earlier.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import sys

from worktoy.desc import AttriBox, FixBox
from worktoy.keenum import KeeBox
from worktoy.mcls import BaseObject
from worktoy.waitaminute import MissingVariable, TypeException
from worktoy.waitaminute.desc import PhantomBoxError

from . import DescTest


class TestAttriBoxBuiltinGeneric(DescTest):
  """
  TestAttriBoxBuiltinGeneric provides tests for builtin parametrized
  generics in the subscript of 'AttriBox', 'FixBox' and 'KeeBox', and for
  the plain classes that must still be claimed as field types.
  """

  def test_builtin_generic_without_call(self) -> None:
    """
    A builtin parametrized generic written without the trailing call is
    refused with 'PhantomBoxError' as the class is created, on every
    version from 3.9, where the builtin generics became subscriptable.
    """
    if sys.version_info < (3, 9):  # pragma: no cover (Python < 3.9)
      self.skipTest('builtin generics are not subscriptable before 3.9')
    subscript = list[int]
    with self.assertRaises((PhantomBoxError, RuntimeError)) as context:
      class Foo:  # noqa
        bar = AttriBox[subscript]
    e = self._unwrapSetName(context.exception, PhantomBoxError)
    self.assertIsInstance(e, PhantomBoxError)
    self.assertEqual(e.fieldName, 'bar')
    self.assertIn('list[int]', str(e))

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
        bar = AttriBox[subscript]()
    e = self._unwrapSetName(context.exception, MissingVariable)
    self.assertIsInstance(e, MissingVariable)
    self.assertEqual(e.varName, '__field_type__')

  def test_fix_box_builtin_generic(self) -> None:
    """
    'FixBox' takes its subscript through 'AttriBox', so it refuses a
    builtin parametrized generic the same way, and the refusal names
    'FixBox' as the box the subscript was written against.
    """
    if sys.version_info < (3, 9):  # pragma: no cover (Python < 3.9)
      self.skipTest('builtin generics are not subscriptable before 3.9')
    subscript = list[int]
    with self.assertRaises((PhantomBoxError, RuntimeError)) as context:
      class Foo:  # noqa
        bar = FixBox[subscript]
    e = self._unwrapSetName(context.exception, PhantomBoxError)
    self.assertIsInstance(e, PhantomBoxError)
    self.assertIn('FixBox[list[int]]', str(e))
    with self.assertRaises((MissingVariable, RuntimeError)) as context:
      class Bar:  # noqa
        bar = FixBox[subscript]()
    e = self._unwrapSetName(context.exception, MissingVariable)
    self.assertIsInstance(e, MissingVariable)
    self.assertEqual(e.varName, '__field_type__')

  def test_kee_box_builtin_generic(self) -> None:
    """
    'KeeBox' accepts only an enumeration in its subscript, so a builtin
    parametrized generic is refused with 'TypeException' at the
    subscript itself, before any class body binds it.
    """
    if sys.version_info < (3, 9):  # pragma: no cover (Python < 3.9)
      self.skipTest('builtin generics are not subscriptable before 3.9')
    subscript = list[int]
    with self.assertRaises(TypeException) as context:
      _ = KeeBox[subscript]
    self.assertEqual(context.exception.varName, 'fieldType')

  def test_class_answering_every_name(self) -> None:
    """
    A class whose '__class_getattr__' answers every name, '__origin__'
    included, is still a plain class and is claimed as a field type. An
    '__origin__' lookup would take such a class for a generic, which is
    why the box asks for the type of the subscript instead.
    """

    class Anything(BaseObject):
      @classmethod
      def __class_getattr__(cls, name: str) -> str:
        return 'answer for %s' % name

    self.assertEqual(Anything.__origin__, 'answer for __origin__')

    class Foo:
      bar = AttriBox[Anything]()

    self.assertIsInstance(Foo().bar, Anything)

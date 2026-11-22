"""
TestABCObject tests 'ABCObject' of 'worktoy.mcls', the base of the
classes 'ABCMeta' builds.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.dispatch import abstract, overload
from worktoy.mcls import BaseObject, ABCMeta, ABCObject
from worktoy.waitaminute.meta import MissingImplementation
from . import MclsTest


class TestABCObject(MclsTest):
  """
  'ABCObject' is to 'ABCMeta' what 'BaseObject' is to 'BaseMeta': a
  'BaseObject' built by 'ABCMeta', so a class based on it declares
  methods with '@abstract' without naming the metaclass. It declares
  nothing abstract itself, so it is no abstract class. The tests pin
  what it is, that a class based on it is held to what it declares
  abstract, and that it keeps everything a 'BaseObject' gives.
  """

  def test_what_it_is(self) -> None:
    self.assertIs(type(ABCObject), ABCMeta)
    self.assertEqual(ABCObject.__bases__, (BaseObject,))
    self.assertEqual(ABCObject.__missing_implementations__, ())
    self.assertIsInstance(ABCObject(), ABCObject)
    self.assertIsInstance(ABCObject(), BaseObject)

  def test_a_class_based_on_it(self) -> None:
    class Model(ABCObject):
      @abstract
      def rowCount(self) -> int: ...

      @overload(str)
      @abstract
      def data(self, index: str) -> str: ...

    class Names(Model):
      def rowCount(self) -> int:
        return 3

      @overload(str)
      def data(self, index: str) -> str:
        return index

    self.assertIs(type(Model), ABCMeta)
    self.assertEqual(Model.__missing_implementations__,
                     ('rowCount', 'data(str)'))
    with self.assertRaises(MissingImplementation) as context:
      Model()
    self.assertIs(context.exception.cls, Model)
    self.assertEqual(context.exception.names, ('rowCount', 'data(str)'))
    self.assertIn("'rowCount', 'data(str)'", str(context.exception))
    names = Names()
    self.assertEqual((names.rowCount(), names.data('a')), (3, 'a'))

  def test_keeps_the_base_object(self) -> None:
    class Point(ABCObject):
      def __init__(self, x: int) -> None:
        BaseObject.__init__(self, x)
        self.x = x

    class Bare(ABCObject):
      """Declares no initializer."""

    self.assertEqual(Point(3).x, 3)
    self.assertEqual(Point(3).getPosArgs(), (3,))
    with self.assertRaises(TypeError) as context:
      Bare(1)
    self.assertEqual(str(context.exception), 'Bare() takes no arguments')

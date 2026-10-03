"""
TestSpaceSubclassFields subclasses 'EZTest' from the 'tests.test_ezdata'
package and pins that a metaclass building its classes with a subclass of
'EZSpace' still inherits the fields of 'EZData' bases built with 'EZSpace'
itself. 'EZSpace.__init__' used to accept a base's namespace only when it
was an instance of the exact namespace class under construction, so such
a class kept its own fields and silently lost every inherited one. A base
that is a plain 'BaseObject' has a namespace holding no fields, and must
still be passed over rather than asked for them.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.ezdata import EZData, EZField, EZMeta, EZSpace
from worktoy.mcls import BaseObject

from . import EZTest


class Point(EZData):
  """Point is an 'EZData' base built with the plain 'EZSpace'."""

  x = EZField[int](0)
  y = EZField[int](0)


class TestSpaceSubclassFields(EZTest):
  """
  TestSpaceSubclassFields provides tests for field inheritance across
  namespace subclasses and for bases that carry no fields.
  """

  def test_space_subclass_inherits_fields(self) -> None:
    """A class built with a subclass of 'EZSpace' inherits the fields of
    a base built with 'EZSpace', ahead of its own."""

    class MySpace(EZSpace):
      pass

    class MyMeta(EZMeta):
      @classmethod
      def __prepare__(mcls, name, bases, **kwargs) -> MySpace:
        return MySpace(mcls, name, bases, **kwargs)

    class Point3(Point, metaclass=MyMeta):
      z = EZField[int](0)

    self.assertEqual([f.fieldName for f in Point3.fields], ['x', 'y', 'z'])
    point = Point3(1, 2, 3)
    self.assertEqual((point.x, point.y, point.z), (1, 2, 3))

  def test_base_object_mixin_passed_over(self) -> None:
    """A plain 'BaseObject' mixin contributes no fields and does not stop
    the class from building."""

    class Greeter(BaseObject):
      def greet(self) -> str:
        return 'hi'

    class Named(Point, Greeter):
      label = EZField[str]('p')

    self.assertEqual(
      [f.fieldName for f in Named.fields], ['x', 'y', 'label'],
    )
    self.assertEqual(Named().greet(), 'hi')

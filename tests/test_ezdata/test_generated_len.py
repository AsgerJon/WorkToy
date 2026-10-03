"""
TestGeneratedLen subclasses 'EZTest' from the 'tests.test_ezdata' package
and pins the '__len__' EZData generates for every class: the number of
fields, own and inherited, agreeing with iteration. An EZData class body
may not define '__len__', while a plain base may, and the generated one
takes precedence over it.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.ezdata import EZData, EZField
from worktoy.waitaminute.ezdata import ReservedMethodError

from . import EZTest


class TestGeneratedLen(EZTest):
  """
  TestGeneratedLen provides tests for the generated '__len__' of 'EZData'
  classes.
  """

  def test_length_is_field_count(self) -> None:
    """
    Testing that the length of an instance is the number of its fields,
    equal to the number of values it iterates.
    """

    class Point(EZData):
      x = EZField[float](0.0)
      y = EZField[float](0.0)

    point = Point(3.0, 4.0)
    self.assertEqual(len(point), 2)
    self.assertEqual(len(point), len(point.asTuple()))

  def test_inherited_fields_counted(self) -> None:
    """
    Testing that inherited fields count toward the length.
    """

    class Point(EZData):
      x = EZField[float](0.0)
      y = EZField[float](0.0)

    class Point3D(Point):
      z = EZField[float](0.0)

    self.assertEqual(len(Point3D(1.0, 2.0, 2.0)), 3)

  def test_class_without_fields(self) -> None:
    """
    Testing that a class without fields has length zero.
    """

    class Empty(EZData):
      pass

    self.assertEqual(len(Empty()), 0)

  def test_class_body_len_refused(self) -> None:
    """
    Testing that an EZData class body defining '__len__' raises
    'ReservedMethodError', naming the method.
    """
    with self.assertRaises(ReservedMethodError) as context:
      class Point(EZData):  # noqa: F841
        x = EZField[float](0.0)
        __len__ = lambda self: 7
    self.assertEqual(context.exception.methodName, '__len__')

  def test_plain_base_len_ignored(self) -> None:
    """
    Testing that a plain base may define '__len__', and that the generated
    '__len__' takes precedence over it, so an instance with fields is
    truthy by its length.
    """

    class Placeholder:
      def __len__(self) -> int:
        return 0

    class Point(EZData, Placeholder):
      x = EZField[float](0.0)
      y = EZField[float](0.0)

    point = Point(3.0, 4.0)
    self.assertEqual(len(point), 2)
    self.assertTrue(point)
    self.assertEqual(len(Placeholder()), 0)

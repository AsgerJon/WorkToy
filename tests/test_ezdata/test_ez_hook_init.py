"""
TestEZHookInit tests the generated constructor and the attribute guards
of a dataclass built by 'EZHook' from 'worktoy.ezdata'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.ezdata import EZData
from worktoy.waitaminute import TypeException
from worktoy.waitaminute.ezdata import ExtraPositionalException
from worktoy.waitaminute.ezdata import ExtraKeywordException
from worktoy.waitaminute.ezdata import RepeatedFieldException
from worktoy.waitaminute.ezdata import KwargsOnlyException
from . import EzdataTest, Point2D, Circle, Span, Labelled


class TestEZHookInit(EzdataTest):
  """
  The generated '__init__' takes the fields by position and by
  keyword, casts every value, refuses surplus, unknown or repeated
  arguments, fills the rest from the defaults and calls
  '__post_init__'. The generated '__setattr__' casts or refuses, and
  the generated '__delattr__' keeps every field. The tests pin each
  route on both a mutable and a frozen class.
  """

  def test_construction(self) -> None:
    self.assertEqual(Point2D(1, 2).asTuple(), (1.0, 2.0))
    self.assertEqual(Point2D(y=2).asTuple(), (0.0, 2.0))
    self.assertEqual(Point2D(1, y=2).asTuple(), (1.0, 2.0))
    self.assertEqual(Point2D().asTuple(), (0.0, 0.0))
    self.assertIs(type(Point2D(1, 2).x), float)
    with self.assertRaises(TypeException) as context:
      Point2D('a')
    self.assertEqual(context.exception.varName, 'x')
    self.assertEqual(context.exception.actualObject, 'a')
    self.assertIs(context.exception.actualType, str)
    self.assertEqual(context.exception.expectedTypes, (float,))
    self.assertIn("'x' to be an instance of 'float'", str(context.exception))
    with self.assertRaises(TypeException) as context:
      Point2D(y='b')
    self.assertEqual(context.exception.varName, 'y')
    self.assertEqual(context.exception.actualObject, 'b')
    self.assertIs(context.exception.actualType, str)
    self.assertEqual(context.exception.expectedTypes, (float,))
    self.assertIn("'y' to be an instance of 'float'", str(context.exception))

  def test_extra_positional_refused(self) -> None:
    with self.assertRaises(ExtraPositionalException) as context:
      Point2D(1, 2, 3)
    exception = context.exception
    self.assertIs(exception.cls, Point2D)
    self.assertEqual(exception.fieldCount, 2)
    self.assertEqual(exception.argCount, 3)
    self.assertIn('2 fields but received 3 positional arguments',
                  str(exception))

    class Empty(EZData):
      """A dataclass without fields."""

    with self.assertRaises(ExtraPositionalException) as context:
      Empty(1)
    self.assertIs(context.exception.cls, Empty)
    self.assertEqual(context.exception.fieldCount, 0)
    self.assertEqual(context.exception.argCount, 1)
    self.assertIn("'Empty' has 0 fields but received 1 positional argument",
                  str(context.exception))

    class One(EZData):
      x = 1

    with self.assertRaises(ExtraPositionalException) as context:
      One(1, 2)
    self.assertIs(context.exception.cls, One)
    self.assertEqual(context.exception.fieldCount, 1)
    self.assertEqual(context.exception.argCount, 2)
    self.assertIn("'One' has 1 field but received 2 positional arguments",
                  str(context.exception))

  def test_unknown_keyword_refused(self) -> None:
    with self.assertRaises(ExtraKeywordException) as context:
      Point2D(z=1)
    exception = context.exception
    self.assertIs(exception.cls, Point2D)
    self.assertEqual(exception.keyword, 'z')
    self.assertEqual(exception.fieldNames, ('x', 'y'))
    self.assertIn("'Point2D' received the keyword 'z'", str(exception))
    self.assertIn("The fields are: 'x', 'y'.", str(exception))

  def test_repeated_field_refused(self) -> None:
    with self.assertRaises(RepeatedFieldException) as context:
      Point2D(1, x=2)
    exception = context.exception
    self.assertIs(exception.cls, Point2D)
    self.assertEqual(exception.fieldName, 'x')
    self.assertIn("'Point2D' received the field 'x' both by position and "
                  "by keyword", str(exception))
    self.assertEqual(Point2D(1, y=2).y, 2.0)

  def test_keyword_only(self) -> None:
    circle = Circle(radius=2.0)
    self.assertEqual(circle.radius, 2.0)
    self.assertEqual(circle.center, Point2D())
    with self.assertRaises(KwargsOnlyException) as context:
      Circle(Point2D(), 2.0)
    exception = context.exception
    self.assertIs(exception.cls, Circle)
    self.assertEqual(exception.argCount, 2)
    self.assertIn("'Circle' was declared with 'kwOnly=True' but received "
                  "2 positional arguments", str(exception))
    with self.assertRaises(KwargsOnlyException) as context:
      Circle(2.0)
    self.assertIs(context.exception.cls, Circle)
    self.assertEqual(context.exception.argCount, 1)
    self.assertIn('received 1 positional argument', str(context.exception))

  def test_post_init(self) -> None:
    span = Span(5, 2)
    self.assertEqual((span.start, span.stop, span.length), (2, 5, 3))
    self.assertEqual(Span(1, 4).length, 3)

    class Sub(Span):
      tag = 'sub'

    self.assertEqual(Sub(3, 1).length, 2)
    self.assertEqual(Point2D().__dict__, {'x': 0.0, 'y': 0.0})

  def test_class_attribute_of_a_mixin_is_no_value(self) -> None:
    self.assertEqual(Labelled().count, 1)
    self.assertEqual(Labelled(count=5).count, 5)
    self.assertEqual(Labelled('t').__dict__, {'label': 't', 'count': 1})

  def test_set_attribute(self) -> None:
    point = Point2D()
    point.x = 3
    self.assertEqual(point.x, 3.0)
    self.assertIs(type(point.x), float)
    with self.assertRaises(TypeException) as context:
      point.y = 'a'
    self.assertEqual(context.exception.varName, 'y')
    self.assertEqual(context.exception.actualObject, 'a')
    self.assertIs(context.exception.actualType, str)
    self.assertEqual(context.exception.expectedTypes, (float,))
    self.assertIn("'y' to be an instance of 'float'", str(context.exception))
    self.assertEqual(point.y, 0.0)
    point.note = 'free'
    self.assertEqual(point.__dict__['note'], 'free')

  def test_frozen_refuses_assignment(self) -> None:
    circle = Circle(radius=2.0)
    for name in ('radius', 'note'):
      with self.subTest(name=name):
        with self.assertRaises(AttributeError) as context:
          setattr(circle, name, 3.0)
        self.assertEqual(str(context.exception), "'Circle' is frozen; "
                         "cannot assign to attribute '%s'!" % name)
    self.assertEqual(circle.radius, 2.0)

  def test_delete_attribute(self) -> None:
    point = Point2D()
    point.note = 'free'
    del point.note
    self.assertNotIn('note', point.__dict__)
    with self.assertRaises(AttributeError) as context:
      del point.x
    self.assertIn("EZData class 'Point2D' does not allow deleting field "
                  "'x'", str(context.exception))
    self.assertEqual(point.x, 0.0)

  def test_frozen_refuses_deletion(self) -> None:
    circle = Circle(radius=2.0)
    for name in ('radius', 'note'):
      with self.subTest(name=name):
        with self.assertRaises(AttributeError) as context:
          delattr(circle, name)
        self.assertEqual(str(context.exception), "'Circle' is frozen; "
                         "cannot delete attribute '%s'!" % name)
    self.assertEqual(circle.radius, 2.0)

  def test_random_points(self) -> None:
    self.randomFloat.size = 6
    self.randomInteger.size = 6
    for x, n in zip(self.randomFloat.row, self.randomInteger.row):
      with self.subTest(x=x, n=n):
        self.assertEqual(Point2D(x, n).asTuple(), (x, float(n)))
        self.assertEqual(Point2D(y=x).y, x)
        point = Point2D()
        point.x = n
        self.assertEqual(point.x, float(n))

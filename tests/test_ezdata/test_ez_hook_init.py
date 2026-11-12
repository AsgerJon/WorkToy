"""
TestEZHookInit tests the generated constructor and the attribute guards
of a dataclass built by 'EZHook' from 'worktoy.ezdata'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.ezdata import EZData, EZField, EZMeta, EZSpace
from worktoy.mcls import BaseMeta
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
  route on both a mutable and a frozen class, and that a field named
  'self' or 'argCount', as a parameter of the generated code is,
  arrives by keyword like any other.
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

  def test_class_without_a_post_init_reads_none(self) -> None:
    #  The lookup of the hook lands on the metaclass for a class without
    #  one, and raises nothing.
    self.assertIsNone(vars(EZMeta)['__post_init__'])
    self.assertIsNone(type.__getattribute__(Point2D, '__post_init__'))
    self.assertNotIn('__post_init__', vars(Point2D))
    self.assertFalse(hasattr(Point2D(), '__post_init__'))
    self.assertIs(type.__getattribute__(Span, '__post_init__'),
                  vars(Span)['__post_init__'])

  def test_post_init_found_wherever_it_sits(self) -> None:
    seen = []

    class Late(EZData):
      x = 0

    Late(1)
    Late.__post_init__ = lambda self: seen.append(self.x)
    Late(2)
    self.assertEqual(seen, [2])

    class Noting:
      def __post_init__(self) -> None:
        seen.append('mixin')

    class After(EZData, Noting):
      x = 0

    After()
    self.assertEqual(seen, [2, 'mixin'])

  def test_post_init_under_a_metaclass_of_another_kind(self) -> None:
    #  A metaclass that is no 'EZMeta' holds no 'None' for the lookup of
    #  the hook to land on; the constructor must do without it.
    class Bare(BaseMeta):
      @classmethod
      def __prepare__(mcls, name: str, bases: tuple, **kw) -> EZSpace:
        return EZSpace(mcls, name, bases, **kw)

    class Loner(metaclass=Bare):
      x = 0
      y = 0

    self.assertNotIsInstance(Loner, EZMeta)
    with self.assertRaises(AttributeError):
      type.__getattribute__(Loner, '__post_init__')
    self.assertEqual(Loner(1, y=2).asDict(), dict(x=1, y=2))
    seen = []

    class Hooked(Loner):
      def __post_init__(self) -> None:
        seen.append(self.x)

    Hooked(3)
    self.assertEqual(seen, [3])

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

  def test_only_the_field_type_itself_is_stored_uncast(self) -> None:
    class Agreeing(type):
      """A metaclass whose classes answer '==' with 'True' to anything."""

      def __eq__(cls, other: object) -> bool:
        return True

      __hash__ = type.__hash__

    class Loose(metaclass=Agreeing):
      """A class that claims to equal every other."""

    class Holder(EZData):
      item = EZField[Loose]()

    self.assertTrue(Loose == int)
    self.assertFalse(int != Loose)
    loose = Loose()
    self.assertIs(Holder(loose).item, loose)
    self.assertIs(Holder(item=loose).item, loose)
    with self.assertRaises(TypeException) as context:
      Holder(5)
    self.assertEqual(context.exception.varName, 'item')
    self.assertEqual(context.exception.actualObject, 5)
    self.assertEqual(context.exception.expectedTypes, (Loose,))
    self.assertIn("'item' to be an instance of 'Loose'",
                  str(context.exception))
    holder = Holder()
    holder.item = loose
    self.assertIs(holder.item, loose)
    with self.assertRaises(TypeException) as context:
      holder.item = 5
    self.assertEqual(context.exception.varName, 'item')
    self.assertEqual(context.exception.actualObject, 5)
    self.assertEqual(context.exception.expectedTypes, (Loose,))
    self.assertIn("'item' to be an instance of 'Loose'",
                  str(context.exception))
    self.assertIs(holder.item, loose)

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

  def test_field_named_like_a_parameter(self) -> None:
    class Call(EZData):
      name = ''
      argCount = 0

    self.assertEqual(Call(name='f', argCount=3).asTuple(), ('f', 3))
    self.assertEqual(Call('f', 3).replace(name='g').asTuple(), ('g', 3))
    self.assertEqual(Call('f', 3).replace(argCount=5).asTuple(), ('f', 5))
    with self.assertRaises(RepeatedFieldException) as context:
      Call('f', 3, argCount=4)
    self.assertEqual(context.exception.fieldName, 'argCount')
    expected = """EZData class 'Call' received the field 'argCount' both
    by position and by keyword."""
    self.assertEqual(str(context.exception),
                     str.join(' ', expected.split()))

    class Links(EZData):
      self = ''
      related = ''

    links = Links(self='/a', related='/b')
    self.assertEqual(links.asTuple(), ('/a', '/b'))
    self.assertEqual(links.replace(self='/c').asTuple(), ('/c', '/b'))
    self.assertEqual(Links('/a').replace(related='/d').asTuple(),
                     ('/a', '/d'))

    class Strict(EZData, kwOnly=True):
      argCount = 0

    self.assertEqual(Strict(argCount=2).asTuple(), (2,))

"""
PromiseGenerated promises the methods an 'EZData' class receives, from
'worktoy.ezdata'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.ezdata import EZData
from worktoy.waitaminute import TypeException
from worktoy.waitaminute.ezdata import ExtraPositionalException
from worktoy.waitaminute.ezdata import ExtraKeywordException
from worktoy.waitaminute.ezdata import RepeatedFieldException


class PromiseGenerated(TestCase):
  """
  An 'EZData' class receives an '__init__' taking its fields by position
  in declaration order or by keyword, each a default when not given,
  each converted to its type as 'typeCast' converts, or refused with
  'TypeException'. Too many positional arguments raise
  'ExtraPositionalException', an unknown keyword
  'ExtraKeywordException', and a field given by position and keyword
  'RepeatedFieldException', all 'TypeError's. '__post_init__', if
  defined, runs after. Iteration gives the values, 'len' the number of
  fields, 'asDict' and 'asTuple' the values, 'replace' a new instance
  with some changed, and '__match_args__' the field names, none for a
  keyword-only class. Two instances of one lineage with equal values are
  equal, a frozen subclass and its parent included; an instance that is
  not frozen is not hashable. Assigning a field converts as '__init__'
  does; deleting a field raises 'AttributeError', while other attributes
  come and go. Source: the docstrings of 'EZData', 'EZMeta' and 'EZHook'.

  Taken back in the update after 1.2.0, with its reason in
  'promises/confessions': equality between a class and a subclass that
  holds its fields in another order.
  """

  def makePoint(self) -> type:
    class Point(EZData):
      x = 0.0
      y = 0.0

    return Point

  def test_init(self) -> None:
    Point = self.makePoint()
    self.assertEqual(tuple(Point(1, 2)), (1.0, 2.0))
    self.assertEqual(tuple(Point(y=3)), (0.0, 3.0))
    self.assertIs(type(Point(1).x), float)
    with self.assertRaises(TypeException):
      Point('one')

  def test_init_refusals(self) -> None:
    Point = self.makePoint()
    with self.assertRaises(ExtraPositionalException) as context:
      Point(1, 2, 3)
    self.assertIs(context.exception.cls, Point)
    self.assertEqual(context.exception.fieldCount, 2)
    self.assertEqual(context.exception.argCount, 3)
    with self.assertRaises(ExtraKeywordException) as context:
      Point(z=1)
    self.assertEqual(context.exception.keyword, 'z')
    self.assertEqual(context.exception.fieldNames, ('x', 'y'))
    with self.assertRaises(RepeatedFieldException) as context:
      Point(1, x=2)
    self.assertEqual(context.exception.fieldName, 'x')
    for error in (ExtraPositionalException, ExtraKeywordException,
                  RepeatedFieldException):
      with self.subTest(error=error.__name__):
        self.assertTrue(issubclass(error, TypeError))

  def test_post_init(self) -> None:
    class Positive(EZData):
      value = 1

      def __post_init__(self) -> None:
        if self.value < 0:
          raise ValueError('negative')

    with self.assertRaises(ValueError):
      Positive(-1)
    self.assertEqual(Positive(2).value, 2)

  def test_views(self) -> None:
    Point = self.makePoint()
    point = Point(1, 2)
    self.assertEqual(len(point), 2)
    self.assertEqual(point.asDict(), {'x': 1.0, 'y': 2.0})
    self.assertEqual(point.asTuple(), (1.0, 2.0))
    moved = point.replace(y=5)
    self.assertEqual(tuple(moved), (1.0, 5.0))
    self.assertEqual(tuple(point), (1.0, 2.0))
    self.assertEqual(Point.__match_args__, ('x', 'y'))

    class Config(EZData, kwOnly=True):
      port = 80

    self.assertEqual(Config.__match_args__, ())

  def test_equality(self) -> None:
    Point = self.makePoint()

    class FrozenPoint(Point, frozen=True):
      pass

    self.assertEqual(Point(1, 2), Point(1, 2))
    self.assertNotEqual(Point(1, 2), Point(1, 3))
    self.assertEqual(Point(1, 2), FrozenPoint(1, 2))
    with self.assertRaises(TypeError):
      hash(Point(1, 2))

  def test_assignment_and_deletion(self) -> None:
    Point = self.makePoint()
    point = Point()
    point.x = 5
    self.assertEqual(point.x, 5.0)
    self.assertIs(type(point.x), float)
    with self.assertRaises(TypeException):
      point.x = 'five'
    with self.assertRaises(AttributeError):
      del point.x
    point.note = 'scratch'
    del point.note
    self.assertFalse(hasattr(point, 'note'))

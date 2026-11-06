"""
TestEZHookMethods tests the generated methods of a dataclass built by
'EZHook' from 'worktoy.ezdata': iteration, conversion, text, equality,
hashing and ordering.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.ezdata import EZData
from worktoy.waitaminute.ezdata import ExtraKeywordException
from . import EzdataTest, Point2D, Circle, Version, Vector, FrozenVector
from . import Vector3


class TestEZHookMethods(EzdataTest):
  """
  A dataclass iterates its field values, measures its fields, converts
  to a dict and a tuple, replaces fields in a copy, writes itself two
  ways, compares equal to a congruent instance of equal values, hashes
  when frozen and orders when ordered. The tests pin each generated
  method with its edge cases.
  """

  def test_iteration_and_length(self) -> None:
    point = Point2D(1, 2)
    self.assertEqual([*point], [1.0, 2.0])
    self.assertEqual(len(point), 2)
    self.assertTrue(point)

    class Empty(EZData):
      """A dataclass without fields."""

    self.assertEqual([*Empty()], [])
    self.assertEqual(len(Empty()), 0)
    self.assertFalse(Empty())

  def test_conversions(self) -> None:
    point = Point2D(1, 2)
    self.assertEqual(point.asDict(), {'x': 1.0, 'y': 2.0})
    self.assertIsNot(point.asDict(), point.asDict())
    self.assertEqual(point.asTuple(), (1.0, 2.0))
    self.assertEqual(point.asTuple(), (*point,))

  def test_replace(self) -> None:
    point = Point2D(1, 2)
    moved = point.replace(y=5)
    self.assertEqual(moved, Point2D(1, 5))
    self.assertEqual(point, Point2D(1, 2))
    self.assertIsNot(moved, point)
    self.assertEqual(point.replace(), point)
    with self.assertRaises(ExtraKeywordException) as context:
      point.replace(z=1, w=2)
    self.assertIs(context.exception.cls, Point2D)
    self.assertEqual(context.exception.keyword, 'z')
    self.assertEqual(context.exception.fieldNames, ('x', 'y'))
    self.assertIsInstance(context.exception, TypeError)
    self.assertIn("'Point2D' received the keyword 'z'",
                  str(context.exception))
    self.assertIn("The fields are: 'x', 'y'.", str(context.exception))
    circle = Circle(radius=1.0)
    self.assertEqual(circle.replace(radius=2.0).radius, 2.0)
    self.assertEqual(circle.radius, 1.0)

  def test_texts(self) -> None:
    point = Point2D(1, 2)
    self.assertEqual(str(point), '<Point2D: x=1.0, y=2.0>')
    self.assertEqual(repr(point), 'Point2D(1.0, 2.0)')
    circle = Circle(radius=2.0)
    self.assertEqual(repr(circle),
                     'Circle(center=Point2D(0.0, 0.0), radius=2.0)')
    self.assertEqual(str(circle),
                     '<Circle: center=Point2D(0.0, 0.0), radius=2.0>')

  def test_equality_within_a_class(self) -> None:
    self.assertEqual(Point2D(1, 2), Point2D(1.0, 2.0))
    self.assertNotEqual(Point2D(1, 2), Point2D(2, 1))
    self.assertIs(Point2D().__eq__(1), NotImplemented)
    self.assertFalse(Point2D() == 1)
    self.assertTrue(Point2D() != 1)
    self.assertFalse(Point2D() == (0.0, 0.0))

  def test_equality_across_classes(self) -> None:
    self.assertEqual(Vector(1, 2), FrozenVector(1, 2))
    self.assertEqual(FrozenVector(1, 2), Vector(1, 2))
    self.assertNotEqual(Vector(1, 2), FrozenVector(1, 3))
    self.assertFalse(Vector(1, 2) == Vector3(1, 2, 0))
    self.assertIs(Vector(1, 2).__eq__(Vector3(1, 2, 0)), False)
    self.assertFalse(Vector3(1, 2, 0) == Vector(1, 2))

    class Lookalike(EZData):
      x = 0.0
      y = 0.0

    self.assertFalse(Vector(1, 2) == Lookalike(1, 2))
    self.assertFalse(Vector(1, 2) == Point2D(1, 2))

  def test_hash(self) -> None:
    self.assertEqual(hash(FrozenVector(1, 2)), hash((1.0, 2.0)))
    self.assertEqual(hash(FrozenVector(1, 2)),
                     hash(FrozenVector(1.0, 2.0)))
    self.assertEqual(len({FrozenVector(1, 2), FrozenVector(1, 2)}), 1)
    with self.assertRaises(TypeError):
      hash(Vector(1, 2))

  def test_ordering(self) -> None:
    self.assertTrue(Version(1, 2) < Version(2, 0))
    self.assertTrue(Version(1, 2) <= Version(1, 2))
    self.assertTrue(Version(1, 3) > Version(1, 2))
    self.assertTrue(Version(1, 3) >= Version(1, 3))
    self.assertFalse(Version(1, 3) < Version(1, 2))
    self.assertEqual(sorted([Version(2, 0), Version(1, 5), Version(1, 2)]),
                     [Version(1, 2), Version(1, 5), Version(2, 0)])

    class Sub(Version, ordered=True):
      patch = 0

    self.assertIs(Version.__lt__(Version(1, 2), Sub(1, 2, 0)),
                  NotImplemented)
    with self.assertRaises(TypeError):
      _ = Version(1, 2) < Sub(1, 2, 0)
    self.assertTrue(Sub(1, 2, 0) < Sub(1, 2, 1))

  def test_random_round_trips(self) -> None:
    self.randomFloat.size = 6
    self.randomInteger.size = 6
    for x, n in zip(self.randomFloat.row, self.randomInteger.row):
      point = Point2D(x, n)
      with self.subTest(x=x, n=n):
        self.assertEqual(Point2D(*point.asTuple()), point)
        self.assertEqual(Point2D(**point.asDict()), point)
        self.assertEqual(point.replace(x=n).asTuple(), (float(n), float(n)))
        self.assertEqual(repr(point), 'Point2D(%r, %r)' % (x, float(n)))

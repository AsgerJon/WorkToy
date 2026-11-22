"""
PromiseDetails promises the finer rules of 'EZData' fields and generated
methods, from 'worktoy.ezdata'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import copy
from unittest import TestCase

from worktoy.ezdata import EZData, EZField, fields


class PromiseDetails(TestCase):
  """
  Methods, properties and classmethods in the body are no fields, and a
  constant kept on a plain base is no field either. A field takes the type of
  its value exactly, so 'x = 0' declares an 'int' field. The default of a
  number or text field converts as 'typeCast' does. A subclass may give an
  inherited field a new default. A body may write its own '__repr__'. An
  instance unpacks as its values, is false without fields, and equals no
  tuple and no instance of a sibling class; an attribute that is no field
  stays out of its values and equality. 'replace' runs '__post_init__' again,
  and 'asDict' keeps a nested 'EZData' as it is. A subclass of a frozen class
  declares 'frozen=True' itself. Copies keep the values. Source: the
  docstrings of 'EZData', 'EZField', 'EZSpace' and 'EZHook', and the 1.1.0
  changelog.
  """

  def test_what_is_a_field(self) -> None:
    class Limits:
      MAX = 100

    class Box(EZData, Limits):
      size = 1

      @property
      def double(self) -> int:
        return 2 * self.size

      def grow(self) -> int:
        return self.size + 1

      @classmethod
      def make(cls) -> Box:
        return cls(3)

    self.assertEqual([f.fieldName for f in fields(Box)], ['size'])
    self.assertEqual((Box.MAX, Box(2).double, Box(2).grow()), (100, 4, 3))
    self.assertEqual(Box.make().size, 3)

  def test_new_default(self) -> None:
    class Point(EZData):
      x = 0.0
      y = 0.0

    class Shifted(Point):
      x = 1.0

    self.assertEqual(tuple(Shifted()), (1.0, 0.0))

  def test_reserved_name_and_own_repr(self) -> None:
    class Named(EZData):
      a = 1

      def __repr__(self) -> str:
        return 'Named!'

    self.assertEqual(repr(Named()), 'Named!')

  def test_instances(self) -> None:
    class Point(EZData):
      x = 0.0
      y = 0.0

    class Left(Point):
      pass

    class Right(Point):
      pass

    class Empty(EZData):
      pass

    x, y = Point(1, 2)
    self.assertEqual((x, y), (1.0, 2.0))
    self.assertFalse(Empty())
    self.assertNotEqual(Point(1, 2), (1.0, 2.0))
    self.assertNotEqual(Left(1, 2), Right(1, 2))
    point = Point(1, 2)
    point.note = 'scratch'
    self.assertEqual(point.asDict(), {'x': 1.0, 'y': 2.0})
    self.assertEqual(point, Point(1, 2))

  def test_post_init_and_nesting(self) -> None:
    calls = []

    class Logged(EZData):
      a = 1

      def __post_init__(self) -> None:
        calls.append(self.a)

    class Inner(EZData):
      v = 1

    class Outer(EZData):
      inner = EZField[Inner]()

    self.assertEqual(Logged(1).replace(a=5).a, 5)
    self.assertEqual(calls, [1, 5])
    self.assertIsInstance(Outer().asDict()['inner'], Inner)

  def test_frozen_rules(self) -> None:
    class Frozen(EZData, frozen=True):
      a = 1
      b = 0

    class StillFrozen(Frozen, frozen=True):
      c = 2

    self.assertTrue(StillFrozen.isFrozen)

  def test_copies(self) -> None:
    class Frozen(EZData, frozen=True):
      a = 1

    self.assertEqual(copy.copy(Frozen(2)), Frozen(2))
    self.assertEqual(copy.deepcopy(Frozen(2)), Frozen(2))

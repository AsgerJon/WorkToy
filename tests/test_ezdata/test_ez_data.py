"""
TestEZData tests 'EZData' from 'worktoy.ezdata' end to end.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core import Object
from worktoy.ezdata import EZData, EZField, EZMeta
from . import EzdataTest, Point2D, Circle, Bag, Span


class TestEZData(EzdataTest):
  """
  'EZData' is the base a dataclass subclasses: fields from
  'EZField[T](...)' or bare values, options by class keyword, a
  '__post_init__' for derived state, and the generated methods in
  return. The tests pin the examples of its docstring, the claims
  about annotations, bare values and fields of every kind, and the
  base itself as a dataclass without fields.
  """

  def test_docstring_examples(self) -> None:
    point = Point2D(3.0, 4.0)
    self.assertEqual((point.x, point.y), (3.0, 4.0))
    circle = Circle(center=point, radius=2.0)
    self.assertIs(circle.center, point)
    self.assertEqual(circle.radius, 2.0)
    self.assertEqual(Circle().radius, 1.0)
    self.assertEqual(Circle().center, Point2D())

  def test_annotation_alone_declares_no_field(self) -> None:
    class Ann(EZData):
      x: int
      y = 1

    self.assertEqual([*Ann.__ez_fields__], ['y'])
    self.assertNotIn('x', Ann().__dict__)
    self.assertEqual(Ann.__annotations__, {'x': 'int'})

  def test_bool_stays_bool(self) -> None:
    class Flagged(EZData):
      n = 0

    self.assertIs(Flagged(True).n, True)
    self.assertIsInstance(Flagged(True).n, int)
    self.assertEqual(Flagged(2).n, 2)

  def test_mutable_defaults_are_not_shared(self) -> None:
    first, second = Bag(), Bag()
    first.items.append(1)
    first.labels['a'] = 1
    first.seeds.append(3)
    self.assertEqual(second.items, [])
    self.assertEqual(second.labels, {})
    self.assertEqual(second.seeds, [1, 2])

  def test_derived_state(self) -> None:
    span = Span(2, 7)
    self.assertEqual(span.length, 5)
    self.assertEqual(span.asDict(), {'start': 2, 'stop': 7})
    self.assertNotIn('length', Span.__ez_fields__)

  def test_base_is_a_dataclass_without_fields(self) -> None:
    self.assertIs(type(EZData), EZMeta)
    self.assertIsSubclass(EZData, Object)
    self.assertEqual(EZData.fields, ())
    instance = EZData()
    self.assertEqual(instance.asTuple(), ())
    self.assertEqual(instance.asDict(), {})
    self.assertEqual(repr(instance), 'EZData()')
    self.assertEqual(str(instance), '<EZData: >')
    self.assertEqual(instance, EZData())
    self.assertFalse(EZData.isFrozen)

  def test_dataclass_as_a_field(self) -> None:
    class Segment(EZData):
      start = EZField[Point2D](Point2D(0.0, 0.0))
      stop = Point2D(1.0, 1.0)

    segment = Segment()
    self.assertEqual(segment.start, Point2D())
    self.assertEqual(segment.stop, Point2D(1.0, 1.0))
    self.assertIsNot(segment.stop, Segment().stop)
    self.assertEqual(Segment.sig.getRawTypes(), (Point2D, Point2D))
    self.assertEqual(Segment(Point2D(2.0, 2.0)).start, Point2D(2.0, 2.0))

  def test_random_spans(self) -> None:
    self.randomInteger.size = 6
    numbers = self.randomInteger.row
    for start, stop in zip(numbers, reversed(numbers)):
      span = Span(start, stop)
      with self.subTest(start=start, stop=stop):
        self.assertLessEqual(span.start, span.stop)
        self.assertEqual(span.length, abs(stop - start))

"""
TestBoxTwoNames subclasses 'DescTest' from the 'tests.test_desc' package
and pins that one box bound to two names in a class body, as in
'width = height = AttriBox[int](0)', gives two fields. The box keeps the
first name and the second name receives a clone of it as the class is
created, so the names keep two values in two slots, as plain Python gives
two attributes. The clone carries the field type, the captured default
and the callbacks registered on the box by then. Before, the box took the
second name for both, and the two attributes read and wrote one value.
'FixBox' and 'FastBox' do the same.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox, FastBox, FixBox
from worktoy.mcls import BaseObject

from . import DescTest

shared = AttriBox[int](0)


class Rect(BaseObject):
  """Rect binds one box to two names."""

  width = height = shared


class Bag(BaseObject):
  """Bag binds one box with a list default to two names."""

  left = right = AttriBox[list]([1, 2])


class Watched(BaseObject):
  """Watched registers a callback on a box bound to two names."""

  first = second = AttriBox[int](0)

  @first.onSet
  def _record(self, value: int) -> None:
    self.__dict__.setdefault('log', []).append(value)


class Once(BaseObject):
  """Once binds one write-once box to two names."""

  a = b = FixBox[int]()


class Plain:
  """Plain binds one 'FastBox' to two names."""

  x = y = FastBox[int](0)


class TestBoxTwoNames(DescTest):
  """
  TestBoxTwoNames provides tests for a box bound to two names in one
  class body.
  """

  def test_two_fields(self) -> None:
    """The two names keep two values."""
    rect = Rect()
    rect.width = 3
    self.assertEqual((rect.width, rect.height), (3, 0))
    rect.height = 4
    self.assertEqual((rect.width, rect.height), (3, 4))

  def test_first_name_keeps_box(self) -> None:
    """The first name keeps the box written in the body; the second name
    holds a clone of the same class, placed on the same owner."""
    width = Rect.__dict__['width']
    height = Rect.__dict__['height']
    self.assertIs(width, shared)
    self.assertIsNot(height, shared)
    self.assertIs(type(height), type(shared))
    self.assertEqual(width.getFieldName(), 'width')
    self.assertEqual(height.getFieldName(), 'height')
    self.assertIs(height.getFieldOwner(), Rect)

  def test_two_slots(self) -> None:
    """Each name stores under its own storage name."""
    rect = Rect()
    rect.width, rect.height = 1, 2
    keys = sorted(k for k in vars(rect) if k.endswith('_field_object__'))
    expected = [
      '__height__attribox_field_object__',
      '__width__attribox_field_object__',
    ]
    self.assertEqual(keys, expected)

  def test_default_per_name(self) -> None:
    """The clone carries the captured default, built once for each name
    and instance."""
    bag = Bag()
    self.assertEqual(bag.left, [1, 2])
    self.assertEqual(bag.right, [1, 2])
    self.assertIsNot(bag.left, bag.right)

  def test_callbacks_carried(self) -> None:
    """A callback registered on the box in the class body is carried by
    the clone, so it fires for both names."""
    watched = Watched()
    watched.first = 1
    watched.second = 2
    self.assertEqual(watched.log, [1, 2])

  def test_set_name_callback_per_name(self) -> None:
    """A 'setName' callback runs once for each name."""
    names = []

    class Named(BaseObject):
      one = two = AttriBox[int](0)

      @classmethod
      @one.setName
      def _named(cls, desc: AttriBox) -> None:
        names.append(desc.getFieldName())

    self.assertEqual(names, ['one', 'two'])
    self.assertIsNot(Named.__dict__['one'], Named.__dict__['two'])

  def test_fix_box(self) -> None:
    """'FixBox' gives two write-once fields."""
    once = Once()
    once.a = 1
    once.b = 2
    self.assertEqual((once.a, once.b), (1, 2))

  def test_fast_box(self) -> None:
    """'FastBox' gives two fields, the second holding a clone."""
    plain = Plain()
    plain.x = 3
    self.assertEqual((plain.x, plain.y), (3, 0))
    self.assertIsNot(Plain.__dict__['x'], Plain.__dict__['y'])
    self.assertEqual(sorted(vars(plain)), ['__fast_x__', '__fast_y__'])

  def test_fast_box_clone(self) -> None:
    """'FastBox.clone' copies the field type and the captured default,
    and no field name."""
    box = FastBox[float](1)
    copy = box.clone()
    self.assertIsNot(copy, box)
    self.assertIs(type(copy), type(box))

    class Holder:
      value = copy

    self.assertEqual(Holder().value, 1.0)
    self.assertIsNone(box.__dict__.get('__field_name__'))

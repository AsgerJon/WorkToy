"""
TestBaseDescriptorPlacement tests the placement of a 'BaseDescriptor'
from 'worktoy.desc': two names, two classes, and the clone.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox, BaseDescriptor
from worktoy.waitaminute.desc import SharedDescriptor
from . import DescTest


class TestBaseDescriptorPlacement(DescTest):
  """
  One descriptor bound to two names in a class body must give two
  attributes, and one bound in two classes must be refused. The tests
  pin the clone the second name receives, the refusal of a second class,
  the placement at the same name again, and what a clone carries.
  """

  def test_second_name_gets_clone(self) -> None:
    class Owner:
      a = b = AttriBox[int](1)

    first, second = Owner.__dict__['a'], Owner.__dict__['b']
    self.assertIsNot(first, second)
    self.assertEqual((first.getFieldName(), second.getFieldName()),
                     ('a', 'b'))
    self.assertIs(second.getFieldOwner(), Owner)
    owner = Owner()
    owner.a = 2
    self.assertEqual((owner.a, owner.b), (2, 1))

  def test_second_class_refused(self) -> None:
    box = AttriBox[int](0)

    class First:
      x = box

    class Later:
      pass

    with self.assertRaises(SharedDescriptor) as context:
      box.__set_name__(Later, 'y')
    self.assertIs(context.exception.desc, box)
    self.assertIs(context.exception.owner, First)
    self.assertEqual(context.exception.fieldName, 'x')
    self.assertIs(context.exception.newOwner, Later)
    self.assertEqual(context.exception.newName, 'y')
    self.assertIsInstance(context.exception, SyntaxError)
    self.assertIn("The 'AttriBox' at 'First.x' is placed again at 'Later.y'",
                  str(context.exception))
    with self.assertRaises((SharedDescriptor, RuntimeError)) as context:
      class Second:
        y = box
    exception = context.exception.__cause__ or context.exception
    self.assertIs(exception.desc, box)
    self.assertIs(exception.owner, First)
    self.assertEqual(exception.fieldName, 'x')
    self.assertEqual(exception.newOwner.__name__, 'Second')
    self.assertEqual(exception.newName, 'y')
    self.assertIn("'Second.y'", str(exception))

  def test_same_name_again_accepted(self) -> None:
    class Owner:
      x = AttriBox[int](0)

    box = Owner.__dict__['x']
    box.__set_name__(Owner, 'x')
    self.assertIs(Owner.__dict__['x'], box)
    self.assertEqual(Owner().x, 0)

  def test_clone_carries_declaration_not_placement(self) -> None:
    class Owner:
      x = AttriBox[int](3)

      @x.onSet
      def _react(self, value: int) -> None:
        """Recorded on the box."""

    box = Owner.__dict__['x']
    _ = Owner().x
    clone = box.clone()
    self.assertIsInstance(clone, AttriBox)
    self.assertIsNot(clone, box)
    self.assertIsNone(clone.getFieldOwner())
    self.assertEqual(clone.getFieldName(), '<AttriBox>')
    self.assertEqual(clone.getPosArgs(), (3,))
    self.assertIs(clone.getFieldType(), int)
    self.assertEqual(clone._getOnSetKeys(), ('_react',))
    self.assertFalse(clone.hasContext())

    class Other:
      pass

    clone.__set_name__(Other, 'z')
    self.assertEqual(clone._getStorageName(), '__z__attribox_field_object__')
    self.assertEqual(box._getStorageName(), '__x__attribox_field_object__')

  def test_base_descriptor_stores_nothing(self) -> None:
    class Owner:
      d = BaseDescriptor()

    owner = Owner()
    self.assertIs(owner.d, Owner.__dict__['d'])

  def test_second_name_sorting_before_the_first(self) -> None:
    class Owner:
      b = a = AttriBox[int](1)

    self.assertIsNot(Owner.__dict__['a'], Owner.__dict__['b'])
    self.assertEqual(Owner.__dict__['a'].getFieldName(), 'a')
    self.assertEqual(Owner.__dict__['b'].getFieldName(), 'b')
    owner = Owner()
    owner.b = 2
    self.assertEqual((owner.a, owner.b), (1, 2))

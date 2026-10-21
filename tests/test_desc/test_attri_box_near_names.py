"""
TestAttriBoxNearNames subclasses 'DescTest' from the 'tests.test_desc'
package and pins that two boxes whose field names differ only in how
their words are joined or capitalised, such as 'fooBar' and 'foo_bar',
are two fields with two slots on every instance, as plain Python gives a
class body with two such names. The storage name of a box is derived
from the field name as written, so two different names can never derive
one storage name, and a class body declaring both is built as any other.
Such a pair used to be refused with 'StorageCollision', because the
storage name was the snake-cased private name of the field, under which
the two shared one slot.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox, FixBox
from worktoy.mcls import BaseObject
from worktoy.waitaminute import MissingVariable

from . import DescTest


class TestAttriBoxNearNames(DescTest):
  """
  TestAttriBoxNearNames provides tests for boxes whose field names differ
  only in word joining or capitalisation.
  """

  def test_camel_and_snake_coexist(self) -> None:
    """'fooBar' and 'foo_bar' on one class are two fields, each holding
    its own default under its own storage name."""

    class Owner:
      fooBar = AttriBox[int](1)
      foo_bar = AttriBox[str]('s')

    owner = Owner()
    self.assertEqual(owner.fooBar, 1)
    self.assertEqual(owner.foo_bar, 's')
    expected = {
      '__fooBar__attribox_field_object__': 1,
      '__foo_bar__attribox_field_object__': 's',
    }
    self.assertEqual(vars(owner), expected)

  def test_write_reaches_one_slot(self) -> None:
    """A write to 'fooBar' leaves 'foo_bar' as it was, and the other way
    round."""

    class Owner:
      fooBar = AttriBox[int](1)
      foo_bar = AttriBox[int](2)

    owner = Owner()
    owner.fooBar = 10
    self.assertEqual(owner.fooBar, 10)
    self.assertEqual(owner.foo_bar, 2)
    owner.foo_bar = 20
    self.assertEqual(owner.fooBar, 10)
    self.assertEqual(owner.foo_bar, 20)

  def test_deletion_leaves_the_other(self) -> None:
    """Deleting 'foo_bar' leaves 'fooBar' standing, and reading the
    deleted field raises 'MissingVariable' as for any deleted box."""

    class Owner:
      fooBar = AttriBox[int](1)
      foo_bar = AttriBox[int](2)

    owner = Owner()
    owner.fooBar = 10
    del owner.foo_bar
    self.assertEqual(owner.fooBar, 10)
    with self.assertRaises(MissingVariable):
      _ = owner.foo_bar

  def test_case_coexists(self) -> None:
    """'X' and 'x' are two fields."""

    class Owner:
      X = AttriBox[int](1)
      x = AttriBox[int](2)

    owner = Owner()
    self.assertEqual(owner.X, 1)
    self.assertEqual(owner.x, 2)
    expected = {
      '__X__attribox_field_object__': 1,
      '__x__attribox_field_object__': 2,
    }
    self.assertEqual(vars(owner), expected)

  def test_inherited_near_name_coexists(self) -> None:
    """'foo_bar' in a subclass body is a second field beside the 'fooBar'
    the subclass inherits, however far up the method resolution order
    that was declared, and a write to either leaves the other."""

    class Parent(BaseObject):
      fooBar = AttriBox[int](1)

    class Middle(Parent):
      pass

    class Child(Middle):
      foo_bar = AttriBox[str]('s')

    child = Child()
    self.assertEqual(child.fooBar, 1)
    self.assertEqual(child.foo_bar, 's')
    child.fooBar = 7
    self.assertEqual(child.foo_bar, 's')
    child.foo_bar = 't'
    self.assertEqual(child.fooBar, 7)
    self.assertEqual(Parent().fooBar, 1)

  def test_other_box_class_coexists(self) -> None:
    """A 'FixBox' and an 'AttriBox' of like names store each under its
    own class name as well."""

    class Owner:
      fooBar = AttriBox[int](1)
      foo_bar = FixBox[str]('s')

    owner = Owner()
    self.assertEqual(owner.fooBar, 1)
    self.assertEqual(owner.foo_bar, 's')
    expected = {
      '__fooBar__attribox_field_object__',
      '__foo_bar__fixbox_field_object__',
    }
    self.assertEqual(set(vars(owner)), expected)

  def test_subclass_redeclaration_takes_over(self) -> None:
    """A subclass redeclaring a field of the same name takes it over, as
    before."""

    class Parent(BaseObject):
      fooBar = AttriBox[int](1)

    class Child(Parent):
      fooBar = AttriBox[int](2)

    self.assertEqual(Child().fooBar, 2)
    self.assertEqual(Parent().fooBar, 1)

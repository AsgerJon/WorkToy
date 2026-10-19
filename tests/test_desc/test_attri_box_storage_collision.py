"""
TestAttriBoxStorageCollision subclasses 'DescTest' and pins that a class
body declaring two boxes whose field names derive the same storage name,
such as 'fooBar' and 'foo_bar', is refused with 'StorageCollision' as the
class is created. The two boxes used to share one slot on every instance,
so reading one returned the value of the other, and the docstring could
only call the result undefined.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox, FixBox
from worktoy.mcls import BaseObject
from worktoy.waitaminute.desc import StorageCollision

from . import DescTest


class TestAttriBoxStorageCollision(DescTest):
  """
  TestAttriBoxStorageCollision provides tests for the refusal of two boxes
  sharing a storage name on one owner.
  """

  def test_camel_and_snake_refused(self) -> None:
    """'fooBar' and 'foo_bar' on one class are refused, the exception
    naming the owner, both fields and the storage name."""
    with self.assertRaises(Exception) as context:
      class Owner(BaseObject):
        fooBar = AttriBox[int](1)
        foo_bar = AttriBox[str]('s')
    e = self._unwrapSetName(context.exception, StorageCollision)
    self.assertIsInstance(e, StorageCollision)
    self.assertEqual(e.ownerName, 'Owner')
    self.assertEqual(e.fieldName, 'foo_bar')
    self.assertEqual(e.existingName, 'fooBar')
    self.assertEqual(e.storageName, '__foo_bar__attribox_field_object__')
    self.assertIn("'fooBar'", str(e))
    self.assertIn("'foo_bar'", str(e))
    self.assertEqual(str(e), repr(e))
    self.assertIsInstance(e, SyntaxError)

  def test_case_refused(self) -> None:
    """'X' and 'x' derive one storage name and are refused as well."""
    with self.assertRaises(Exception) as context:
      class Owner:
        X = AttriBox[int](1)
        x = AttriBox[int](2)
    e = self._unwrapSetName(context.exception, StorageCollision)
    self.assertIsInstance(e, StorageCollision)

  def test_distinct_names_accepted(self) -> None:
    """Fields whose names derive distinct storage names are declared as
    ever, and each holds its own value."""

    class Owner(BaseObject):
      fooBar = AttriBox[int](1)
      fooBaz = AttriBox[str]('s')

    owner = Owner()
    self.assertEqual(owner.fooBar, 1)
    self.assertEqual(owner.fooBaz, 's')

  def test_other_box_class_accepted(self) -> None:
    """A 'FixBox' stores under its own class name, so it never collides
    with an 'AttriBox' of a like name."""

    class Owner(BaseObject):
      fooBar = AttriBox[int](1)
      foo_bar = FixBox[str]('s')

    owner = Owner()
    self.assertEqual(owner.fooBar, 1)
    self.assertEqual(owner.foo_bar, 's')

  def test_subclass_redeclaration_accepted(self) -> None:
    """A subclass redeclaring a field of the same name takes it over,
    which is no collision."""

    class Parent(BaseObject):
      fooBar = AttriBox[int](1)

    class Child(Parent):
      fooBar = AttriBox[int](2)

    self.assertEqual(Child().fooBar, 2)
    self.assertEqual(Parent().fooBar, 1)

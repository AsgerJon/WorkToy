"""
TestAliasRedeclaration subclasses 'DescTest' from the 'tests.test_desc'
package and pins that a subclass may redeclare a field its parent exposes
under a second name through 'Alias'. The alias swaps itself for the
parent's box as the parent is created, so the parent holds one box under
two names. The subclass redeclaring the field is a redeclaration, not a
collision, and on a subclass instance the alias keeps reading and writing
the one storage name the field name derives. Such a subclass used to be
refused with 'StorageCollision', the guard comparing the parent's box with
itself under the alias name.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox, Alias
from worktoy.mcls import BaseObject

from . import DescTest


class TestAliasRedeclaration(DescTest):
  """
  TestAliasRedeclaration provides tests for a subclass redeclaring a field
  the parent aliases.
  """

  @staticmethod
  def _makePair() -> tuple[type, type]:
    """A parent aliasing its field and a subclass redeclaring it."""

    class Parent(BaseObject):
      v = AttriBox[int](1)
      w = Alias('v')

    class Child(Parent):
      v = AttriBox[int](2)

    return Parent, Child

  def test_subclass_builds(self) -> None:
    """The subclass is built, its own default stands, and the parent is
    as it was."""
    Parent, Child = self._makePair()
    self.assertEqual(Child().v, 2)
    self.assertEqual(Parent().v, 1)
    self.assertEqual(Parent().w, 1)

  def test_alias_shares_storage_on_subclass(self) -> None:
    """On a subclass instance the alias reads the redeclared field, a write
    through either name reaches the other, and the instance holds one
    storage name for the field."""
    Parent, Child = self._makePair()
    child = Child()
    self.assertEqual(child.v, 2)
    self.assertEqual(child.w, 2)
    child.w = 5
    self.assertEqual(child.v, 5)
    child.v = 7
    self.assertEqual(child.w, 7)
    keys = [k for k in vars(child) if k.endswith('_field_object__')]
    self.assertEqual(keys, ['__v__attribox_field_object__'])

  def test_alias_is_the_parent_box(self) -> None:
    """The alias name on the parent holds the parent's box itself, and the
    subclass holds its own box under the field name alone."""
    Parent, Child = self._makePair()
    self.assertIs(Parent.__dict__['w'], Parent.__dict__['v'])
    self.assertNotIn('w', Child.__dict__)
    self.assertIsNot(Child.__dict__['v'], Parent.__dict__['v'])

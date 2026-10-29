"""
TestAliasRedeclaration subclasses 'DescTest' from the 'tests.test_desc'
package and pins that a subclass may redeclare a field its parent exposes
under a second name through 'Alias'. The alias stays on the parent and
forwards each access to the box the field name holds on the class of the
instance, so on a subclass instance it reads and writes the subclass's
own box, under the one storage name the field name derives. Such a
subclass used to be refused with 'StorageCollision', and after that guard
went the alias swapped itself for the parent's box, so a subclass
redeclaring the field reached the parent's box through the alias.
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

  def test_alias_stays_on_the_parent(self) -> None:
    """The alias name on the parent holds the alias, and the subclass
    holds its own box under the field name alone."""
    Parent, Child = self._makePair()
    self.assertIsInstance(Parent.__dict__['w'], Alias)
    self.assertIsNot(Parent.__dict__['w'], Parent.__dict__['v'])
    self.assertNotIn('w', Child.__dict__)
    self.assertIsNot(Child.__dict__['v'], Parent.__dict__['v'])

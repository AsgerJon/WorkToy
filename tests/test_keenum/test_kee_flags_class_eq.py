"""
TestKeeFlagsClassEq subclasses 'KeeTest' and pins that a 'KeeFlags' class
compares by identity without hashing the other operand. 'KeeFlagsMeta'
defined an '__eq__' that hashed the other operand and re-raised most
failures, so comparing a flags class with an unhashable object, such as
a member of unhashable value, raised, as did 'in' on a list holding one.
The class keeps its hash, so it still serves as a dict key.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeNum, Kee, KeeFlags, KeeFlag

from . import KeeTest


class Perm(KeeFlags):
  """Perm is a flags class."""

  READ = KeeFlag()


class Other(KeeFlags):
  """Other is another flags class of the same shape."""

  READ = KeeFlag()


class Bag(KeeNum):
  """Bag holds a member whose value cannot be hashed."""

  A = Kee[list]([1, 2])


class TestKeeFlagsClassEq(KeeTest):
  """
  TestKeeFlagsClassEq provides tests for comparing 'KeeFlags' classes.
  """

  def test_unhashable_operand(self) -> None:
    """Comparing with a member of unhashable value answers 'False'."""
    self.assertFalse(Perm == Bag.A)
    self.assertTrue(Perm != Bag.A)

  def test_in_list(self) -> None:
    """'in' on a list holding such a member answers 'False'."""
    self.assertNotIn(Perm, [Bag.A])

  def test_identity(self) -> None:
    """A flags class equals itself and no other class."""
    self.assertTrue(Perm == Perm)
    self.assertFalse(Perm == Other)
    self.assertFalse(Perm == [1])

  def test_dict_key(self) -> None:
    """A flags class still serves as a dict key."""
    table = {Perm: 'perm', Other: 'other'}
    self.assertEqual(table[Perm], 'perm')
    self.assertEqual(table[Other], 'other')

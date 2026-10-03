"""
TestInheritedMemberLookup subclasses 'KeeTest' and pins that an
enumeration takes from its base only what is a member there. 'KeeMeta'
used to take any attribute of the base under the name of a member, so a
plain class attribute broke the class with a message unrelated to the
cause, and a member of another enumeration held as an attribute became a
member of the subclass. 'KeeFlagsSpace' likewise read 'flags' off every
base, so a plain mixin carrying a 'flags' attribute broke a flags class.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeNum, Kee, KeeFlags, KeeFlag

from . import KeeTest


class Color(KeeNum):
  """Color is an enumeration whose member another holds as a plain
  attribute."""

  RED = Kee[int](1)


class Mixin:
  """Mixin carries a plain 'flags' attribute."""

  flags = ['not a flag']


class TestInheritedMemberLookup(KeeTest):
  """
  TestInheritedMemberLookup provides tests for the members and flags an
  enumeration takes from its bases.
  """

  def test_plain_attribute_of_base(self) -> None:
    """A member named like a plain attribute of the base is a member of
    its own, and the base keeps the attribute."""

    class Base(KeeNum):
      A = Kee[int](1)
      LIMIT = 10

    class Derived(Base):
      LIMIT = Kee[int](5)

    self.assertEqual([m.name for m in Derived], ['A', 'LIMIT'])
    self.assertEqual(Derived.LIMIT.value, 5)
    self.assertEqual(Base.LIMIT, 10)

  def test_foreign_member_of_base(self) -> None:
    """A member named like a member of another enumeration that the base
    holds as an attribute is a member of its own."""

    class Base(KeeNum):
      A = Kee[int](1)
      OTHER = Color.RED

    class Derived(Base):
      OTHER = Kee[int](5)

    self.assertIsNot(Derived.OTHER, Color.RED)
    self.assertIn(Derived.OTHER, Derived)
    self.assertEqual(Derived.OTHER.value, 5)

  def test_inherited_member_shared(self) -> None:
    """A member the base declares is the very member in the subclass."""

    class Base(KeeNum):
      A = Kee[int](1)

    class Derived(Base):
      B = Kee[int](2)

    self.assertIs(Derived.A, Base.A)
    self.assertEqual([m.name for m in Derived], ['A', 'B'])

  def test_flags_mixin_last(self) -> None:
    """A plain mixin after the flags root contributes no flags."""

    class P(KeeFlags, Mixin):
      READ = KeeFlag()

    self.assertEqual([f.name for f in P.flags], ['READ'])

  def test_flags_mixin_first(self) -> None:
    """A plain mixin before a flags base contributes no flags, and the
    flags of the flags base are inherited."""

    class Perm(KeeFlags):
      READ = KeeFlag()

    class P(Mixin, Perm):
      WRITE = KeeFlag()

    self.assertEqual([f.name for f in P.flags], ['READ', 'WRITE'])

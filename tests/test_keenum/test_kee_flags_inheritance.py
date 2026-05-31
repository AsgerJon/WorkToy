"""
TestKeeFlagsInheritance pins the flag bit-positions and member counts of
'KeeFlags' classes across multiple levels of inheritance.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.keenum import KeeFlags, KeeFlag
from . import KeeTest

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestKeeFlagsInheritance(KeeTest):
  """
  These tests are adversarial towards the index bookkeeping in
  'KeeFlagsSpace'. The existing meta tests assert only that
  'value == index + constant', which holds for any self-consistent
  indexing. They do not pin the absolute bit-position assigned to each
  flag, nor the materialized member count, under inheritance. A flag whose
  bit-position is computed wrong would still satisfy the existing tests but
  fail here.
  """

  def testFlagBitPositions(self) -> None:
    """A child's flags keep declaration order across the inheritance
    boundary, base flags first, and are numbered 0..n-1 with no gaps."""

    class Base(KeeFlags):
      A = KeeFlag()
      B = KeeFlag()

    class Child(Base):
      C = KeeFlag()
      D = KeeFlag()

    self.assertEqual([f.name for f in Base.flags], ['A', 'B'])
    self.assertEqual([f.index for f in Base.flags], [0, 1])
    self.assertEqual([f.name for f in Child.flags], ['A', 'B', 'C', 'D'])
    self.assertEqual([f.index for f in Child.flags], [0, 1, 2, 3])

  def testMemberCount(self) -> None:
    """A KeeFlags class materializes exactly '2 ** flagCount' members,
    inherited flags included."""

    class Base(KeeFlags):
      A = KeeFlag()
      B = KeeFlag()

    class Child(Base):
      C = KeeFlag()
      D = KeeFlag()

    self.assertEqual(len(Base), 4)
    self.assertEqual(len(Child), 16)

  def testParentNotCorruptedByChild(self) -> None:
    """Building a child must not mutate the parent's flag set. The
    'getKeeFlags' getter merges into the base-flags dict, so this guards
    against that merge leaking back onto the parent class."""

    class Base(KeeFlags):
      A = KeeFlag()
      B = KeeFlag()

    class Child(Base):  # noqa
      C = KeeFlag()
      D = KeeFlag()

    self.assertEqual([f.name for f in Base.flags], ['A', 'B'])
    self.assertEqual([f.index for f in Base.flags], [0, 1])
    self.assertEqual(len(Base), 4)

  def testCombinedMemberBitmask(self) -> None:
    """A combined member's index is the OR of its high flags' bits, and
    resolution by name set is order- and case-insensitive."""

    class Base(KeeFlags):
      A = KeeFlag()
      B = KeeFlag()

    class Child(Base):
      C = KeeFlag()
      D = KeeFlag()

    member = Child['A', 'C']
    self.assertEqual(member.index, (1 << 0) | (1 << 2))  # 5
    self.assertEqual(set(member.names), {'A', 'C'})
    self.assertIs(Child['C', 'A'], member)
    self.assertIs(Child['a_c'], member)

  def testNullAndFullMembers(self) -> None:
    """The all-low member is 'NULL' and falsy; the all-high member carries
    every flag and the maximal index."""

    class Base(KeeFlags):
      A = KeeFlag()
      B = KeeFlag()

    class Child(Base):
      C = KeeFlag()
      D = KeeFlag()

    null = Child(0)
    self.assertEqual(null.name, 'NULL')
    self.assertFalse(null)

    full = Child(15)
    self.assertEqual(set(full.names), {'A', 'B', 'C', 'D'})
    self.assertTrue(full)

  def testThreeLevelInheritance(self) -> None:
    """A third level keeps the same contiguous numbering and doubles the
    member count again."""

    class Base(KeeFlags):
      A = KeeFlag()
      B = KeeFlag()

    class Child(Base):
      C = KeeFlag()
      D = KeeFlag()

    class Grand(Child):
      E = KeeFlag()

    self.assertEqual(
      [f.name for f in Grand.flags], ['A', 'B', 'C', 'D', 'E']
    )
    self.assertEqual([f.index for f in Grand.flags], [0, 1, 2, 3, 4])
    self.assertEqual(len(Grand), 32)

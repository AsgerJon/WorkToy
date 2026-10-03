"""
TestKeeFlagsSeveral subclasses 'KeeTest' and pins that a 'KeeFlags' class
looked up by several identifiers resolves each of them as a single lookup
would, a member, a name in any case or order, or an index, and gives the
member having every flag high that any of them has, as 'KeeBox' does.
The lookup used to upper-case every identifier as a flag name, so members
and indices raised 'AttributeError', from the membership test too, and a
combined name among several matched nothing.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeFlags, KeeFlag
from worktoy.waitaminute.keenum import KeeResolveError

from . import KeeTest


class Perm(KeeFlags):
  """Perm holds three flags."""

  READ = KeeFlag()
  WRITE = KeeFlag()
  EXEC = KeeFlag()


class TestKeeFlagsSeveral(KeeTest):
  """
  TestKeeFlagsSeveral provides tests for looking up a 'KeeFlags' class by
  several identifiers.
  """

  def test_members(self) -> None:
    """Several members combine."""
    self.assertIs(Perm[Perm.READ, Perm.WRITE], Perm.READ_WRITE)

  def test_indices(self) -> None:
    """Several indices combine."""
    self.assertIs(Perm[1, 2], Perm.READ_WRITE)

  def test_name_and_index(self) -> None:
    """A name and an index combine."""
    self.assertIs(Perm['read', 4], Perm.READ_EXEC)

  def test_combined_name_among_several(self) -> None:
    """A combined name among several identifiers contributes all its
    flags."""
    self.assertIs(Perm['READ_WRITE', 'EXEC'], Perm.READ_WRITE_EXEC)

  def test_call(self) -> None:
    """A call with several identifiers combines them as subscripting
    does."""
    self.assertIs(Perm(Perm.READ, 4), Perm.READ_EXEC)

  def test_contains(self) -> None:
    """The membership test resolves several identifiers, and answers
    'False' for an identifier matching nothing."""
    self.assertIn((1, 2), Perm)
    self.assertNotIn((1, 'BOGUS'), Perm)

  def test_names_any_case(self) -> None:
    """Several names in any case and order combine, a repeated one
    collapsing."""
    self.assertIs(Perm['write', 'READ', 'read'], Perm.READ_WRITE)

  def test_unknown_name(self) -> None:
    """An unknown name among several raises 'KeeResolveError'."""
    with self.assertRaises(KeeResolveError):
      _ = Perm['READ', 'BOGUS']

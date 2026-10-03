"""
TestKeeFlagsSpaceMerge subclasses 'KeeTest' and pins that the namespace of
a 'KeeFlags' class merges its inherited and declared flags into a new
mapping. 'getKeeFlags' merged the declared flags into the inherited ones
in place, so the inherited mapping came to hold the declared flags as
well, and every merged mapping was that one object.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeFlags, KeeFlag

from . import KeeTest


class Perm(KeeFlags):
  """Perm declares one flag."""
  READ = KeeFlag()


class MorePerm(Perm):
  """MorePerm inherits one flag and declares another."""
  EXEC = KeeFlag()


class TestKeeFlagsSpaceMerge(KeeTest):
  """
  TestKeeFlagsSpaceMerge provides tests for the flag mappings of
  'KeeFlagsSpace'.
  """

  def test_inherited_flags_unchanged(self) -> None:
    """The inherited mapping holds the inherited flags alone."""
    space = MorePerm.__namespace__
    self.assertEqual([*space._getBaseFlags()], ['READ'])

  def test_declared_flags_alone(self) -> None:
    """The mapping of the declared flags holds those alone."""
    space = MorePerm.__namespace__
    self.assertEqual([*space.__kee_flags__], ['EXEC'])

  def test_merged_flags(self) -> None:
    """The merged mapping lists the inherited flags first."""
    space = MorePerm.__namespace__
    self.assertEqual([*space.getKeeFlags()], ['READ', 'EXEC'])

  def test_merged_mapping_is_new(self) -> None:
    """Each merge is a new mapping, which a caller may change freely."""
    space = MorePerm.__namespace__
    merged = space.getKeeFlags()
    self.assertIsNot(merged, space.getKeeFlags())
    self.assertIsNot(merged, space._getBaseFlags())
    merged.clear()
    self.assertEqual([*space.getKeeFlags()], ['READ', 'EXEC'])

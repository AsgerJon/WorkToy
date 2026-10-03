"""
TestKeeFlagsCached subclasses 'KeeTest' and pins that a 'KeeFlags' class
clones its flags once. Every read of 'flags' cloned all of them again, and
so did every 'highs', 'lows', 'name', 'names' and hash of a member, since
those read 'flags'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeFlags, KeeFlag

from . import KeeTest


class Perm(KeeFlags):
  """Perm declares two flags."""
  READ = KeeFlag()
  WRITE = KeeFlag()


class MorePerm(Perm):
  """MorePerm inherits two flags and declares a third."""
  EXEC = KeeFlag()


class TestKeeFlagsCached(KeeTest):
  """
  TestKeeFlagsCached provides tests for the flags a 'KeeFlags' class
  keeps.
  """

  def test_same_flags_each_read(self) -> None:
    """Two reads of 'flags' give the same flag objects."""
    for first, second in zip(Perm.flags, Perm.flags):
      with self.subTest(flag=first.name):
        self.assertIs(first, second)

  def test_members_share_flags(self) -> None:
    """The flags a member reports are those of its class."""
    high, = Perm.READ.highs
    self.assertIs(high, Perm.flags[0])
    low, = Perm.READ.lows
    self.assertIs(low, Perm.flags[1])

  def test_subclass_flags_own(self) -> None:
    """A subclass keeps flags of its own, owned by it."""
    self.assertIs(Perm.flags[0].fieldOwner, Perm)
    self.assertIs(MorePerm.flags[0].fieldOwner, MorePerm)
    self.assertIsNot(MorePerm.flags[0], Perm.flags[0])
    self.assertEqual(len(MorePerm.flags), 3)

  def test_list_change_kept_out(self) -> None:
    """Changing the list 'flags' returns leaves the class unchanged."""
    Perm.flags.clear()
    self.assertEqual(len(Perm.flags), 2)

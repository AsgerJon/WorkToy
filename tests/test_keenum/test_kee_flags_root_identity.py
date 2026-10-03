"""
TestKeeFlagsRootIdentity subclasses 'KeeTest' from the 'tests.test_keenum'
package and pins that the root 'KeeFlags' class is recognised as itself
and not by its name. The metaclass, the namespace and the namespace
compilation used to take any class named 'KeeFlags' for the root: such a
user class built no members, and it replaced the real root for every
flags class built after it, which drives the write guard on members,
'__subclasscheck__' and the choice of '_getValue'. The root is now marked
by the '_root' class keyword, as 'KeeMetaMeta' marks the root of 'KeeNum'.
The classes are built inside the tests, so a failure stays in its test.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeFlags as RootFlags, KeeFlag, KeeFlagsMeta
from worktoy.waitaminute.keenum import KeeWriteOnceError

from . import KeeTest


class TestKeeFlagsRootIdentity(KeeTest):
  """
  TestKeeFlagsRootIdentity provides tests for a user class named
  'KeeFlags'.
  """

  def test_named_like_root_builds_members(self) -> None:
    """A user class named 'KeeFlags' builds its members."""

    class KeeFlags(RootFlags):
      READ = KeeFlag()
      WRITE = KeeFlag()

    self.assertEqual(len(KeeFlags), 4)
    self.assertIs(KeeFlags['write', 'read'], KeeFlags.READ_WRITE)

  def test_root_kept(self) -> None:
    """The real root stays the root after such a class is built."""

    class KeeFlags(RootFlags):
      READ = KeeFlag()

    self.assertIs(KeeFlagsMeta.__kee_class__, RootFlags)
    self.assertIsSubclass(KeeFlags, RootFlags)

  def test_later_flags_unaffected(self) -> None:
    """A flags class built afterwards keeps its write guard and its place
    under the root."""

    class KeeFlags(RootFlags):
      READ = KeeFlag()

    class Perm(RootFlags):
      READ = KeeFlag()
      WRITE = KeeFlag()

    self.assertIsSubclass(Perm, RootFlags)
    with self.assertRaises(KeeWriteOnceError):
      Perm.READ = None

  def test_named_like_root_inherits_flags(self) -> None:
    """A user class named 'KeeFlags' inherits the flags of its parent."""

    class Base(RootFlags):
      READ = KeeFlag()

    class KeeFlags(Base):
      WRITE = KeeFlag()

    self.assertEqual(len(KeeFlags), 4)
    self.assertEqual(KeeFlags.READ_WRITE.names, {'READ', 'WRITE'})

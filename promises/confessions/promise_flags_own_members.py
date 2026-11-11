"""
ConfessedFlagsOwnMembers confesses that a 'KeeFlags' subclass does not
hold members of its own for the flags of its base.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase, skip

from worktoy.keenum import KeeFlag

from ..keenum._file_access import FileAccess


class ConfessedFlagsOwnMembers(TestCase):
  """
  Promised in 1.1.0: a 'KeeFlags' subclass holds members of its own, so
  the member of the subclass and the member of its base with the same
  flags are two objects, equal and hashing alike.

  Taken back in 1.2.0. Two objects for one set of flags each carried
  what its own class gave it, and what they carried could differ while
  they compared equal, as their values did
  ('promise_flags_mask_value.py'). That the two are equal and hash
  alike is still owed, in 'promises/keenum/promise_flags.py'; that they
  are two objects is not.
  """

  @skip('Confessed in 1.2.0: a subclass holds no members of its own.')
  def test_members_of_its_own(self) -> None:
    class Extended(FileAccess):
      APPEND = KeeFlag()

    self.assertIsNot(Extended.READ, FileAccess.READ)

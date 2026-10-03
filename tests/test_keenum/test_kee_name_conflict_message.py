"""
TestKeeNameConflictMessage subclasses 'KeeTest' and pins that the message
of 'KeeNameConflict' names the member. It read '__name__' off the 'Kee',
which has none, so every message named the member 'Unknown'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeNum, Kee
from worktoy.waitaminute.keenum import KeeNameConflict

from . import KeeTest


class TestKeeNameConflictMessage(KeeTest):
  """
  TestKeeNameConflictMessage provides tests for the message of
  'KeeNameConflict'.
  """

  def test_member_named(self) -> None:
    """The message renders the member, which carries its first name."""
    kee = Kee[int](1)
    with self.assertRaises(KeeNameConflict) as context:
      class Color(KeeNum):  # noqa: F841
        RED = kee
        CRIMSON = kee
    message = str(context.exception)
    self.assertIn(str(kee), message)
    self.assertNotIn('Unknown', message)

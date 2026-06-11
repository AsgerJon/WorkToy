"""
TestMemberAlias pins how a 'KeeNum' class body responds to aliasing a
member, as in 'CRIMSON = RED'. The namespace shadow space resolves the
read of 'RED' to the claimed 'Kee' object, and binding that object
under a second name raises 'KeeNameConflict'. Before the shadow space,
the same body raised a bare 'NameError', or worse, silently bound a
module-level global that happened to share the member's name.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import Kee, KeeNum
from worktoy.waitaminute.keenum import KeeNameConflict
from . import KeeTest

#  Module-level decoy sharing its name with the member declared in the
#  test bodies below.
RED = 'global decoy'


class TestMemberAlias(KeeTest):
  """
  TestMemberAlias provides tests for aliasing 'KeeNum' members in the
  class body, which the shadow space turns into a loud name conflict
  instead of a silent global capture.
  """

  def test_alias_raises_name_conflict(self) -> None:
    """
    Testing that binding a member's 'Kee' object under a second name
    raises 'KeeNameConflict'.
    """
    with self.assertRaises(KeeNameConflict):
      class Color(KeeNum):
        CHERRY = Kee[int](1)
        SCARLET = CHERRY

  def test_alias_conflict_beats_global_decoy(self) -> None:
    """
    Testing that the member name resolves to the claimed 'Kee' object
    rather than the module-level decoy, so the alias attempt raises
    'KeeNameConflict' instead of silently binding the decoy.
    """
    with self.assertRaises(KeeNameConflict):
      class Hue(KeeNum):
        RED = Kee[int](1)
        SCARLET = RED

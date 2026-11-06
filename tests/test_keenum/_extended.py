"""
Extended is 'Permission' with one flag more.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeFlag

from . import Permission


class Extended(Permission):
  """
  A flags class based on another keeps the flags of its base first and
  builds members of its own. 'Extended' adds 'OWN' behind the three
  flags of 'Permission', so it has sixteen members, and its 'READ' is
  equal to the 'READ' of 'Permission' without being the same object.
  """

  OWN = KeeFlag()

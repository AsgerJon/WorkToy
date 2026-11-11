"""
Extended is 'Permission' with one flag more.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import Kee

from . import Permission


class Extended(Permission):
  """
  A flags class based on another holds the flags of its base first and
  shares the members of its base, the very objects. 'Extended' adds
  'OWN' behind the three flags of 'Permission', so it holds sixteen
  members, eight of them those of 'Permission', and builds the eight
  holding 'OWN'.
  """

  OWN = Kee[str]()

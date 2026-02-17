"""

"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.keenum import KeeFlags, KeeFlag

if TYPE_CHECKING:  # pragma: no cover
  pass


class FlagsExample(KeeFlags):
  """
  FlagsExample is an example of the use of the KeeFlags class.
  It defines a set of flags with specific values.
  """

  NEVER = KeeFlag()
  GONNA = KeeFlag()
  GIVE = KeeFlag()

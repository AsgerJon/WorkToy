"""
KeeFlags enumerations all combinations of boolean valued flags. It
dynamically adds instances of KeeFlags for each boolean valued entry. The
result is a KeeNum-like enumeration consisting of all possible combinations
of boolean flags.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeNum
from . import KeeFlagsMeta


class KeeFlags(KeeNum, metaclass=KeeFlagsMeta):
  """
  KeeFlags is a metaclass that dynamically creates instances of KeeFlags
  for each boolean valued entry. It allows for the creation of an
  enumeration consisting of all possible combinations of boolean flags.
  """

  def _getValue(self) -> int:
    """
    Returns the integer value of the KeeFlags instance.
    """
    included = list(KeeNum._getValue(self))
    if not included:
      return 0
    out = included[0].getValue()
    for kee in included:
      out |= kee.getValue()
    return out

"""
Shade is an enumeration of integers with a '__class_resolve__' hook.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.keenum import KeeNum, Kee

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any


class Shade(KeeNum):
  """
  An enumeration may decide identifiers of its own through
  '__class_resolve__', which the lookups consult after identity and
  name and before index and value. 'Shade' resolves a 'float' to the
  member whose value is nearest below it, and defers for anything else,
  so 'Shade(5.5)' is 'MID' while 'Shade[1]' is still the second member.
  """

  LIGHT = Kee[int](1)
  MID = Kee[int](5)
  DARK = Kee[int](9)

  @classmethod
  def __class_resolve__(cls, identifier: Any) -> Any:
    if isinstance(identifier, float):
      for member in reversed(cls.members):
        if member.value <= identifier:
          return member
    return NotImplemented

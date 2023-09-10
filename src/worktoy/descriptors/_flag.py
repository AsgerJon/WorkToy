"""WorkToy - Descriptors - Flag
Implementation of boolean valued descriptor."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.descriptors import AbstractAttribute


class Flag(AbstractAttribute):
  """WorkToy - Descriptors - Flag
  Implementation of boolean valued descriptor."""

  @classmethod
  def getClassDefaultValue(cls) -> int:
    """Getter-function for default value."""
    return False

  def getType(self) -> type:
    """Getter-function for value type."""
    return bool

"""WorkToy - Fields - ReadOnly
Implements descriptor class for write-once attributes."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from worktoy.fields import Attribute


class ReadOnly(Attribute):
  """WorkToy - Fields - ReadOnly
  Implements descriptor class for write-once attributes."""

  def __init__(self, *args, **kwargs) -> None:
    Attribute.__init__(self, *args, **kwargs)

  def __set__(self, obj: Any, newValue: Any) -> None:
    setattr(obj, self._name, newValue)

"""WorkToy - Fields - Flag
Boolean descriptor class implementation."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from worktoy.fields import Attribute


class Flag(Attribute):
  """WorkToy - Fields - Flag
  Boolean descriptor class implementation."""

  def __init__(self, *args, **kwargs) -> None:
    Attribute.__init__(self, *args, **kwargs)

  def __get__(self, obj: Any, cls: type) -> bool:
    return True if Attribute.__get__(self, obj, cls) else False

  def __set__(self, obj: Any, newValue: Any) -> None:
    Attribute.__set__(self, obj, True if newValue else False)

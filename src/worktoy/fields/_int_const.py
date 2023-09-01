"""WorkToy - Fields - IntConst
Integer-valued field of constant value."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.fields import ReadOnlyField


class IntConst(ReadOnlyField):
  """WorkToy - Fields - IntConst
  Integer-valued field of constant value."""

  def __init__(self, *args, **kwargs) -> None:
    ReadOnlyField.__init__(self, *args, **kwargs)

  def getFieldSource(self) -> type:
    """Integer"""
    return int

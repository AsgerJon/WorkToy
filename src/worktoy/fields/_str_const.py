"""WorkToy - Fields - StrConst
String-valued field of constant value."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.fields import ReadOnlyField, AbstractField


class StrConst(ReadOnlyField):
  """WorkToy - Fields - StrConst
  String-valued field of constant value."""

  def __init__(self, fieldType: type, *args, **kwargs) -> None:
    AbstractField.__init__(self, *args, **kwargs)

  def getFieldSource(self) -> type:
    """String."""
    return str

"""WorkToy - Fields - StrField
String-valued mutable field."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from icecream import ic

from worktoy.core import Function
from worktoy.fields import AbstractField


class StrField(AbstractField):
  """WorkToy - Fields - StrField
  String-valued mutable field."""

  def __init__(self, defVal: str, *args, **kwargs) -> None:
    AbstractField.__init__(self, defVal, *args, **kwargs)

  def getFieldSource(self) -> type:
    """str type"""
    return str

  def getPermissionLevel(self) -> int:
    """Protected. """
    return 2


class StrLabel(StrField):
  """WorkToy - Fields - StrLabel
  String-valued mutable label."""

  def __init__(self, defVal: str, *args, **kwargs) -> None:
    StrField.__init__(self, defVal, *args, **kwargs)

  def getPermissionLevel(self) -> int:
    """ReadOnly, 1"""
    return 1
